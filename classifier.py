import re
# classifier shell for processing tweets

def process_tweet(tweet):
	tweet=tweet.lower()
	#create regex for anything starting with a www or http(s) and ending at the next whitespace
	urlre=re.compile(r'www\.[\S]+|https?://[\S]+', re.UNICODE)
	tweet=urlre.sub('URL', tweet)
	userre=re.compile(r'@([\S]+)', re.UNICODE)
	tweet=userre.sub('USER', tweet)
	hashre=re.compile(r'#([\S]+)', re.UNICODE)
	tweet=hashre.sub(r'\1', tweet)
	tweet = tweet.strip('\'"')
	return tweet