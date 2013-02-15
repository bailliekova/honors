import re
from itertools import chain
from nltk import word_tokenize, sent_tokenize
import random
from nltk.classify.util import apply_features
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier#, MaxentClassifer
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
	tweet=re.sub(r'[^\w\s]', '', tweet, re.UNICODE)
	if exclude_emoticons:
		tweet=emoticonre.sub('', tweet)
	return tweet

class Classifier:
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
		#word tokenize by sentences, then chane the sentences together into one sequence
		tokens=chain([word_tokenize(s) for s in sent_tokenize(preprocessed)])
		tokens=[token for token in tokens if token not in self.stopwords]
		features=dict()
		for feature in self.feature_list:
			features['contains(%s)' % feature]= feature in tokens
		return features

	def train_model(self, training_set):
		random.shuffle(training_set)
		feature_list=set(chain.from_iterable([word_tokenize(process_tweet(tweet)) for tweet, sentiment in training_set]))			
		self.featurelist=[feature for feature in feature_list if feature not in self.stopwords]
		ts=apply_features(self.extract_features, training_set)
		self.classifier=NaiveBayesClassifier.train(ts)

	def classify(self, text):
		if self.classifier:
			return self.classifier.classify(self.extract_features(text))
		else:
			raise Exception('Classifier has not been trained!')

if __name__ == '__main__':
	#read in training set
	#with codecs.open(trainingsetfile_name, 'r', encoding='utf-8') as trainingsetfile:
		#training_set=[tuple(line[0], line[1]) for line in trainingsetfile]
	#NBC=Classifier()
	#NBC.train_model(training_set)
	#print NBC.classify("Obama sucks. #Nobama")
	pass
