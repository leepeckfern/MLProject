import read as r
import copy
from helper import *
from math import log
import numpy as np
from time import sleep

###PART2###

# count y that lead to a specific x, PART 2.1
def count_Y2X(X, Y, x, y):          ##number of emissions
  Y2X = 0
  for i in range(len(X)):
    for j in range(len(X[i])):
      if(Y[i][j] == y and X[i][j] == x):
        Y2X += 1
  return Y2X

def count_Y(Y, y):              ##number of tags.
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
"""
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
"""

######PART2.3#########


# Implement a simple sentiment analysis system that produce tag
#y* = argmax e(x|y)

## in: word sequences
## out: lists of tag
def getUniqueY(Y):          ##all possible tags
  a = set(y for i in Y for y in i)
  return list(a)
'''
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
'''


"""This function generates the potential tag sequence based on
    the emission emissionParameters """
def part2analysis(X, Y, newX):
        a = getUniqueY(Y)    ##all possible tags
        y2x = YtoX(X, Y)
        com = combineX(X)
        
        
        output = [] # create a var for output list
        unique_tag_Y = a # create list of unique tag, Y
        count = 0   #number of sentences done
        for s in  newX:     #s is the sentence
                temp = []       #hold the tags for the sentence
                for w in s:     #w is word
                        potential_Y = [] # create a potential y list
                        
                        for i in range(len(unique_tag_Y)): #iterating through each possible tag
                            potential_Y.append(emissionParameters(y2x, com, Y, w, unique_tag_Y[i])) ##calculate all possible emission parameter and adding it to the list for that word
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

#############################
#Part4

sentence = None
y2x= None
trans = None
a=None
memoA = {}
memoB = {}

def maxmargin(X,Y,newX):
    global sentence
    global y2x
    global trans
    global a
    global memoA
    global memoB
    a = getUniqueY(Y) # unique Y tag list
    modi = modifiedY(Y) # Y list with 'START' & 'STOP'
    join = joinY(modi) # join the modified Y tgt to form a list
    y2x = YtoX2(X, Y)  # emission list
    com = combineX(X) # combine X to one list
    trans = transTable(Y, a, modi, join)
    lengthOfNewX = len(newX)
    lengthOfUniY = len(a)
    
    output={}
    count=1
    for sentence in newX:
        
        optimal_Y_sequence=[]
        for j in range(len(sentence)):
            Ys=[]
            memoA = {}
            memoB = {}
            print("------------------------")
            for possibleY in range(lengthOfUniY):
                #print ((j,possibleY))
                Ys.append(forward(a[possibleY],j+1)*backward(a[possibleY],j+1))
            optimal_Y_sequence.append(a[np.argmax(Ys)])
                #print (Ys)
        #print (optimal_Y_sequence)
        output[count]=optimal_Y_sequence
        count+=1
    print (trans)
    return output
#print (a)
    #print (emissionParameters(y2x,com,Y,'the','O'))
#print (forward('O',1,'I',y2x,com,Y,trans))
#print (backward('O',1,'I',y2x,com,Y,trans))

def transHelper(v,u):
    return trans[(v,u)]

def emissionHelper(j,y):
    return emissionParameters2(y2x,sentence[j-1],y)

def MemoizeA(f):
    global memoA
    #memoA = {}
    def helper(u,j):
        global memoA
        if (u,j) not in memoA:
            memoA[(u,j)] = f(u,j)
            print("memoing","A",u,j)
        #print (f,u,j)
        return memoA[(u,j)]
    return helper

def MemoizeB(f):
    global memoB
    #memoB = {}
    def helper(u,j):
        global memoB
        if (u,j) not in memoB:
            memoB[(u,j)] = f(u,j)
            print("memoing","B",u,j)
        #print (f,u,j)
        return memoB[(u,j)]
    return helper

@MemoizeA
def forward(u,j):#,sentence,y2x,trans,a):
    global trans
    if j <= 1:
        return(trans[('START',u)])
    else:
        sum=0.0
        for v in a:
            sum+=forward(u,j-1)*trans[(v,u)]*emissionParameters2(y2x,sentence[j-1],v)
            
        return sum
