neg_words=[]
pos_words=[]
neu_words=[]

with open('data/subjclueslen1-HLTEMNLP05.tff', 'r') as wordfile:
  for line in wordfile:
    tokens=line.split()
    word=tokens[2].partition('=')[2]
    polarity=tokens[-1].partition('=')[2]
    if polarity=='positive':
      neg_words.append(word)
    elif polarity=='positive':
      pos_words.append(word)
    elif polarity=='neutral':
      neu_words.append(word)
    else:
      print word, polarity


