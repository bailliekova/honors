#script to validate coding
import cPickle as pickle
import sys
from nltk.metrics import accuracy, ConfusionMatrix, precision, recall, f_measure
from collections import defaultdict
import classifier

if __name__=='__main__':
	validation_pickle=sys.argv[1]
	classifier_pickle=sys.argv[2]
	validation_set=pickle.load(open(validation_pickle, 'rb'))
	c=pickle.load(open(classifier_pickle, 'rb'))
	
	reference=defaultdict(set)
	observed=defaultdict(set)
	for i, (tweet, label) in enumerate(validation_set):
		reference[label].add(i)
		observation=c.classify(tweet)
		observed[observation].add(i)
	
	print "accuracy: %s" % accuracy(observed, reference)
	print "pos precision: %s" % precision(reference['positive'], observed['positive'])
	print "pos recall: %s" % recall(reference['positive'], observed['positive'])
	print "pos f-measure: %s" % f_measure(reference['positive'], observed['positive'])
	print "neg precision: %s" % precision(reference['negative'], observed['negative'])
	print "neg recall: %s" % recall(reference['negative'], observed['negative'])
	print "neg f-measure: %s" % f_measure(reference['negative'], observed['negative'])
	
