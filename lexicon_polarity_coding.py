import csv

neg_words=[]
pos_words=[]
neu_words=[]
both_words=[]

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

outrows=[]
with open('tweets.csv', 'r') as tweetfile:
  for tweetrow in tweetfile:
    outrow=tweetrow
    for word in pos_words:
      if word in text:
        #make a record that the tweet is positive
        outrow.append('true')
        break
    else:
      outrow.append('false')
    for word in neg_words:
      if word in text:
        outrow.append('true')
        break
    else:
      tweetrow.append('true')
    for word in neu_words:
      if word in text:
        outrow.append('true')
        #make a record that tweet is neutral
        break
    else:
      tweetrow.append('false')
    outrows.append(outrow)

with open('codedtweets.csv', 'wb') as csvfile:
  writer=csv.writer(csvfile, delimiter='\t')
  for row in outrows:
    writer.write(row)