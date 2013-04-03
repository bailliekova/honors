from random import choice
import cPickle as pickle
import codecs

tweets=codecs.open("data/obamatweets.csv", encoding='utf-8').readlines()
ids_in_order=[]
turk_obama_file=codecs.open("Obama_turk_sample.csv", 'w', encoding='utf-8')
tweets_seen=set()
lines=0

print "sampling"
while True:
	tweet=choice(tweets)
	tweet=tweet.replace(',', '')
	tokens=tweet.split('\t')
	if len(tokens)==1:
		print tweet
		continue
	ids_in_order.append(tokens[1])
	if tokens[0] not in tweets_seen:
		tweets_seen.add(tokens[0])
		turk_obama_file.write(','.join(tokens))
		turk_obama_file.flush()
		lines+=1
	if lines==6000:
		break
turk_obama_file.close()

print "pickling"
with open("O_ids.pkl", 'wb') as picklefile:
	pickle.dump(ids_in_order, picklefile)