@MemoizeB
def backward(u,j):#,sentence,y2x,trans,a):
    global trans
    if j >= len(sentence):
        return(trans[(u,'STOP')]*emissionParameters2(y2x,sentence[j-1],u))
    else:
        sum=0.0
        for v in a:
            sum+=backward(v,j+1)*trans[(u,v)]*emissionParameters2(y2x,sentence[j-1],u)
        return sum



#################################
#Part5
#####################################



def secondOrderTransmission (trainingY):
    trans = {}
    modi = modifiedY(trainingY)
    for sentence in modi:
        sentence.insert(0,'START') ##adding the second start tag
        for word in range(len(sentence)-2):
            tuv = (sentence[word],sentence[word+1],sentence[word+2])
            if tuv in trans:
                trans[tuv] += 1
            else:
                trans[tuv] = 1
            tu = (sentence[word],sentence[word+1])
            if tu in trans:
                trans[tu] += 1
            else:
                trans[tu] = 1
    return trans

def a_tuv(trans,t,u,v):
    if (t,u,v) in trans:
        return float(trans[(t,u,v)])/float(trans[(t,u)])
    else:
        return 0.0

def secondOrderViterbi(X,Y,newX):
    trans2 = secondOrderTransmission(Y)
    emission = YtoX2(X, Y)
    a = getUniqueY(Y)
    allTags = a
    allTags.append('START')
    allTags.append('STOP')
    for t in allTags:
        for u in allTags:
            if (t,u) not in trans2:
                trans2[(t,u)] = 1
            for v in allTags:
                if (t,u,v) not in trans2:
                    trans2[(t,u,v)]=1

    for sentence in newX:
        optimal_Y_sequence=[]
        Pi_1s={}
        Pi_Ks={}
        max_Pi_i_minus1 = 0
        t = None
        u = None
        for i in range(len(sentence)+2):
            if i == 0:
                max_Pi_i_minus1 = 1
            elif i == 1:
                for v in a:
                    for u in a:
                        Pi_Ks[i,u,v] = (0, None)
                    # print(a_tuv(trans2,'START','START',v),emissionParameters2(emission,sentence[i-1],v))
                    Pi_Ks[i,'START',v] = (a_tuv(trans2,'START','START',v)*emissionParameters2(emission,sentence[i-1],v),'START')
                    # print (Pi_Ks[i,'START',v])
            elif i == (len(sentence)+1):
                for u in a:
                    maxT = 0
                    argmaxT = None
                    for t in a:
                        value = Pi_Ks[i-1,t,u][0]*a_tuv(trans2,t,u,'STOP')
                        if value > maxT:
                            maxT = value
                            argmaxT = t
                    Pi_Ks[i,u,'STOP'] = (maxT,argmaxT)
            else:
                for v in a:
                    for u in a:
                        maxT = -1
                        argmaxT = None
                        for t in a:
                            print(Pi_Ks[(i-1,t,u)])
                            value = float(Pi_Ks[(i-1,t,u)][0]) * a_tuv(trans2,t,u,v)*emissionParameters2(emission,sentence[i-1],v)
                            Pi_Ks[i,u,v]=(value, None)
                            if value > maxT:
                                maxT = value
                                argmaxT = t
                    Pi_Ks[i,u,v] = (maxT,argmaxT)
            for key in Pi_Ks:
                if key[0] == i:
                    print(key,Pi_Ks[key])
            sleep(2)
        return None










# def viterbiImproved(X, Y, newX):
    
#     a = getUniqueY(Y) # unique Y tag list
#     modi = modifiedY(Y) # Y list with 'START' & 'STOP'
#     join = joinY(modi) # join the modified Y tgt to form a list
#     y2x = YtoX(X, Y)  # emission list
#     com = combineX(X) # combine X to one list
#     trans = transTable(Y, a, modi, join)
#     lengthOfNewX = len(newX)
#     lengthOfUniY = len(a)

#     # Initialised the viterbi
#     output = {}
#     wholeText = []
#     subSentences = []
#     newSubSentences = []
#     maxSeg = []
#     text = []

#     for i in range(lengthOfNewX): # for each sentence
#         print(i, " sentence")
#         tupperware = ()
#         subSentences = []
#         newSubSentences = []
#         maxSeg = []
#         layer = []
#         word = []

