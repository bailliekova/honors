#script to grab emoticon data
import codecs
import sys
import os
import re
import cPickle as pickle
from classifier import *

def create_training_set():
	infilename=sys.argv[1]
	posre=re.compile(r'[:;B=]-?[\)\]}D]')
	negre=re.compile(r'[:;B=]_?-?[\(\{\[]')
	trainingset=[]
	with codecs.open(infilename, 'r', encoding='UTF-8') as infile:
		for line in infile:
			text=line.split('\t')[0]
			m=posre.search(text)
			if m:
				trainingset.append((text, 'positive'))
			m2=negre.search(text)
			if m2:
				trainingset.append((text, 'negative'))
			#if m1 or m2:
				# try:
				# 	print text, 'negative'
				# except UnicodeError:
				# 	continue
	print len(trainingset)
	with open('emoticon_training_set.pkl', 'w') as picklefile:
		pickle.dump(trainingset, picklefile)
	return trainingset

if __name__ == '__main__':
	print 'creating training set...'
	if os.path.exists("emoticon_training_set.pkl"):
		training_set=pickle.load(open('emoticon_training_set.pkl'))
	else:
		training_set=create_training_set()
	print 'initializing new classifier...'
	NBC=Classifier()
	print 'training model...'
	NBC.train_model(training_set)
	print 'lets classify something: for example, the tweet "Obama sucks. #Nobama"'
	print NBC.classify("Obama sucks. #Nobama. I hate him. Worst President ever. ")

