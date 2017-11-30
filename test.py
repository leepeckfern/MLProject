import read


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
                i[j]="#UNK#"     #############PART 2.2

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
                # print(word)
                words.append(word)


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

#TESTING

X = [["see", "me", "cry", "up", "to", "the", "moon"],["cat", "like", "to", "see", "the", "moon"]]
Y = [["V", "N", "V", "P", "D", "D", "N"], ["N", "V", "D", "V", "D", "N"]]
#word_seq = [["the", "cat", "cry", "over", "the", "milk"]]#, ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
word_seq = list()
readNewX("/home/dily/MLProject/EN/EN/dev.in", word_seq)
#print(emissionfunction(X,Y,"the", "D"))
with open('dev.p2.out','w') as f:
	print >> f, 'Filename:', sentiment_analysis(word_seq, read.word_seq, read.label_seq)