#         if(len(newX[i]) > 1):
#             """This part is from START to layer 1"""
#             for j in range(lengthOfUniY):
                
#                 pattern = ("START", a[j])
#                 piAxB = 0

#                 if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][0], a[j]) == 0:
#                     piAxB = -10000
#                 else:
#                     piAxB = log(1) + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][0], a[j]))

#                 word.append(("START", a[j], piAxB)) #[()]
                
#             sort = sorted(word, key=lambda x: x[2], reverse=True)
#             layer.append(sort) # Here we have the first transition score in order


#             print("start layer is done, move on to layer one")
#             """this part is from second layer up to last"""
#             for k in range(len((newX)[i])-1):
#                 word = []

#                 temp = []

#                 # from first layer
#                 if k == 0:

#                     for n in range(lengthOfUniY):
                        
#                         for m in range(len(layer[k])):
#                             # print("layer :",layer[k][m])
#                             pattern = (layer[k][m][1], a[n]) # index[i][k-1][m][1] = previous node
#                             piAxB = 0

#                             if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][k+1], a[n]) == 0:
#                                 piAxB = -10000
#                             else:
#                                 piAxB = layer[k][m][2] + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][k+1], a[n]))

#                             word.append((layer[k][m][1], a[n], piAxB))

#                         sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form

#                         temp.append(sort[0])
#                     sort = sorted(temp, key=lambda x: x[2], reverse=True) # one last sort for that layer
#                     layer.append(sort)




#                 else:
#                     for n in range(lengthOfUniY):
                        
#                         for m in range(len(layer[k])):

#                             pattern = (layer[k][m][1], a[n]) # index[i][k-1][m][1] = previous node
#                             piAxB = 0

#                             if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][k+1], a[n]) == 0:
#                                 piAxB = -10000
#                             else:
#                                 piAxB = layer[k][m][2] + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][k+1], a[n]))
                            
#                             word.append((layer[k][m][1], a[n], piAxB))

#                         sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form
#                         temp.append(sort[0])
#                     sort = sorted(temp, key=lambda x: x[2], reverse=True)
#                     layer.append(sort)
#                     # text.append(layer)
#                     # print("Length of layer: ",len(layer))                 
                
#             print("Done with hidden layer")
#             """This is from last layer to 'STOP'"""
#             word = []
#             for j in range(len(layer[-1])):
                
#                 pattern = (layer[-1][j][1], "STOP")
#                 piAxB = 0

#                 if trans[pattern] == 0:
#                     piAxB = -10000
#                 else:
#                     piAxB = layer[-1][j][2] * log(trans[pattern])

#                 word.append((layer[-1][j][1], "STOP", piAxB))
#             sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form
#             layer.append(list(sort[0]))
            

#             path = []
#             path.append(layer[-1][0]) # first append the node before 'STOP'

#             temp_path = deepcopy(layer)
#             temp_path.pop()


#             o = len(temp_path)

#             while(o > 1):
#                 # at this stage the output format should be like [[(),(),(),()],[(),(),()],[(),(),()]]
#                 for j in range(len(temp_path[-1])):

#                     re = path[0]

#                     if re == temp_path[-1][j][1]:
#                         path.insert(0, temp_path[-1][j][0])
#                         temp_path.pop()
#                         break
#                     else:
#                         pass

#                 o -= 1
#                 output[i+1] = path
#                 # print(output)
#         else:
#             """This part is from START to layer 1"""
#             for j in range(lengthOfUniY):
                
#                 pattern = ("START", a[j])
#                 piAxB = 0

#                 if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][0], a[j]) == 0:
#                     piAxB = -10000
#                 else:
#                     piAxB = log(1) + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][0], a[j]))

#                 word.append(("START", a[j], piAxB)) #[()]
                
#             sort = sorted(word, key=lambda x: x[2], reverse=True)
#             layer.append(sort[0][1]) # Here we have the first transition score in order
#             output[i+1] = layer
#     return output

# def viterbi2(X, Y, newX):
    
