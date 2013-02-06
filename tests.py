import unittest 
from classifier import *

class PreprocessingTest(unittest.TestCase):

	def setUp(self):
		self.tweet='this is a tweet with a http://www.github.com and @mention and a #hashtag'
		self.tweet2='this tweet has a different url format: https://mail.google.com'
		self.tweet3='this tweet has yet another format for urls: I love www.github.com'

	def test_process_tweets(self):
		raise Exception('write this test')	