import unittest 
import re
from classifier import process_tweet

class PreprocessingTest(unittest.TestCase):

	def setUp(self):
		self.tweet='this is a tweet with a http://www.github.com and @mention and a #hashtag'
		self.tweet2='this tweet has a different url format: https://mail.google.com'
		self.tweet3='this tweet has yet another format for urls: I love www.github.com'
		self.tweet_up='THIS TWEET IS IN UPPERCASE'
		self.tweet_happy='This tweet has an emoticon :)'
		self.tweet_happy1='this tweet :) is happy'
		self.tweet_sad=':( RT things are sad today'
		self.posre=re.compile(r'[:;B=]-?[\)\]}D]')
		self.negre=re.compile(r'[:;B=]_?-?[\({\[]')

	def test_process_tweets(self):
		self.assertEqual(process_tweet(self.tweet), 'this is a tweet with a URL and USER and a hashtag')
		self.assertEqual(process_tweet(self.tweet2), 'this tweet has a different url format URL')
		self.assertEqual(process_tweet(self.tweet3), 'this tweet has yet another format for urls i love URL')
		self.assertEqual(process_tweet(self.tweet_up), 'this tweet is in uppercase')
	
	def test_regex(self):
	 	self.assertTrue(self.posre.search(self.tweet_happy))
	 	self.assertTrue(self.posre.search(self.tweet_happy1))
	 	self.assertTrue(self.negre.search(self.tweet_sad))
		#raise Exception("Write this test case, loser!")

if __name__ == '__main__':
		unittest.main()	
