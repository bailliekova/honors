#
from classifier import Classifier, process_tweet
from nltk import MaxentClassifier, sent_tokenize, word_tokenize
from itertools import chain
import cPickle as pickle

def main():
	me=Classifier()
	feature_set=pickle.load(open('undersampled_emoticon.pkl', 'rb'))
	feature_list=chain.from_iterable([word_tokenize(process_tweet(tweet)) for tweet, sentiment in feature_set])
	me.feature_list=list(feature_list)
	ts=[(me.extract_features(tweet), label) for tweet, label in feature_set]
	me.classifier=MaxentClassifier.train(ts, algorithm='CG')
	return me


if __name__ == '__main__':
	me=main()
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
			classification=me.classify(text)
			#print classification
			sentiment_dict[date][classification]+=1
	#with open('emoticon_sentiment.pkl', 'wb') as picklefile:
		#pickle.dump(sentiment_dict, picklefile)

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