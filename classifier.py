import re
from itertools import chain
from nltk import word_tokenize, sent_tokenize
import random
from nltk.classify.util import apply_features
from nltk import NaiveBayesClassifier
# classifier shell for processing tweets

emoticonre=re.compile(r'[;:B]-?[)(PpD\[\]){}]', re.UNICODE)

def process_tweet(tweet, exclude_emoticons=False):
	tweet=tweet.lower()
	#create regex for anything starting with a www or http(s) and ending at the next whitespace
	urlre=re.compile(r'www\.[\S]+|https?://[\S]+', re.UNICODE)
	tweet=urlre.sub('URL', tweet)
	userre=re.compile(r'@([\S]+)', re.UNICODE)
	tweet=userre.sub('USER', tweet)
	hashre=re.compile(r'#([\S]+)', re.UNICODE)
	tweet=hashre.sub(r'\1', tweet)
	#remove punctuation
	tweet=re.sub(r'[^\w\s]', '', tweet, re.UNICODE)
	if exclude_emoticons:
		tweet=emoticonre.sub('', tweet)
	return tweet

class Classifier:
	def __init__(self, stopwords=None):
		self.stopwords=stopwords
		self.feature_list=[]
		stopwords.append('USER').append('URL')
		self.classifier=None

	def train_model(self, training_set):
		random.shuffle(training_set)
		feature_list=set(chain([word_tokenize(process_tweet(tweet) for tweet, sentiment in training_set]))			
		self.featurelist=[feature for feature in featurelist if feature not in self.stopwords]
		ts=nltk.classify.util.apply_features(extract_features, training_set)
		self.classifier=NaiveBayesClassifier.train(ts)

	def extract_features(self, text):
		preprocessed=process_tweet(text)
		#word tokenize by sentences, then chane the sentences together into one sequence
		tokens=chain([word_tokenize(s) for s in sent_tokenize(preprocessed)])
		tokens=[t for token in tokens in token not in stopwords]
		features=dict()
		for feature in self.feature_list:
			features['contains(%s)' % feature]= feature in tokens
		return features

	def classify(self, text):
		if self.classifier:
			print self.classifier.classify(extract_features(text))
		else:
			raise Exception('Classifier has not been trained!')

if __name__ == '__main__':
	#read in training set
	with codecs.open(trainingsetfile_name, 'r', encoding='utf-8') as trainingsetfile:
		training_set=[tuple(line[0], line[1]) for line in trainingsetfile]
	NBC=Classifier()
	NBC.train_model(training_set)
	NBC.classify("Obama sucks. #Nobama")
