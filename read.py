# -*- coding: utf-8 -*-

# Reading input file: dev.in
import sys

file_location = sys.argv[1]
words = list()
labels = list()
word_seq = list()
label_seq = list()


"""The following read file method allow us to get file input and store each sentence into 
a sublist"""

def read(file, word_seq, label_seq):
	words = list()
	labels = list()
	with open(file) as infile:
		for line in infile:
			if line == '\n':
				# print(line)
				word_seq.append(words)
				label_seq.append(labels)
				words = list()
				labels = list()
			else:
				word, label = line.strip().split(' ')
				print(word)
				words.append(word)
				labels.append(label)
				# print(line)
read(file_location, word_seq, label_seq)

print(word_seq)
print(label_seq)


#####################################################################
"""write file function"""
