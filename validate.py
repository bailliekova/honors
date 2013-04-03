#script to validate coding
import codecs
import sys

infile_name=sys.argv[1]
validate_name=sys.argv[2]

for line in codecs.open(validate_name, 'r', encoding='utf-8'): 
	tokens=line.split(',')
	tweetid=tokens[1]
	text=tokens[0]
	rating=tokens[x]

for line in codecs.open(infile_name, 'r', encoding='utf-8'):
	tokens=line.split('/t')
	