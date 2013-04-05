#script to validate coding
import cPickle as pickle
import sys
from nltk.metrics import accuracy, ConfusionMatrix, precision, recall, f_measure
from collections import DefaultDict

if __name__=='__main__':
	validation_pickle=sys.argv[1]
	classifier_pickle=sys.arv[2]
	validation_set=pickle.load(open(validation_pickle, 'rb'))
	classifier=pickle.load(open(classifier_pickle, 'rb'))
	
	reference=defaultdict(set)
	observed=defaultdict(set)
	for (tweetid, tweet, label) in validation_set:
		reference[label].add(tweetid)
		observation=classifier.classify(tweet)
		observed[observation].add(tweetid)
	
	print "accuracy: %s" % accuracy(observed, reference)
	print "pos precision: %s" % precision(reference['positive'], observed['positive'])
	print "pos recall: %s" % recall(reference['positive'], observed['positive'])
	print "pos f-measure: %s" % f_measure(reference['positive'], observed['positive'])
        print "neg precision: %s" % precision(reference['negative'], observed['negative'])
        print "neg recall: %s" % recall(reference['negative'], observed['negative'])
        print "neg f-measure: %s" % f_measure(reference['negative'], observed['negative'])
	
