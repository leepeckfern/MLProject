"""
Write a function that estimates the emission parameters
from the training set using MLE
"""

# Emission parameters
# count(y -> x)/ count(y)
# emissionParameters takes in tags vector and words sequence	
def emissionParameters(X, Y, x, y):
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

# This function count the total number of y in given tags sequence
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
	unique_tag_Y = unique_Y(Y) # create list of unique tag, Y

	for s in output:
		count = 0

		# max_pro_Y = []
		for w in s:
			potential_Y = [] # create a potential y list
			for i in range(len(unique_tag_Y)):
				a = emissionParameters(X, Y, w, unique_tag_Y[i])
				potential_Y.append(a)
			argmax_Y = unique_tag_Y[potential_Y.index(max(potential_Y))] # the tag with highest possiblity
			output[word_seq.index(s)][s.index(w)] = argmax_Y
		count += 1
		print("%d sentence is done. Still have %d"%(count, len(output) - count))
	print("Completed")

	return output 
#################################PART 3##################################
# transmission parameters
# count(yi-1, yi-1)/ count(yi-1)
# E.g: 'START', 'V'
def transitionParameter(Y, curr_y, next_y):
    # print(curr_y,next_y)
    newY=""
    for y in Y:
         y.insert(0,"START")
         y.insert(len(y)+1, "STOP")
         # a = "START" + ''.join(map(str,y)) + "STOP"
         # newY += a
         # print(newY)
         print(y)
    pattern = curr_y + next_y
    count_yi_minus_one = count_Y(Y,curr_y)
    # print("count_yi_minus_one: "+str(count_yi_minus_one))
    transition_count = countPattern(Y,pattern)
    # print("transition_count: "+str(transition_count))

    return transition_count/count_yi_minus_one

#######################################################################################################

""" Now is the time to implement viterbi """

#######################################################################################################

# Input: state sequence, observation sequence, given observation

# Output: most likely hidden state seq MX = {x1 ,x2,..,xT}


# formula: a(from prev state to next state) * b(X_test)
def joinSeq(Y, curr_y, next_y, X, x, y):
	temp_Y = Y # make a copy of the label list
    for y in temp_Y:
         y.insert(0,"START")
         y.insert(len(y)+1, "STOP")

	for seq in Y:
		for state in seq:



def viterbi(X, Y, X_test):
	newY = unique_Y(Y) # get unique Y
	for seq in Y:
		for state in seq:






"""
Test cases
"""
X = [["see", "me", "cry", "up", "to", "the", "moon"],["cat", "like", "to", "see", "the", "moon"]]
Y = [["V", "N", "V", "P", "D", "D", "N"], ["N", "V", "D", "V", "D", "N"]]
word_seq = [["the", "cat", "cry", "over", "the", "milk"], ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
# print(sentiment_analysis(word_seq, X, Y))

print("transition params: " + str(transitionParameter(Y, 'START', 'V')))
# print("transition params: " + str(transitionParameter(Y, 'N', 'STOP')))
