"""
Copied and modified from hw4
"""
import time
import numpy as np
import matplotlib.pyplot as plt

K = 10
MAX_T = 200

def weak_learner_optimal(D,distribution):
	optimal_error,optimal_feature,optimal_threshold = 0.5,0,0
	m,d = D.shape
	X = D[:,:d-1]
	labels = D[:,d-1]
	init_err = sum(distribution[labels==0]) # initially all 0s are errors
	for feat in range(d-1):
		feature_column = X[:,feat]
		sorted_index = feature_column.argsort()
		sorted_labels = labels[sorted_index].astype(bool)
		sorted_feature = feature_column[sorted_index]
		sorted_distribution = distribution[sorted_index]
		thres = sorted_feature[0] - 1
		err = init_err
		for i in range(m):
			if sorted_feature[i] > thres:
				if abs(0.5-err) > abs(0.5-optimal_error):
					optimal_error = err
					optimal_feature = feat
					optimal_threshold = thres
				thres = sorted_feature[i]
			err = err + sorted_distribution[i] if sorted_labels[i] else err - sorted_distribution[i]
		if abs(0.5-err) > abs(0.5-optimal_error):
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

def ada_boosting(D):
	m,d = D.shape
	distribution = np.ones(m)/float(m)
	weighed_weak_learners = [] # list of (alpha,feature,threshold)
	train_X = D[:,:d-1]
	train_y = D[:,d-1]
	for i in range(MAX_T):
		s = time.time()
		feat,thresh,round_err = weak_learner_optimal(D,distribution)
		alpha = 0.5*np.log((1-round_err)/round_err)
		yhs = -2*(np.logical_xor((D[:,feat] > thresh),train_y) - 0.5)
		distribution = distribution*np.exp(-1*alpha*yhs)
		distribution = distribution/np.sum(distribution)
		weighed_weak_learners.append((alpha,feat,thresh))
		print "round %d, feat %d, thresh %0.4f, roundErr %0.4f, time %0.4f" %(i,feat,thresh,round_err,time.time()-s)
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
	ada_boosting(train)
