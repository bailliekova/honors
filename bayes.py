#Bayesian classifier
import codecs
import sys, os, re, random, datetime
import cPickle as pickle
from classifier import *
from nltk import NaiveBayesClassifier, MaxentClassifier
from collections import defaultdict
import argparse


if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('--trainingset', '-t', default='undersampled_emoticon.pkl')
	parser.add_argument('--infile', '-i', default='obamatweets.csv')
	parser.add_argument('--outfile', '-o', default='emoticon_obama_daily.csv')
	parser.add_argument('--validation_set', '-v', default='validation_set_categorical.pkl')
	parser.add_argument('--classifier', '-c', choices=['nb','svm', 'me'], default='nb')
	parser.add_argument('--mode', '-m', choices=['c','v'], default='v')
	args=parser.parse_args()

	print 'initializing new classifier...'
	nbc=Classifier()
	feature_sets=pickle.load(open(args.trainingset, 'rb'))
	print "training model %s" % datetime.datetime.now()

	nbc.train_model(feature_sets)
	
	print 'done training model at %s' % datetime.datetime.now()

	if args.mode=='v':
		print 'validating model'
		validation_set=pickle.load(open(args.validation_set, 'rb'))
		print 'validating against Turk data'
		nbc.validate(validation_set)
		print 'n-fold cross validation'
		nbc.n_fold_validation(args.trainingset)

	if args.mode=='c':
		sentiment_dict=defaultdict(lambda: defaultdict(int))
		print 'classifying obamatweets.csv...'
		with codecs.open(os.path.join('data', args.infile), 'r', encoding='utf-8') as infile:
			lines=infile.readlines()
			for line in lines:
				try:
					print line
				except:
					pass
				tokens=line.split('\t')
				text=tokens[0]
				try:
					date=tokens[7]
				except IndexError:
					continue
				classification=nbc.classify(text)
				sentiment_dict[date][classification]+=1
		
		print 'writing to file... %s ' % datetime.datetime.now()
		with open(os.path.join('data', args.outfile), 'w') as outfile:
			outfile.write('\t'.join(['date', 'positive', 'negative', 'ratio\n']))
			for date in sentiment_dict:
				pos=sentiment_dict[date]['positive']
				neg=sentiment_dict[date]['negative']
				try:
					ratio=1.0*sentiment_dict[date]['positive']/sentiment_dict[date]['negative']
				except:
					ratio=None
				row=[date, pos, neg, ratio] 
				outfile.write('\t'.join([str(x) for x in row]))
				outfile.write('\n')
				outfile.flush()



