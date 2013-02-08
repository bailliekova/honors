import codecs

infile=codecs.open('data/romneytweets.csv', 'r', encoding='utf-8')
outfile=codecs.open('data/romneytweets_culled.csv', 'w', encoding='utf-8')
for line in infile:
	line_1=line.lower()
	tokens=line_1.split('\t')
	if 'romney' or ' mitt 'in tokens[0]:
		outfile.write(line)