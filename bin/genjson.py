from collections import defaultdict
import json

d=defaultdict(dict)
with open('data\US_FIPS_Codes.txt', 'r') as infile:
	for line in infile:
		statename, countyname, statefips, countyfips=line.strip().split('\t')
		d[statename][countyname]=countyfips
		d[statename]['statefips']=statefips

with open('US_FIPS_County.JSON', 'wb') as jsonfile:
	json.dump(d, jsonfile, indent=4)