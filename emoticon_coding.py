#script to grab emoticon data
import codecs
import sys, os, re, random
import cPickle as pickle
from classifier import *
import nltk
from collections import defaultdict

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
	print len(trainingset)
	with open('emoticon_training_set.pkl', 'w') as picklefile:
		pickle.dump(trainingset, picklefile)
	return trainingset

if __name__ == '__main__':

	if os.path.exists("emoticon_nb_classifier.pkl"):
		nbc=pickle.load(open('emoticon_nb_classifier.pkl', 'rb'))
	else:
		print 'initializing new classifier...'
		nbc=Classifier()
		print 'creating labeled set...'
		if os.path.exists("undersampled_emoticon.pkl"):
			feature_sets=pickle.load(open('undersampled_emoticon.pkl'))
		else:
			feature_sets=create_training_set()
		"training model..."
		nbc.train_model(feature_sets)
		with open('emoticon_nb_classifier.pkl', 'wb') as picklefile:
			pickle.dump(nbc, picklefile)
			
	#print "n fold validation..."
	#nbc.n_fold_validation(feature_sets, seed=)
	#print "showing most informative features..."
	#nbc.classifier.show_most_informative_features()
	sentiment_dict=defaultdict(lambda: defaultdict(int))
	infile='data/obamatweets.csv'
	#infile='data/toy.csv'
	print 'classifying obamatweets.csv...'

	with codecs.open(infile, 'r', encoding='utf-8') as infile:
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
			sentiment_dict[date][classification]+=1


	print 'aggregating into daily statistics...'
	with open('data/emoticon_obama_daily.csv', 'w') as outfile:
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

	#nbc.classifier.show_most_informative_features(5)
	#nbc.n_fold_validation(feature_sets, classifier=MaxentClassifier)

