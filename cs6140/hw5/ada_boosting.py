"""
Copied and modified from hw4
"""
import time
import numpy as np
import matplotlib.pyplot as plt

K = 10
MAX_T = 300

def weak_learner_optimal(D,distribution):
	optimal_error,optimal_feature,optimal_threshold = 0.5,0,0
	m,d = D.shape
	X = D[:,:d-1]
	labels = D[:,d-1]
	total = len(labels)
	for feat in range(d-1):
		thresholds = np.unique(X[:,feat])
		before_min = np.min(thresholds) - 1
		err = np.sum(distribution[np.logical_xor((X[:,feat] > before_min),labels)])
		if np.abs(0.5-err) > np.abs(0.5-optimal_error):
			optimal_error = err
			optimal_feature = feat
			optimal_threshold = before_min
		for thres in thresholds:
			err = np.sum(distribution[np.logical_xor((X[:,feat] > thres),labels)])
			if np.abs(0.5-err) > np.abs(0.5-optimal_error):
				optimal_error = err
				optimal_feature = feat
				optimal_threshold = thres
	return optimal_feature,optimal_threshold,optimal_error

def ada_predict(X,weighed_weak_learners,threshold=0):
	fx = f_X(X,weighed_weak_learners)
	return ((fx > threshold) - 0.5) * 2

def f_X(X,weighed_weak_learners):
	fx = np.zeros(len(X))
	for alpha,feat,thresh in weighed_weak_learners:
		fx += alpha*2*((X[:,feat] > thresh) - 0.5)
	return fx

def error_rate(y,labels):
	return np.sum(np.logical_xor(y>0,labels))/float(len(y))

def tprs_fprs(X,y,weighed_weak_learners):
	fx = f_X(X,weighed_weak_learners)
	tprs,fprs = [],[]
	threshs = np.unique(fx)
	tpr,fpr = tpr_fpr((fx > np.min(threshs)-1),y)
	tprs.append(tpr)
	fprs.append(fpr)
	for t in threshs:
		tpr,fpr = tpr_fpr((fx > t),y)
		tprs.append(tpr)
		fprs.append(fpr)
	return tprs,fprs

def tpr_fpr(y,labels):
	tp = np.sum(np.logical_and(y,labels))
	fp = np.sum(np.logical_and(y,np.logical_not(labels)))
	p = np.sum(labels)
	n = len(labels) - p
	return 0 if p == 0 else tp/float(p),0 if n == 0 else fp/float(n)

def auc(xs,ys):
	X = np.vstack((xs,ys))
	X_sort = X[:,np.argsort(X[0])]
	area = 0.0
	for i in range(len(X_sort[0])-1):
		x1,y1 = X_sort[:,i]
		x2,y2 = X_sort[:,i+1]
		area += (x2-x1)*(y1+y2)*0.5
	return area

def ada_boosting(D,test):
	m,d = D.shape
	distribution = np.ones(m)/float(m)
	weighed_weak_learners = [] # list of (alpha,feature,threshold)
	train_X = D[:,:d-1]
	train_y = D[:,d-1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	old_auc,old_err = 0,0
	for i in range(MAX_T):
		s = time.time()
		feat,thresh,round_err = weak_learner_optimal(D,distribution)
		alpha = 0.5*np.log((1-round_err)/round_err)
		yhs = -2*((D[:,feat] > thresh) - 0.5)
		distribution = distribution*np.exp(-1*alpha*yhs)
		distribution = distribution/np.sum(distribution)
		weighed_weak_learners.append((alpha,feat,thresh))
		train_err = 0
		train_err = error_rate(ada_predict(train_X,weighed_weak_learners),train_y)
		test_err = error_rate(ada_predict(test_X,weighed_weak_learners),test_y)
		t,f = tprs_fprs(test_X,test_y,weighed_weak_learners)
		test_auc = auc(f,t)
		print "round %d, feat %d, thresh %0.4f, roundErr %0.4f, trainErr %0.4f, testErr %0.4f, auc %0.4f" %(i,feat,thresh,round_err,train_err,test_err,test_auc)
		print "round time %0.4f" %(time.time()-s)
	return weighed_weak_learners

if __name__ == '__main__':
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	print "============================================="
	k_folds = np.array_split(spambase,K)
	i = int(np.random.rand()*K)
	print "================================Optimal Weak Learner======================================="
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	ada_boosting(train,test)
