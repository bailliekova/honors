from classifier import Classifier, process_tweet
from nltk import MaxentClassifier, sent_tokenize, word_tokenize
from itertools import chain
from collections import Counter, defaultdict
import cPickle as pickle
import os

def main():
	me=Classifier()
	feature_counter=Counter()
	feature_set=pickle.load(open('validation_set.pkl', 'rb'))
	feature_set_labels=[]
	for tweet, rating in feature_set:
		print rating
		try:
			float(rating)
		except:
			continue
		if float(rating)>0:
			label='positive'
		elif float(rating)<0:
			label='negative'
		else:
			label='neutral'
		feature_set_labels.append((tweet, label))
	feature_list=chain.from_iterable([word_tokenize(process_tweet(tweet)) for tweet, sentiment in feature_set_labels])
	for feat in feature_list:
		feature_counter[feat]+=1
	me.feature_list=[feat for feat, count in feature_counter.most_common(1000)]
	ts=[(me.extract_features(tweet), label) for tweet, label in feature_set]
	print 'training Maxent'
	me.classifier=MaxentClassifier.train(ts)
	return me


if __name__ == '__main__':
	me=main()
	if not os.path.exists('turk_me_classifier.pkl'):
		with open('turk_me_classifier.pkl', 'wb') as picklefile: 
			pickle.dump(me, picklefile)
	
	sentiment_dict=defaultdict(lambda: defaultdict(int))
	print 'classifying obamatweets.csv...'
	outfile=codecs.open('data\turk_maxent_coded.csv', 'w')
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
			classification=me.classify(text)
			outfile.write('\t'.join([tokens[1], classification, '\n']))
			outfile.flush()
			#print classification
			sentiment_dict[date][classification]+=1
	with open('turk_sentiment_me.pkl', 'wb') as picklefile:
		pickle.dump(sentiment_dict, picklefile)

	print 'aggregating into daily statistics...'
	with open('data\emoticon_obama_daily_me.csv', 'w') as outfile:
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