#     a = getUniqueY(Y) # unique Y tag list
#     modi = modifiedY(Y) # Y list with 'START' & 'STOP'
#     join = joinY(modi) # join the modified Y tgt to form a list
#     y2x = YtoX(X, Y)  # emission list
#     com = combineX(X) # combine X to one list
#     trans = transTable(Y, a, modi, join)
#     lengthOfNewX = len(newX)
#     lengthOfUniY = len(a)

#     # Initialised the viterbi
#     output = {}
#     wholeText = []
#     subSentences = []
#     newSubSentences = []
#     maxSeg = []
#     text = []

#     for i in range(lengthOfNewX): # for each sentence
#         print(i, " sentence")
#         tupperware = ()
#         subSentences = []
#         newSubSentences = []
#         maxSeg = []
#         layer = []
#         word = []

#         if(len(newX[i]) > 1):
#             """This part is from START to layer 1"""
#             for j in range(lengthOfUniY):
                
#                 pattern = ("START", a[j])
#                 piAxB = 0

#                 if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][0], a[j]) == 0:
#                     piAxB = -10000
#                 else:
#                     piAxB = log(1) + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][0], a[j]))

#                 word.append(("START", a[j], piAxB)) #[()]
                
#             sort = sorted(word, key=lambda x: x[2], reverse=True)
#             layer.append(sort) # Here we have the first transition score in order


#             print("start layer is done, move on to layer one")
#             """this part is from second layer up to last"""
#             for k in range(len((newX)[i])-1):
#                 word = []

#                 temp = []

#                 # from first layer
#                 if k == 0:

#                     for n in range(lengthOfUniY):
                        
#                         for m in range(len(layer[k])):
#                             # print("layer :",layer[k][m])
#                             pattern = (layer[k][m][1], a[n]) # index[i][k-1][m][1] = previous node
#                             piAxB = 0

#                             if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][k+1], a[n]) == 0:
#                                 piAxB = -10000
#                             else:
#                                 piAxB = layer[k][m][2] + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][k+1], a[n]))

#                             word.append((layer[k][m][1], a[n], piAxB))

#                         sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form

#                         temp.append(sort[0])
#                     sort = sorted(temp, key=lambda x: x[2], reverse=True) # one last sort for that layer
#                     layer.append(sort)




#                 else:
#                     for n in range(lengthOfUniY):
                        
#                         for m in range(len(layer[k])):

#                             pattern = (layer[k][m][1], a[n]) # index[i][k-1][m][1] = previous node
#                             piAxB = 0

#                             if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][k+1], a[n]) == 0:
#                                 piAxB = -10000
#                             else:
#                                 piAxB = layer[k][m][2] + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][k+1], a[n]))
                            
#                             word.append((layer[k][m][1], a[n], piAxB))

#                         sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form
#                         temp.append(sort[0])
#                     sort = sorted(temp, key=lambda x: x[2], reverse=True)
#                     layer.append(sort)
#                     # text.append(layer)
#                     # print("Length of layer: ",len(layer))                 
                
#             print("Done with hidden layer")
#             """This is from last layer to 'STOP'"""
#             word = []
#             for j in range(len(layer[-1])):
                
#                 pattern = (layer[-1][j][1], "STOP")
#                 piAxB = 0

#                 if trans[pattern] == 0:
#                     piAxB = -10000
#                 else:
#                     piAxB = layer[-1][j][2] * log(trans[pattern])

#                 word.append((layer[-1][j][1], "STOP", piAxB))
#             sort = sorted(word, key=lambda x: x[2], reverse=True) # [(), (), ()] in sorted form
#             layer.append(list(sort[0]))
            

#             path = []
#             path.append(layer[-1][0]) # first append the node before 'STOP'

#             temp_path = deepcopy(layer)
#             temp_path.pop()


#             o = len(temp_path)

#             while(o > 1):
#                 # at this stage the output format should be like [[(),(),(),()],[(),(),()],[(),(),()]]
#                 for j in range(len(temp_path[-1])):

#                     re = path[0]

#                     if re == temp_path[-1][j][1]:
#                         path.insert(0, temp_path[-1][j][0])
#                         temp_path.pop()
#                         break
#                     else:
#                         pass

#                 o -= 1
#                 output[i+1] = path
#                 # print(output)
#         else:
#             """This part is from START to layer 1"""
#             for j in range(lengthOfUniY):
                
