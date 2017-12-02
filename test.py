import read as r
import copy
from helper import *
from math import log

###PART2###

# count y that lead to a specific x, PART 2.1
def count_Y2X(X, Y, x, y):
  Y2X = 0
  for i in range(len(X)):
    for j in range(len(X[i])):
      if(Y[i][j] == y and X[i][j] == x):
        Y2X += 1
  return Y2X

def count_Y(Y, y):
  num_Y = 0
  for sub_y in Y:
    num_Y += sub_y.count(y)
  return num_Y




#####PART 2.2
def cleanfunction(X,k=2):
    print(X)
    dic = {}
    
    for i in X:
        for j in i:
            if j in dic.keys():
                dic[j]+=1
            else:
                dic[j]=1
    #print dic


    for i in X:
        for j in range(len(i)):
            if dic[i[j]] < k:
                i[j]="#UNK#"     #############PART 2.2
    print(X)
    return X

def emissionfunction(X, Y, x, y):

    #print X

    # Check if x apper in the training set
    exist = False
    
    for word_seq in X:
        if x in word_seq:
            exist = True
            break
                    
    if(exist == True):
	#print count_Y2X(X,Y,x,y)
	#print count_Y(Y, y)+1
        return float(count_Y2X(X, Y, x, y)/float(count_Y(Y, y)+1))    ##return emission parameter. PART 2.1
    else:
        return 1/(count_Y(Y, y) + 1)

######PART2.3#########


# Implement a simple sentiment analysis system that produce tag
#y* = argmax e(x|y)

## in: word sequences
## out: lists of tag
def getUniqueY(Y):
  a = set(y for i in Y for y in i)
  return list(a)

def countPattern(Y,pattern):
    #print(Y)
    all_Y = ''
    for y in Y:
        # a = "START" + ''.join(map(str,y)) + "STOP"
        # all_Y += a
        all_Y += ''.join(map(str,y))

        # all_Y += 'STOP'
    # print(all_Y)
    return all_Y.count(pattern)

"""This function calculate the probability for
    the emission from each state to the observation"""
def emissionParameters(YX, comX, Y, x, y):
    
    # Check if x apper in the training set
    if x in comX:
        output = emissionXExist(YX, Y, x, y)
    else:
        output = emissionXnotExist(Y, y)
    return output


"""This function join each y and x respectively and form a string"""
def YtoX(X, Y):
    Y2X = []
    count = 0
    # pattern = x + "-->" + y
    for i in range(len(X)):
        for j in range(len(X[i])):
            Y2X.append(Y[i][j] + "-->" + X[i][j])
    
    # count  =Y2X.count(pattern)
    return Y2X

"""This function combine x into a list"""
def combineX(X):
    sq = list()
    for word_seq in X:
        for word in word_seq:
            sq.append(word)
    
    return sq


"""This function generates the potential tag sequence based on
    the emission emissionParameters """
def part2analysis(X, Y, newX):
        a = getUniqueY(Y)
        y2x = YtoX(X, Y)
        com = combineX(X)
        
        
        output = [] # create a var for output list
        unique_tag_Y = a # create list of unique tag, Y
        count = 0
        for s in  newX:
                temp = []
                for w in s:
                        potential_Y = [] # create a potential y list
                        for i in range(len(unique_tag_Y)):
                            potential_Y.append(emissionParameters(y2x, com, Y, w, unique_tag_Y[i]))
                        argmax_Y = unique_tag_Y[potential_Y.index(max(potential_Y))] # the tag with highest possiblity\
                        print("argmax: ",argmax_Y)
                        # output[newX.index(s)][s.index(w)] = argmax_Y
                        temp.append((argmax_Y))
            # print(output)
                count += 1
                output.append((temp))
                print("%d sentence is done. Still have %d"%(count, len(output) - count))
        print("Completed")
                
        return output


######"""This function read testing data"""###############
def readNewX(testdata, newX):
    words = list()
    # labels = list()
    with open(testdata) as infile:
        for line in infile:
            if line == '\n':

                newX.append(words)
                
                words = list()

            else:
                word = line.strip()
                    #print(word)
                words.append(word)
# print(newX)


#####"""This function read testing data"""######FOR WEIRD CHARACTERS########
def readNewXW(testdata, newX):
    words = list()
    # labels = list()
    with open(testdata, encoding='utf8') as infile:
        for line in infile:
            if line == '\n':

                newX.append(words)
                
                words = list()

            else:
                word = line.strip()
                # print(word)
                words.append(word)




