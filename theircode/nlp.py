#!/usr/bin/python
from decoder import *
from var import *

class C_ounter(Counter):
    __count=int()

    @property
    def _count(self):
        return self.__count

    def __getitem__(self, child):
        prob=Counter.__getitem__(self, child)/self.__count
        if not prob:
            prob=def_prob
        return prob

    def add(self, child, n):
        Counter.__setitem__(self, child, Counter.__getitem__(self, child)+n)
        self.__count+=n
        return

class Param_dict:
    def __init__(self, fh):
        self.__e=defaultdict(C_ounter)
        self.__t=defaultdict(C_ounter)
        for buffer in fh.iter_file(Filter.train.value):
            w0, t0=buffer[0]
            w1, t1=buffer[1]
            self.__t[t0].add(t1, 1)
            if t1!='STOP':
                self.__e[t1].add(w1.lower(), 1)
        return

    @property
    def _e(self):
        return self.__e

    @property
    def _t(self):
        return self.__t

class File_handler:
    def __init__(self, f):
        self.__f=f
        self.__f_pox=deque()
        return

    def close(self):
        self.__f.close()
        return

    def iter_file(self, filter_, reverse=False):
        start_word_tag=('', 'START')
        stop_word_tag=('', 'STOP')
        buffer=deque([start_word_tag], maxlen=2)
        if reverse:
            iter_=self.__reverse_iter
        else:
            iter_=self.__forward_iter
        for line in iter_():
            m=re.match(filter_, line)
            if m:
                word_tag=(m.group(1), m.group(2))
                buffer.append(word_tag)
                yield buffer
            elif line=='\n':
                if buffer[1][1]!='START':
                    buffer.append(stop_word_tag)
                    yield buffer
                    buffer.append(start_word_tag)
        return

    def __forward_iter(self):
        f=self.__f
        f_pox=self.__f_pox
        try:
            if f_pox:
                for line in f_pox:
                    yield line
            else:
                f.seek(0, 0)
                for line in f:
                    yield line
                    f_pox.append(line)
        except Exception as e:
            raise Exception('Unhandled exception. {:}'.format(f.name)) from e
        return

    def __reverse_iter(self):
        f=self.__f
        f_pox=self.__f_pox
        if f_pox:
            for i in range(len(f_pox)-1, -1, -1):
                yield f_pox[-1]
                f_pox.rotate(1)
        else:
            raise Exception('Try running forward_iter first. {:}'.format(f.name))
        return

    def write(self, string):
        try:
            self.__f.write(string)
        except Exception as e:
            raise Exception('Unhandled exception. {:}'.format(f.name)) from e
        return

class HMM:
    def __init__(self, f_train_m, f_dev_in, f_dev_out, d):
        self.fh_train_m=File_handler(f_train_m)
        self.fh_dev_in=File_handler(f_dev_in)
        self.fh_dev_out=File_handler(f_dev_out)
        self.param=Param_dict(self.fh_train_m)
        self.decoder=d
        return

    def decode(self):
        fh_dev_in=self.fh_dev_in
        fh_dev_out=self.fh_dev_out
        param=self.param
        decoder=self.decoder
        try:
            decoder_dict[decoder](fh_dev_in, fh_dev_out, param)
        except Exception as e:
            raise Exception('Decoding module exception. {:}'.format(decoder)) from e
        return

def modify_train(f_train_m, f_train, k=3):
    fh_train_m=File_handler(f_train_m)
    fh_train=File_handler(f_train)
    count=Counter()
    for buffer in fh_train.iter_file(Filter.train.value):
        word=buffer[1][0]
        count[word.lower()]+=1
    for buffer in fh_train.iter_file(Filter.train.value):
        word=buffer[1][0]
        tag=buffer[1][1]
        if tag=='STOP':
            fh_train_m.write('\n')
        elif count[word.lower()]<k:
            fh_train_m.write('{:} {:}\n'.format(word, '#UNK#'))
        else:
            fh_train_m.write('{:} {:}\n'.format(word, tag))
    return

def add_decoder_module(name, f):
    if isinstance(name, str) and hasattr(f, '__call__'):
        decoder_dict[name]=f
        print('Decoder module added. ')
    else:
        raise Exception('Try: add_decoder_module(name <string>, module <callable>). ')
    return

decoder_dict={'simple':simple_decoder, 'viterbi':viterbi_decoder}#, 'max-marginal':max_marginal_decoder}

### DEBUGGING ONLY ###
def run(p, d):
    try:
        f_name='{:}train-m'.format(p)
        f_train_m=open(f_name, 'w', encoding='utf-8', errors='surrogateescape')
        f_name='{:}train'.format(p)
        f_train=open(f_name, 'r', encoding='utf-8', errors='surrogateescape')
        modify_train(f_train_m, f_train)
        f_train.close()
        f_train_m.close()
    except FileExistsError:
        pass
    except Exception as e:
        raise e

    f_name='{:}train-m'.format(p)
    with open(f_name, 'r', encoding='utf-8', errors='surrogateescape') as f_train_m:
        f_name='{:}dev.in'.format(p)
        with open(f_name, 'r', encoding='utf-8', errors='surrogateescape') as f_dev_in:
            f_name='{:}{:}-dev.p2.out'.format(p, d)
            with open(f_name, 'w', encoding='utf-8', errors='surrogateescape') as f_dev_out:
                start=timer()
                hmm=HMM(f_train_m, f_dev_in, f_dev_out, d)
                hmm.decode()
                stop=timer()
                print('Runtime: {:}s. '.format(stop-start))
    return

class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('IMPORT|'):
            return text[7:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='NLP: sentiment decoder by... Adeeb Hossain, Goh Zhong Lon Ryan, Loh Haw Yuh', formatter_class=SmartFormatter)
    parser.add_argument('--import', help="IMPORT|To run in a python script...\n"
"\tfrom __name__ import *\n"
"\trun(P, D) # Refer to below for help on P, D\n"
"To add custom decoder module...\n"
"\tadd_decoder_module(name, callable) # callable receives 3 argument: file handler for in.file, out.file and parameter dictionary\n"
"To access parameter dictionary...\n"
"\ttransmission<u, v>=param_dict._t[u][v]\n"
"\temission<v, x>=param_dict._e[v][x]\n")
    requiredNamed=parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-p', type=str, help='folder of data: <SG\\SG\\>', required=True)
    requiredNamed.add_argument('-d', type=str, choices=[name for name in decoder_dict.keys()], help='decoder', required=True)
    parser.add_argument('-v', '--verbosity', action='store_true', default=False)
    args=parser.parse_args()
    p=args.p
    d=args.d
    verbose=args.verbosity

    run(p, d)
