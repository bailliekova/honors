import unittest 
import re
from classifier import *

class PreprocessingTest(unittest.TestCase):

	def setUp(self):
		self.tweet='this is a tweet with a http://www.github.com and @mention and a #hashtag'
		self.tweet2='this tweet has a different url format: https://mail.google.com'
		self.tweet3='this tweet has yet another format for urls: I love www.github.com'
		self.tweet_up='THIS TWEET IS IN UPPERCASE'
		self.posre=re.compile(r'[:;B=]-?[\)\]}D]')
		self.negre=re.compile(r'[:;B=]_?-?[\({\[]')

	def test_process_tweets(self):
		self.assertEqual(process_tweet(self.tweet), 'this is a tweet with a URL and USER and a hashtag')
		self.assertEqual(process_tweet(self.tweet2), 'this tweet has a different url format URL')
		self.assertEqual(process_tweet(self.tweet3), 'this tweet has yet another format for urls i love URL')
		self.assertEqual(process_tweet(self.tweet_up), 'this tweet is in uppercase')
	
	def test_regex(self):
		tweet_happy='This tweet has an emoticon :)'
		tweet_happy1='this tweet :) is happy'
		tweet_sad=':( RT things are sad today'
		tweet_no_emoticon='This has a colon: then a )'
		example_tweet='RT @TPO_Hisself: Want to Know Just How Close the Muslim Brotherhood Is to the Obama Admin? http://t.co/ZvBD7FPK'
	 	self.assertTrue(self.posre.search(tweet_happy))
	 	self.assertTrue(self.posre.search(tweet_happy1))
	 	self.assertTrue(self.negre.search(tweet_sad))
	 	self.assertTrue(self.posre.search(tweet_no_emoticon) is None)
	 	self.assertTrue(self.negre.search(tweet_no_emoticon) is None)
	 	self.assertTrue(self.negre.search(example_tweet) is None)

	def test_initialize_classifier(self):
		c=Classifier()
		self.assertTrue(c is not None)
		self.assertTrue(c.stopwords)
		
	def test_extract_features(self):
		raise Exception("Write this test case, loser!")

	def test_NaiveBayes(self):
		raise Exception("Write this test case, loser!")

	def test_MaxEnt(self):
		raise Exception("Write this test case, loser!")

	def test_SVM(self):
		raise Exception("Write this test case, loser!")


if __name__ == '__main__':
		unittest.main()	
