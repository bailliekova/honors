#script to grab emoticon data
import codecs
import sys
import re


if __name__ == '__main__':
	infilename=sys.argv[1]
	posre=re.compile(r'[:;B=]-?[\)\]}D]')
	negre=re.compile(r'[:;B=]_?-?[\(\{\[]]')
	trainingset=[]
	with codecs.open(infilename, 'r', encoding='UTF-8') as infile:
		for line in infile:
			text=line.split('\t')[0]
			m=posre.search(text)
			if m:
				trainingset.append((text, 'positive'))
				try:
					print text, 'positive'
				except UnicodeError:
					pass
			m2=negre.search(text)
			if m2:
				trainingset.append((text, 'negative'))
				try:
					print text, 'negative'
				except UnicodeError:
					continue
	print len(trainingset)
		
