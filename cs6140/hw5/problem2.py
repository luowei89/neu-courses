import numpy as np
import naive_bayes as nb
from sklearn.decomposition import PCA

def naive_bayes(train_X,train_y,test_X,test_y):
	train = np.array(np.hstack((train_X,np.matrix(train_y).T)))

	phi,params = nb.naive_bayes_learn(train,nb.TP_GAUSSIAN)
	predicted = nb.naive_bayes_log_prob_diff(test_X,nb.TP_GAUSSIAN,phi,params) > 0
	acc = np.sum(predicted==test_y)/float(len(test_y))
	print "Naive Bayes Classifier, Gaussian Fit, Accuracy: %f" %acc

def pca_naive_bayes(train_X,train_y,test_X,test_y):
	pca = PCA(n_components=120)
	pca_obj = pca.fit(train_X,train_y)
	pca_train_X = pca_obj.transform(train_X)
	pca_test_X = pca_obj.transform(test_X)

	train = np.array(np.hstack((pca_train_X,np.matrix(train_y).T)))

	phi,params = nb.naive_bayes_learn(train,nb.TP_GAUSSIAN)
	predicted = nb.naive_bayes_log_prob_diff(pca_test_X,nb.TP_GAUSSIAN,phi,params) > 0
	acc = np.sum(predicted==test_y)/float(len(test_y))
	print "Naive Bayes Classifier, Gaussian Fit, PCA, Accuracy: %f" %acc

if __name__ == '__main__':
	print "============================================="
	print "loading spambase polluted data..."
	train_X = np.loadtxt("../dataset/spam_polluted/train_feature.txt")
	train_y = np.loadtxt("../dataset/spam_polluted/train_label.txt")
	test_X = np.loadtxt("../dataset/spam_polluted/test_feature.txt")
	test_y = np.loadtxt("../dataset/spam_polluted/test_label.txt")
	print "============================================="
	naive_bayes(train_X,train_y,test_X,test_y)
	pca_naive_bayes(train_X,train_y,test_X,test_y)