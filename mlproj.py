
#import read

from copy import deepcopy

##PART 2 number 1,2,3
def emissionfunction(X, Y, x, y, k=2):

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
                i[j]="#UNK#"

    #print X

    # Check if x apper in the training set
    exist = False
    
    for word_seq in X:
        if x in word_seq:
            exist = True
            break
                    
    if(exist == True):
        return count_Y2X(X, Y, x, y)/(count_Y(Y, y)+1)
    else:
        return 1/(count_Y(Y, y) + 1)

def count_Y(Y, y):
  num_Y = 0
  for sub_y in Y:
    num_Y += sub_y.count(y)
  return num_Y


# count y that lead to a specific x
def count_Y2X(X, Y, x, y):
  Y2X = 0
  for i in range(len(X)):
    for j in range(len(X[i])):
      if(Y[i][j] == y and X[i][j] == x):
        Y2X += 1
  return Y2X

#############################END OF PART 2##################################
def getUniqueY(Y):
  a = set(y for i in Y for y in i)
  return list(a)


def countPattern(Y,pattern):
    print(Y)
    all_Y = ''
    for y in Y:
        # a = "START" + ''.join(map(str,y)) + "STOP"
        # all_Y += a
        all_Y += ''.join(map(str,y))

        # all_Y += 'STOP'
    # print(all_Y)
    return all_Y.count(pattern)



# Implement a simple sentiment analysis system that produce tag
#y* = argmax e(x|y)

## in: word sequences
## out: lists of tag

def sentiment_analysis(word_seq, X, Y):
    output = word_seq # create a var for output list
    unique_tag_Y = getUniqueY(Y) # create list of unique tag, Y
        
    for s in output:
        count = 0
            
        # max_pro_Y = []
        for w in s:
            potential_Y = [] # create a potential y list
            for i in range(len(unique_tag_Y)):
                a = emissionfunction(X, Y, w, unique_tag_Y[i])
                potential_Y.append(a)
            argmax_Y = unique_tag_Y[potential_Y.index(max(potential_Y))] # the tag with highest possiblity            
            output[word_seq.index(s)][s.index(w)] = argmax_Y
        count += 1
        print("%d sentence is done. Still have %d"%(count, len(output) - count))
    print("Completed")
    
    return output
    


#if(exist == True):
#return count_Y2X(X, Y, x, y)/(count_Y(Y, y)+1)
# else:
#return 1/(count_Y(Y, y) + 1)


#PART 3

def emissionXExist(YX, Y, x, y):
    # if(countY2X(YX, x, y) == 0):
    #     return 0
    # else:
    return countY2X(YX, x, y)/(countY(Y, y))

def emissionXnotExist(Y, y):
    return 1/(countY(Y, y) + 1)


def emissionParameters(YX, comX, Y, x, y):

    # Check if x apper in the training set
    if checkNewXinX(comX, x) == True:
        output = emissionXExist(YX, Y, x, y)
    else:
        output = emissionXnotExist(Y, y)
    return output
"""This function count the total # of y in a tag sequence"""
def countY(Y, y):
    num_Y = 0
    for sub_y in Y:
        num_Y += sub_y.count(y)
    return num_Y

"""This function check if the new x appear in the training X set"""
def checkNewXinX(X, x):
    if x in combineX(X):
        return True
    else:
        return False
# transmission parameters
# count(yi-1, yi-1)/ count(yi-1)
# E.g: 'START', 'V'
def transitionParameter(Y, prev_y, current_y, modi, join):
    
    # probability of transition that we want to get
    transition = prev_y + "-->" +current_y

    # A modified Y sequence with 'START' & 'STOP' state added
    newY = modi
  
    # get the total number of prev Y
    count_prevY = countY(newY,prev_y)
    # print(count_prevY)

    # get the number of transition count Yi-1 -> Yi
    transition_count = join.count(transition)
    # print(transition_count)
    

    return transition_count/count_prevY


"""This function adds 'START' and 'STOP to the Y sequence"""
def modifiedY(Y):
    temp = deepcopy(Y)
    
    for i in range(len(Y)):
        temp[i].insert(0, "START")
        temp[i].insert(len(temp[i]) + 1, "STOP")

    return temp

def joinY(newY):
    sq = []

    for y in newY:
        # print(y)
        for t in range(len(y)-1):
        	sq.append(y[t]+"-->"+y[t+1])
    return sq

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

def combineX(X):
    sq = list()
    for word_seq in X:
        for word in word_seq:
            sq.append(word)
    
    return sq

"""This function will form a transition params table"""
def transTable(Y, uniY, modi, join):
    """TODO:
        Add 'START' & 'STOP' for the 2 unique Y seq
        and form a probability table"""
    

    # unique Y sequence at y-axis
    uniY_vertical = deepcopy(uniY)
    uniY_vertical.insert(0, "START") 

    # unique X sequence at x-axis
    uniY_horizontal = deepcopy(uniY)
    uniY_horizontal.insert(len(uniY_vertical) + 1, "STOP")

    # A dict to store the state(i-1, i) mapped with prob
    prob_dict = {}

    for prev_state in uniY_vertical:

        for current_state in uniY_horizontal:
            state = (prev_state, current_state)
            # print(state)
            prob_dict[state] = transitionParameter(Y, prev_state, current_state, modi, join) 
            

    
    return prob_dict








#######################################################################################################

""" Now is the time to implement viterbi """

#######################################################################################################

# Input: state sequence, observation sequence, given observation

# Output: most likely hidden state seq MX = {x1 ,x2,..,xT}


# formula: a(from prev state to next state) * b(X_test)




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
word_seq = [["the", "cat", "cry", "over", "the", "milk"]]#, ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
#print(emissionfunction(X,Y,"cry", "N"))
#print(sentiment_analysis(word_seq, read.word_seq, read.label_seq))
print(viterbi(X,Y,word_seq))
