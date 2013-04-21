import re
from itertools import chain
from nltk import word_tokenize, sent_tokenize, classify, NaiveBayesClassifier, MaxentClassifier
from nltk.classify.util import apply_features
from nltk.corpus import stopwords
from nltk.metrics import ConfusionMatrix, precision, recall, f_measure
import random
from collections import defaultdict, Counter
# classifier shell for processing tweets

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

def recode_turk(turk_set, include_neutral=False):
	validation_set=[]
	for tweet, rating in turk_set:
		if float(rating)>0:
			validation_set.append((tweet, 'positive'))
		elif float(rating)<0:
			validation_set.append((tweet, 'negative'))
		elif include_neutral:
			validation_set.append((tweet, 'neutral'))
		else:
			pass
		return validation_set

class Classifier:
	"""
	Wrapper around nltk.classifier with methods for feature extraction. 
	"""
	def __init__(self, stopws=None):
		if stopws is None:
			self.stopwords=stopwords.words('english')
		else:
			self.stopwords=stopws
		self.stopwords.extend(['USER', 'URL'])
		self.feature_list=[]
		self.classifier=None 
	
	def extract_features(self, text):
		preprocessed=process_tweet(text)
		sents=sent_tokenize(preprocessed)
		wordlists=[word_tokenize(s) for s in sents]
		tokens=set([word for wordlist in wordlists for word in wordlist if word not in self.stopwords])
		features=dict()
		for feature in self.feature_list:
			features['contains(%s)' % feature]= feature in tokens
		return features

	def train_model(self, training_set, classifier=NaiveBayesClassifier, feature_limit=2000):
		feature_counter=Counter(chain.from_iterable([word_tokenize(process_tweet(tweet)) for tweet, sentiment in training_set]))
		for word in self.stopwords:
			del feature_counter[word]
		self.feature_list=[feat for feat, count in feature_counter.most_common(feature_limit)]
		#self.feature_list=[feature for feature in feature_list if feature not in self.stopwords]
		ts=[(self.extract_features(tweet), label) for tweet, label in training_set]
		#ts=apply_features(self.extract_features, training_set)
		self.classifier=classifier.train(ts)

	def classify(self, text):
		"""
		Convenience method, calls self.classifier's classify method, raises an expection if self.classifier not initialized.
		"""
		if self.classifier:
			return self.classifier.classify(self.extract_features(text))
		else:
			raise Exception('Classifier has not been trained!')

	def n_fold_validation(self, training_set, classifier=NaiveBayesClassifier, n=10, seed=None):
		"""
		Performs an n-fold validation of the classifier, returning mean accuracy. 
		Shuffles the trainingset, using option argument seed for replicability. 
		"""
		if seed:
			random.shuffle(training_set, seed)
		else:
			random.shuffle(  training_set)
		statistics=[]
		# alist=[]
		for x in xrange(0, 10):
			print "fold %d" % x
			training_tweets=[tweet_tuple for i, tweet_tuple in enumerate(training_set) if i % n != x]
			validation_tweets=[tweet_tuple for i, tweet_tuple in enumerate(training_set) if i % n == x]
			self.train_model(training_set=training_tweets, classifier=classifier)
			validation_set=[(self.extract_fea tures(tweet), sentiment) for tweet, sentiment in validation_tweets]
			# a=classify.accuracy(self.classifier, validation_set)
			# print "Accuracy: %s" % a
			# print type(a)
			statistics.append(self.validate(validation_tweets))
		# 	alist.append(a)
		# print alist
		# mean_acc=sum(alist)/len(alist)
		# print "Mean Accuracy: %s" % mean_acc
		print "Mean positive precision %s" % sum([stat[1] for stat in statistics])/len(statistics)
		print "Mean positive recall %s" % sum([stat[2] for stat in statistics])/len(statistics)
		print "Mean positive f-measure %s" % sum([stat[3] for stat in statistics])/len(statistics)
		print "Mean negative precision %s" % sum([stat[4] for stat in statistics])/len(statistics)
		print "Mean negative recall %s" % sum([stat[5] for stat in statistics])/len(statistics)
		print "Mean negative f-measure %s" % sum([stat[6] for stat in statistics])/len(statistics)
		return mean_acc

	def validate(self, validation_set):
		if self.classifier is None:
			raise Exception("self.classifier is None")
		reference=defaultdict(set)
		observed=defaultdict(set)
		observed['neutral']=set()

		for i, (tweet, label) in enumerate(validation_set):
			reference[label].add(i)
			observation=self.classify(tweet)
			observed[observation].add(i)
		acc=classify.accuracy(self.classifier, observed)
		posp=precision(reference['positive'],observed['positive'])
		posr=recall(reference['positive'], observed['positive'])
		posf=f_measure(reference['positive'], observed['positive'])
		negp=precision(reference['negative'],observed['negative'])
		negr=recall(reference['negative'], observed['negative'])
		negf=f_measure(reference['negative'], observed['negative'])
		
		print "accuracy: %s" % acc
		print "pos precision: %s" % posp
		print "pos recall: %s" % posr
		print "pos f-measure: %s" % posf
		print "neg precision: %s" % negp
		print "neg recall: %s" % negr
		print "neg f-measure: %s" % negf
		return (acc, posp, posr, posf, negp, negr, negf)

if __name__ == '__main__':
	pass