##################PART 3
"""Viterbi Algorithm"""
def viterbi(X, Y, newX):
    
    a = getUniqueY(Y) # unique Y tag list
    modi = modifiedY(Y) # Y list with 'START' & 'STOP'
    join = joinY(modi) # join the modified Y tgt to form a list
    y2x = YtoX(X, Y)  # emission list
    com = combineX(X) # combine X to one list
    trans = transTable(Y, a, modi, join)
    lengthOfNewX = len(newX)
    lengthOfUniY = len(a)

    # Initialised the viterbi
    output = {}
    wholeText = []
    subSentences = []
    newSubSentences = []
    maxSeg = []
    text = []

    for i in range(lengthOfNewX): # for each sentence
        print(i, " sentence")
        tupperware = ()
        subSentences = []
        newSubSentences = []
        maxSeg = []
        layer = []
        word = []

        if(len(newX[i]) > 1):
            """This part is from START to layer 1"""
            for j in range(lengthOfUniY):
                
                pattern = ("START", a[j])
                piAxB = 0

                if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][0], a[j]) == 0:
                    piAxB = -10000
                else:
                    piAxB = log(1) + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][0], a[j]))

                word.append(("START", a[j], piAxB)) #[()]
                
            sort = sorted(word, key=lambda x: x[2], reverse=True)
            layer.append(sort) # Here we have the first transition score in order


            print("start layer is done, move on to layer one")
            """this part is from second layer up to last"""
            for k in range(len((newX)[i])-1):
                word = []

                temp = []

                # from first layer
                if k == 0:

                    for n in range(lengthOfUniY):
                        
                        for m in range(len(layer[k])):
                            # print("layer :",layer[k][m])
                            pattern = (layer[k][m][1], a[n]) # index[i][k-1][m][1] = previous node
                            piAxB = 0

                            if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][k+1], a[n]) == 0:
                                piAxB = -10000
                            else:
                                piAxB = layer[k][m][2] + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][k+1], a[n]))

                            word.append((layer[k][m][1], a[n], piAxB))

                        sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form

                        temp.append(sort[0])
                    sort = sorted(temp, key=lambda x: x[2], reverse=True) # one last sort for that layer
                    layer.append(sort)




                else:
                    for n in range(lengthOfUniY):
                        
                        for m in range(len(layer[k])):

                            pattern = (layer[k][m][1], a[n]) # index[i][k-1][m][1] = previous node
                            piAxB = 0

                            if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][k+1], a[n]) == 0:
                                piAxB = -10000
                            else:
                                piAxB = layer[k][m][2] + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][k+1], a[n]))
                            
                            word.append((layer[k][m][1], a[n], piAxB))

                        sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form
                        temp.append(sort[0])
                    sort = sorted(temp, key=lambda x: x[2], reverse=True)
                    layer.append(sort)
                    # text.append(layer)
                    # print("Length of layer: ",len(layer))                 
                
            print("Done with hidden layer")
            """This is from last layer to 'STOP'"""
            word = []
            for j in range(len(layer[-1])):
                
                pattern = (layer[-1][j][1], "STOP")
                piAxB = 0

                if trans[pattern] == 0:
                    piAxB = -10000
                else:
                    piAxB = layer[-1][j][2] * log(trans[pattern])

                word.append((layer[-1][j][1], "STOP", piAxB))
            sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form
            layer.append(list(sort[0]))
            

            path = []
            path.append(layer[-1][0]) # first append the node before 'STOP'

            temp_path = deepcopy(layer)
            temp_path.pop()


            o = len(temp_path)

            while(o > 1):
                # at this stage the output format should be like [[(),(),(),()],[(),(),()],[(),(),()]]
                for j in range(len(temp_path[-1])):

                    re = path[0]

                    if re == temp_path[-1][j][1]:
                        path.insert(0, temp_path[-1][j][0])
                        temp_path.pop()
                        break
                    else:
                        pass

                o -= 1
                output[i+1] = path
                # print(output)
        else:
            """This part is from START to layer 1"""
            for j in range(lengthOfUniY):
                
                pattern = ("START", a[j])
                piAxB = 0

                if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][0], a[j]) == 0:
                    piAxB = -10000
                else:
                    piAxB = log(1) + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][0], a[j]))

                word.append(("START", a[j], piAxB)) #[()]
                
            sort = sorted(word, key=lambda x: x[2], reverse=True)
            layer.append(sort[0][1]) # Here we have the first transition score in order
            output[i+1] = layer
    return output


#TESTING

X = [["see", "me", "cry", "up", "to", "the", "moon"],["cat", "like", "to", "see", "the", "moon"]]
Y = [["V", "N", "V", "P", "D", "D", "N"], ["N", "V", "D", "V", "D", "N"]]
#word_seq = [["the", "cat", "cry", "over", "the", "milk"]]#, ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
word_seq = list()

readW('/Volumes/SOYOUNG/MLProject/EN/EN/train', X, Y)
readNewXW("/Volumes/SOYOUNG/MLProject/EN/EN/dev.in", word_seq)
#print(emissionfunction(X,Y,"the", "D"))
with open('/Volumes/SOYOUNG/MLProject/EN/EN/dev.p2.out','w') as f:
    #print(read.word_seq)
    in_seq = copy.deepcopy(word_seq)
    clean_word_seq=cleanfunction(r.word_seq)
    #print(read.word_seq)
    #w=part2analysis(clean_word_seq, r.label_seq, word_seq)
    #print(word_seq)
    w=viterbi(clean_word_seq, r.label_seq, word_seq)
    
    for s in range(len(in_seq)): #s is a sentence
        print(in_seq[s])

        for ss in range(len(in_seq[s])): #ss is a word inside sentence
#print(word_seq)
            print(in_seq[s][ss], w[s][ss], file=f)
#print('\n')
