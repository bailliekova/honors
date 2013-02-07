import unittest 
from classifier import *

class PreprocessingTest(unittest.TestCase):

	def setUp(self):
		self.tweet='this is a tweet with a http://www.github.com and @mention and a #hashtag'
		self.tweet2='this tweet has a different url format: https://mail.google.com'
		self.tweet3='this tweet has yet another format for urls: I love www.github.com'
		self.tweet4='this tweet is in uppercase'
		
	def test_process_tweets(self):
		self.assertEqual(process_tweet(self.tweet), 'this is a tweet with a URL and USER and a hashtag')
		self.assertEqual(process_tweet(self.tweet2), 'this tweet has a different url format: URL')
		self.assertEqual(process_tweet(self.tweet3), 'this tweet has yet another format for urls: i love URL')
		self.assertEqual(process_tweet(self.tweet4), 'this tweet is in uppercase')

if __name__ == '__main__':
		unittest.main()	