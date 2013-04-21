from __future__ import print_function
import argparse, random, codecs, os, re
import numpy as np
import cPickle as pickle
from time import time
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression 
from sklearn import metrics 
from sklearn.utils.extmath import density

emoticonre=re.compile(r'[;:B=]_?-?[)\(PpD\[\]{}]', re.UNICODE)

def process_tweet(tweet, exclude_emoticons=False):
	tweet=tweet.lower()
	#create regex for anything starting with a www or http(s) and ending at the next whitespace
	urlre=re.compile(r'www\.[\S]+|https?://[\S]+', re.UNICODE)
	tweet=urlre.sub('URL', tweet)
	#replace @handles with the word "USER"
	userre=re.compile(r'@([\S]+)', re.UNICODE)
	tweet=userre.sub('USER', tweet)
	#replace hashtags with the word that was in the hashtag
	hashre=re.compile(r'#([\S]+)', re.UNICODE)
	tweet=hashre.sub(r'\1', tweet)
	#remove punctuation
	tweet=re.sub(r'[^\w\s]+', ' ', tweet, re.UNICODE)
	if exclude_emoticons:
		tweet=emoticonre.sub('', tweet)
	return tweet

def split_set(labeled_set, n, shuffle=True, x=0):
	if shuffle:
		random.shuffle(labeled_set)
	training_set=[(tweet, label) for i, (tweet, label) in enumerate(labeled_set) if i%n!=x]
	test_set=[(tweet, label) for i, (tweet, label) in enumerate(labeled_set) if i%n==x]
	return (training_set, test_set)

def benchmark(clf, x_train, y_train, x_test, y_test):
	print('_' * 80)
	print("Training: ")
	print(clf)
	t0 = time()
	clf.fit(x_train, y_train)
	train_time = time() - t0
	print("train time: %0.3fs" % train_time)

	t0 = time()
	pred = clf.predict(x_test)
	test_time = time() - t0
	print("test time:  %0.3fs" % test_time)

	score = metrics.f1_score(y_test, pred)
	print("f1-score:   %0.3f" % score)

	print("classification report:")
	print(metrics.classification_report(y_test, pred, target_names=['positive', 'negative',]))# 'neutral']))
	print("confusion matrix:")
	conf=metrics.confusion_matrix(y_test,pred)
	print(conf)
	print("accuracy:  %f" % (float(np.sum(conf.diagonal()))/np.sum(conf)))
	return metrics.precision_recall_fscore_support(y_test, pred)


if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('--training_set', '-t', default='undersampled_emoticon.pkl')
	parser.add_argument('--infile', '-i', default='obamatweets.csv')
	parser.add_argument('--mode', '-m', default='v')
	parser.add_argument('--classifier', '-c', default='nb')
	args=parser.parse_args()

	with open(args.training_set, 'rb') as picklefile:
		training_set=pickle.load(picklefile)
	ts=[]
	for tweet, label in training_set:
		if label=='positive':
			ts.append((process_tweet(tweet), 0))
		elif label=='negative':
			ts.append((process_tweet(tweet), 1))
		# elif label=='neutral':
		# 	ts.append((tweet,2))
		else:
			pass


	# n-fold validation
	if args.mode=='v':
		print("10-fold validation...")
		nbresults=[]
		svmresults=[]
		meresults=[]
		for x in xrange(0,10):
			training_set, test_set=split_set(ts, n=10, x=x)
			train_tweets, train_labels=zip(*training_set)
			test_tweets, test_labels=zip(*test_set)
			count_vect=CountVectorizer(charset_error=u'ignore', stop_words='english')
			x_train=count_vect.fit_transform(train_tweets)
			x_test=count_vect.transform(test_tweets)
			categories=['positive', 'negative']	
			nbresults.append(benchmark(BernoulliNB(), x_train, train_labels, x_test, test_labels))
			svmresults.append(benchmark(LinearSVC(), x_train, train_labels, x_test, test_labels))
			meresults.append(benchmark(LogisticRegression(), x_train, train_labels, x_test, test_labels))

	if args.mode=='c':
		"classification...."
		if args.classifier=='nb':
			clf=BernoulliNB()
		elif args.classifier=='svm':
			clf=LinearSVC()
		elif args.classifier=='maxent':
			clf=LogisticRegression()
		x_tweets, y_final= zip(*ts)
		c=CountVectorizer(charset_error=u'ignore', stop_words='english')
		x_final=c.fit_transform(x_tweets)
		clf.fit(x_final, y_final)
		sentiment_dict=defaultdict(lambda: defaultdict(int))
		print('classifying obamatweets.csv...')
		with codecs.open(os.path.join('data', 'obamatweets.csv'), 'r', encoding='utf-8') as infile:
			for line in infile:
				tokens=line.split('\t')
				text=tokens[0]
				try:
					date=tokens[7]
				except IndexError:
					continue
				classification=clf.predict(c.transform(text))[0]
				if classification==1:
					print(text, classification)
				sentiment_dict[date][classification]+=1
		
		print('writing to file...')
		outfile_name=args.classifier+'_'+args.training_set[:-4]+'.csv'
		with open(os.path.join('data', outfile_name), 'w') as outfile:
			outfile.write('\t'.join(['date', 'positive', 'negative', 'ratio\n']))
			for date in sentiment_dict:
				pos=sentiment_dict[date][0]
				neg=sentiment_dict[date][1]
				try:
					ratio=1.0*sentiment_dict[date]['positive']/sentiment_dict[date]['negative']
				except:
					ratio=None
				row=[date, pos, neg, ratio] 
				outfile.write('\t'.join([str(x) for x in row]))
				outfile.write('\n')
				outfile.flush()
