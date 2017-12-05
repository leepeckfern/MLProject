from var import *
from numpy import argmax

def simple_decoder(fh_dev_in, fh_dev_out, param):
    for buffer in fh_dev_in.iter_file(Filter.dev.value):
        word=buffer[1][0]
        eol_tag=buffer[1][1]
        if eol_tag=='STOP':
            tag=''
        else:
            tag_prob=max([(i0, i1[word.lower()]) for i0, i1 in param._e.items()], key=lambda x:x[1])
            tag=tag_prob[0]
        fh_dev_out.write('{:} {:}\n'.format(word, tag))
    return

def viterbi_decoder(fh_dev_in, fh_dev_out, param):
    def loop(prev_score, curr_score, word):
        for curr_tag, curr_Tscore in curr_score.items():
            if curr_tag=='STOP':
                e=1
            else:
                e=param._e[curr_tag][word]
            best_Tscore=max([(prev_tag, prev_Tscore[1]*param._t[prev_tag][curr_tag]*e) for prev_tag, prev_Tscore in prev_score.items()], key=lambda x:x[1])
            curr_score[curr_tag]=best_Tscore
        return
    start_score=defaultdict(int, {'START':('', 1.0)})
    stop_score=defaultdict(int, {'STOP':('', 0.0)})
    score_array=deque()
    for buffer in fh_dev_in.iter_file(Filter.dev.value):
        if buffer[0][1]=='START':
            prev_score=start_score
        else:
            prev_score=score_array[-1]
        if buffer[1][1]=='STOP':
            curr_score=stop_score
        else:
            curr_score=defaultdict(int, tag_array)
        word=buffer[1][0].lower()
        loop(prev_score, curr_score, word)
        score_array.append(curr_score)
    tag_seq=deque()
    while score_array:
        score=score_array.pop()
        if score['STOP']:
            tag=score['STOP'][0]
        else:
            tag=score[tag_seq[0]][0]
        tag_seq.appendleft(tag)
    tag_seq.popleft()
    for buffer in fh_dev_in.iter_file(Filter.dev.value):
        word=buffer[1][0]
        try:
            tag=tag_seq.popleft()
        except IndexError:
            break
        if tag=='START':
            fh_dev_out.write('\n')
        else:
            fh_dev_out.write('{:} {:}\n'.format(word, tag))
    return

def max_marginal_decoder(f1,f2_dev_out,param):
    def compute_alpha(i):
        alpha_scores = []
        for buffer in f1.iter_file(Filter.dev.value):
            word = buffer[1][0]
            for u in tag_array:
                for v in tag_array:
                    transprob = param.__t[u][v]
                    emissionprob = param.__e[v][word]
                    if i == 1:
                        alpha_val = 1
                    else:
                        alpha_val = compute_alpha(i-1)*transprob*emissionprob
                alpha_scores.append(alpha_val)
        return alpha_scores
    def compute_beta(i):
        beta_scores = []
        for buffer in f1.iter_file(Filter.dev.value, reverse=True):
            word = buffer[1][0]
            for u in tag_array:
                for v in tag_array:
                    transprob = param.__t[u][v]
                    emissionprob = param.__e[v][word]
                    if i == 1 and (buffer[1][1] == 'STOP'):
                        beta_val = param.__t[u]['STOP']*param.__e[u][word]
                    else:
                        beta_val = compute_beta(i-1)*transprob*emissionprob
                beta_scores.append(beta_val)
        return beta_scores
    opttags = []
    for k in range(1,len(f1)+1,1):
        for u in tag_array:
            totalscore.append((compute_alpha(k).alpha_scores[u])*(compute_beta.beta_scores[u]))
        opttags.append(tag_array[argmax(totalscore)])
    for buffer in f1.iter_file(Filter.dev.value):
        word = buffer[1][0]
        tag = opttags.popleft()
        f2.dev_out.write('{:} {:}\n'.format(word, tag))
    return
















