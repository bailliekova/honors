import codecs
import sys, os, re, random
import cPickle as pickle
from classifier import *
import nltk
from collections import defaultdict

if __name__ == '__main__':
	print 'initializing new classifier...'
	nbc=Classifier()
	feature_set=pickle.load(open('validation_set.pkl', 'rb'))
	fs=[]
	for tweet,rating in feature_set:
		if float(rating)> 0:
			label='positive'
		elif float(rating)<0:
			label='negative'
		else:
			label='neutral'
		fs.append((tweet,label))
	"n fold validation..."
	nbc.n_fold_validation(fs)
	"training model..."
	nbc.train_model(fs)
	print "showing most informative features..."
	nbc.classifier.show_most_informative_features()
	sentiment_dict=defaultdict(lambda: defaultdict(int))
	print 'classifying obamatweets.csv...'

	with codecs.open('data\obamatweets.csv', 'r', encoding='utf-8') as infile:
		for line in infile:
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
			#print classification
			sentiment_dict[date][classification]+=1
	#with open('emoticon_sentiment.pkl', 'wb') as picklefile:
		#pickle.dump(sentiment_dict, picklefile)

	print 'aggregating into daily statistics...'
	with open('data\turk_obama_daily.csv', 'w') as outfile:
		outfile.write('\t'.join(['date', 'positive', 'negative', 'ratio\n']))
		for date in sentiment_dict:
			pos=sentiment_dict[date]['positive']
			neg=sentiment_dict[date]['negative']
			try:
				ratio=1.0*sentiment_dict[date]['positive']/sentiment_dict[date]['negative']
			except:
				ratio=None
			row=[pos, neg, ratio] 
			outfile.write('\t'.join([str(x) for x in row]))
			outfile.write('\n')
			outfile.flush()

	#nbc.classifier.show_most_informative_features(5)
	#nbc.n_fold_validation(feature_sets, classifier=MaxentClassifier)

