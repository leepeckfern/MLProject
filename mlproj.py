def emissionParametersk(X, Y, x, y, k=2):

    dic = {}

    for i in X:
        for j in i:
            if j in dic.keys():
                dic[j]+=1
            else:
                dic[j]=1
    print dic


    for i in X:
        for j in range(len(i)):
            if dic[i[j]] < k:
                i[j]="#UNK#"

    print X

    # Check if x apper in the training set
    
    exist = False

    for word_seq in X:
        if x in word_seq:
            exist = True
            break


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


#if(exist == True):
#return count_Y2X(X, Y, x, y)/(count_Y(Y, y)+1)
# else:
#return 1/(count_Y(Y, y) + 1)



X = [["see", "me", "cry", "up", "to", "the", "moon"],["cat", "like", "to", "see", "the", "moon"]]
Y = [["V", "N", "V", "P", "D", "D", "N"], ["N", "V", "D", "V", "D", "N"]]

print(emissionParametersk(X,Y,"cry", "N"))