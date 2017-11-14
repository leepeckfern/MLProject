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