#                 pattern = ("START", a[j])
#                 piAxB = 0

#                 if trans[pattern] == 0 or emissionParameters(y2x, com, Y, newX[i][0], a[j]) == 0:
#                     piAxB = -10000
#                 else:
#                     piAxB = log(1) + log(trans[pattern]) + log(emissionParameters(y2x, com, Y, newX[i][0], a[j]))

#                 word.append(("START", a[j], piAxB)) #[()]
                
#             sort = sorted(word, key=lambda x: x[2], reverse=True)
#             layer.append(sort[0][1]) # Here we have the first transition score in order
#             output[i+1] = layer
#     return output

#TESTING

X = [["see", "me", "cry", "up", "to", "the", "moon"],["cat", "like", "to", "see", "the", "moon"]]
Y = [["V", "N", "V", "P", "D", "D", "N"], ["N", "V", "D", "V", "D", "N"]]
#word_seq = [["the", "cat", "cry", "over", "the", "milk"]]#, ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
word_seq = list()

readW('/Volumes/SOYOUNG/MLProject/CN/CN/train', X, Y)
readNewXW("/Volumes/SOYOUNG/MLProject/CN/CN/dev.in", word_seq)
#print(emissionfunction(X,Y,"the", "D"))
              
'''
#part2
with open('/Volumes/SOYOUNG/MLProject/CN/CN/dev.p2.out','w') as f:
    in_seq = copy.deepcopy(word_seq)
    clean_word_seq=cleanfunction(r.word_seq)
              
    w=part2analysis(clean_word_seq, r.label_seq, word_seq)
    for s in range(len(in_seq)): #s is a sentence
        for ss in range(len(in_seq[s])): #ss is a word inside sentence
            print(in_seq[s][ss], w[s][ss], file=f)    #part2
        print('',file = f)

#part 3

with open('/Volumes/SOYOUNG/MLProject/CN/CN/dev.p3.out','w') as f:
    in_seq = copy.deepcopy(word_seq)
    clean_word_seq=cleanfunction(r.word_seq)
    w=viterbi(clean_word_seq, r.label_seq, word_seq)
    
    for s in range(len(in_seq)): #s is a sentence
        for ss in range(len(in_seq[s])): #ss is a word inside sentence
            print(in_seq[s][ss], w[s+1][ss], file=f)    #part3
        print('',file = f)

#part 4
with open('/Volumes/SOYOUNG/MLProject/CN/CN/dev.p4.out','w') as f:
    in_seq = copy.deepcopy(word_seq)
    clean_word_seq=cleanfunction(r.word_seq)
    #word_seq=[['-','I'],[ 'will', 'never', 'forget'],[ 'the', 'amazing', 'meal'],[ 'service', ',', 'and', 'ambiance'],['I', 'experience', 'at', 'this', 'restaurant', '.']]
    w=maxmargin(clean_word_seq, r.label_seq, word_seq)
    for s in range(len(in_seq)): #s is a sentence
        for ss in range(len(in_seq[s])): #ss is a word inside sentence
            print(in_seq[s][ss], w[s+1][ss], file=f)    #part4
        print('',file = f)
'''

#print(np.argmax([8,8,8,778]))
#out= YtoX2(clean_word_seq,r.label_seq)
#   print(out)



trans2 =(secondOrderTransmission(r.label_seq))
print (trans2.keys())
a = getUniqueY(r.label_seq)
for t in a:
    for u in a:
        for v in a:
            if (t,u,v) in trans2:
                print(t,u,v)
print (a_tuv(trans2,'START','START','O'))
# sleep(3)



#part5
with open('/Volumes/SOYOUNG/MLProject/EN/EN/dev.p5.out','w') as f:
    in_seq = copy.deepcopy(word_seq)
    clean_word_seq=cleanfunction(r.word_seq)
    # w=viterbi2(clean_word_seq, r.label_seq, word_seq)
    w=secondOrderViterbi(clean_word_seq, r.label_seq, word_seq)
    
    for s in range(len(in_seq)): #s is a sentence
        for ss in range(len(in_seq[s])): #ss is a word inside sentence
            print(in_seq[s][ss], w[s+1][ss], file=f)    #part5
        print('',file = f)

