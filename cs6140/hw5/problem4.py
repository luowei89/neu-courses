import numpy as np
import naive_bayes as nb

def missing_values(test,train,m_type):
	n = test.shape[1]
	test_X = test[:,:n-1]
	test_y = test[:,n-1]

	phi,params = nb.naive_bayes_learn(train,m_type)
	predicted = nb.naive_bayes_log_prob_diff(test_X,m_type,phi,params) > 0
	acc = np.sum(predicted==test_y)/float(len(test_y))
	print "Naive Bayes Classifier, %s Fit, Accuracy: %f" %(m_type,acc)

if __name__ == '__main__':
	print "============================================="
	print "loading spambase data with missing values..."
	train = np.loadtxt("../dataset/spam_missing_values/20_percent_missing_train.txt",delimiter=",")
	test = np.loadtxt("../dataset/spam_missing_values/20_percent_missing_test.txt",delimiter=",")
	print "============================================="
	np.seterr(invalid="ignore") # ignore np.nan <= threshold, will return False
	missing_values(test,train,nb.TP_GAUSSIAN)
	missing_values(test,train,nb.TP_BERNOULLI)
	missing_values(test,train,nb.TP_HISTOGRAM)