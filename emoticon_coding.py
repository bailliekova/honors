#script to grab emoticon data
import codecs
import sys, os, re, random
import cPickle as pickle
from classifier import *
import nltk

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

def 
if __name__ == '__main__':
	print 'initializing new classifier...'
	nbc=Classifier()
	print 'creating labeled set...'
	if os.path.exists("emoticon_training_set.pkl"):
		feature_sets=pickle.load(open('emoticon_training_set.pkl'))
	else:
		feature_sets=create_training_set()

	#nbc.n_fold_validation(feature_sets)
	nbc.train_model(feature_sets)
	sentiment_dict=defaultdict(lambda: defaultdict(int))
	with codecs.open('data\obamatweets.csv', 'r', encoding='utf-8') as infile:
		for line in infile:
			tokens=line.split('\t')
			text=tokens[0]
			try:
	      		date=outrow[7]
	    	except IndexError:
	      		continue 
			classification=nbc.classify(text)
			print classification, text
			sentiment_dict[date][classification]+=1

	with open('data\emoticon_obama_daily.csv', 'w') as outfile:
		outfile.write('\t'.join(['date', 'positive', 'negative', 'ratio\n']))
		for date in sentiment_dict:
			row=[sentiment_dict[date]['positive'], sentiment_dict[date]['negative'], 1.0* sentiment_dict[date]['positive']/sentiment_dict[date]['negative']] 
			outfile.write('\t'.join([str(x) for x in row]))
			outfile.write('\n')
			outfile.flush()
	






	#nbc.classifier.show_most_informative_features(5)
	#nbc.n_fold_validation(feature_sets, classifier=MaxentClassifier)



