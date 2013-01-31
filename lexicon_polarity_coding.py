import codecs
import sys
import csv
from collections import defaultdict

neg_words=[]
pos_words=[]
neu_words=[]
both_words=[]

tweetfile_name=sys.argv[1]
def make_sentiment_dict():
  return {'positive':0, 'negative':0, 'neutral':0}

sentiment_dict=dict()
#create word lists from .tff file
print "Creating lexicon..."
with open('data/subjclueslen1-HLTEMNLP05.tff', 'r') as wordfile:
  for line in wordfile:
    tokens=line.split()
    word=tokens[2].partition('=')[2]
    polarity=tokens[-1].partition('=')[2]
    if 'neg' in polarity:
      neg_words.append(word)
    elif polarity=='positive':
      pos_words.append(word)
    elif polarity=='neutral':
      neu_words.append(word)
    elif polarity=='both':
      both_words.append(word)
    else:
      print word, polarity

print "Processing tweets..."
outrows=[]
with open(tweetfile_name, 'r') as tweetfile:
  for tweetrow in tweetfile:
    outrow=tweetrow.split('\t')
    text=outrow[0]
    date=outrow[7]
    if date not in sentiment_dict:
      sentiment_dict[date]=make_sentiment_dict()
    for word in pos_words:
      if word in text:
        sentiment_dict[date]['positive']+=1
        outrow.append('true')
        break
    else:
      outrow.append('false')
    for word in neg_words:
      if word in text:
        sentiment_dict[date]['negative']+=1
        outrow.append('true')
        break
    else:
      outrow.append('false')
    for word in neu_words:
      if word in text:
        sentiment_dict[date]['neutral']+=1
        outrow.append('true')
        break
    else:
      outrow.append('false')
    outrows.append(outrow)

#write coded tweets to file.
print "writing coded tweets to file"
outfile_name=infile_name.partition('.')[0]+'_coded.csv'
with codecs.open(outfile_name, 'w', encoding='utf-8') as outfile:
  for row in outrows:
    outfile.write('\t'.join([unicode(x) for x in row]))
    outfile.write('\n')
    outfile.flush()
  
#write daily dictionary to file 

"writing daily summmary file...."
summaryfile_name=infile_name.partition('.')[0]+'_daily.csv'
with open(summaryfile_name, 'wb') as summaryfile:
  csvwriter=csv.writer(summaryfile, delimiter='\t')
  for date in sentiment_dict:
    dailysent=1.0*sentiment_dict[date]['positive']/sentiment_dict[date]['negative']
    row=date, sentiment_dict[date]['positive'], sentiment_dict[date]['negative'], sentiment_dict[date]['neutral'], dailysent
    csvwriter.writerow(row)
