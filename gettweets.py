import dbutils
import codecs

conn=dbutils.connect()
c=conn.cursor()
keyword=sys.argv[1]
c.execute('SELECT t.text, t.id, t.userid, t.favorites, t.retweet, t.latitude, t.longitude, t.date, t.datetime, i.keyword FROM tweets_index as i JOIN tweets_onepercent_tweets as t ON i.tweetid=t.id WHERE i.keyword=%s and t.date< "2012-11-08" ', keyword)
rs=c.fetchall()

with codecs.open('obamatweets.csv', 'w') as outfile:
	for r in rs:
		outfile.write('\t'.join([unicode(x) for x in r]))
		outfile.flush()
