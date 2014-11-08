import naive_bayes as nb
import numpy as np

def naive_bayes():
	print "============================================="
	print "loading spambase polluted data..."
	train_X = np.loadtxt("../dataset/spam_polluted/train_feature.txt")
	train_y = np.loadtxt("../dataset/spam_polluted/train_label.txt")
	test_X = np.loadtxt("../dataset/spam_polluted/test_feature.txt")
	test_y = np.loadtxt("../dataset/spam_polluted/test_label.txt")
	print "============================================="
	train = np.array(np.hstack((train_X,np.matrix(train_y).T)))

	phi,params = nb.naive_bayes_learn(train,nb.TP_GAUSSIAN)
	predicted = nb.naive_bayes_log_prob_diff(test_X,nb.TP_GAUSSIAN,phi,params) > 0
	err = np.sum(np.logical_xor(predicted,test_y))/float(len(test_y))
	print "Accuracy for Naive Bayes Classifier with Gaussian Model : %0.4f" %(1-err)

if __name__ == '__main__':
	naive_bayes()