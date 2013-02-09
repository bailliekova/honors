import codecs
import sys

def count_duplicates(infilename):
	uniquetweets=set()
	with codecs.open(infilename, 'r', encoding='utf-8') as infile:
		for i, line in enumerate(infile):
		 	text=line.split('\t')[0]
		 	uniquetweets.add(text)

	duplicates= i-len(uniquetweets)
	print "unique tweets: %s, duplicates: %s" % (len(uniquetweets), duplicates)

if __name__ == '__main__':
	infilename=sys.argv[1]
	count_duplicates(infilename)
