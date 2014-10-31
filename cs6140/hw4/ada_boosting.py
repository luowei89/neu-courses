import numpy as np
import matplotlib.pyplot as plt

K = 10
MAX_T = 200

legends = []

def decision_stupms(D):
	stumps = {}
	m,d = D.shape
	X = D[:,:d-1]
	labels = D[:,d-1]
	for feat in range(d-1):
		thresholds = np.unique(X[:,feat])
		before_min = np.min(thresholds) - 1
		stumps[(feat,before_min)] = np.logical_xor((X[:,feat] > before_min),labels)
		for thres in thresholds:
			stumps[(feat,thres)] = np.logical_xor((X[:,feat] > thres),labels)
	return stumps

def weak_learner_optimal(stumps,distribution):
	optimal_error,optimal_feature,optimal_threshold = 0.5,0,0
	for feat,thresh in stumps:
		err = np.sum(distribution[stumps[(feat,thresh)]])
		if np.abs(0.5-err) > np.abs(0.5-optimal_error):
			optimal_error = err
			optimal_feature = feat
			optimal_threshold = thresh
	return optimal_feature,optimal_threshold,optimal_error

def weak_learner_random(stumps,distribution):
	random_i = int(np.random.rand()*len(stumps))
	feat,thresh = stumps.keys()[random_i]
	err = np.sum(distribution[stumps[(feat,thresh)]])
	return feat,thresh,err

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

def plot_ROC(xs,ys,auc,title):
	plt.clf()
	plt.plot(xs, ys)
	plt.axis([0, 1, 0, 1])
	plt.title("ROC curve for AdaBoosting, AUC: %0.4f" %auc)
	plt.ylabel("True Positive Rate")
	plt.xlabel("False Positive Rate")
	plt.savefig("ROC_AdaBoosting_%s.png" %title)

def ada_boosting(D,test,weak_learner_fun=weak_learner_optimal,title="Optimal"):
	m,d = D.shape
	distribution = np.ones(m)/float(m)
	stumps = decision_stupms(D)
	weighed_weak_learners = [] # list of (alpha,feature,threshold)
	train_X = D[:,:d-1]
	train_y = D[:,d-1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	old_auc,old_err = 0,0
	for i in range(MAX_T):
		feat,thresh,round_err = weak_learner_fun(stumps,distribution)
		alpha = 0.5*np.log((1-round_err)/round_err)
		yhs = -2*(stumps[(feat,thresh)] - 0.5)
		distribution = distribution*np.exp(-1*alpha*yhs)
		distribution = distribution/np.sum(distribution)
		weighed_weak_learners.append((alpha,feat,thresh))
		#print "round %d, feat %d, thresh %0.4f, roundErr %0.4f" %(i,feat,thresh,round_err)
		train_err = 0
		train_err = error_rate(ada_predict(train_X,weighed_weak_learners),train_y)
		test_err = error_rate(ada_predict(test_X,weighed_weak_learners),test_y)
		t,f = tprs_fprs(test_X,test_y,weighed_weak_learners)
		test_auc = auc(f,t)
		print "round %d, feat %d, thresh %0.4f, roundErr %0.4f, trainErr %0.4f, testErr %0.4f, auc %0.4f" %(i,feat,thresh,round_err,train_err,test_err,test_auc)
		if test_auc == old_auc and test_err == old_err:
			break # converge
		#if abs(test_auc - old_auc)<1e-4 and abs(test_err - old_err)<1e-4: # loose condition
		if title=="Optimal":
			if abs(round_err-0.5) < 2e-2 or train_err == 0:
				break 
		old_auc,old_err = test_auc,test_err
	#plt.plot(f, t)
	#legends.append("%s, AUC: %0.4f" %(title,test_auc))
	#plot_ROC(f,t,test_auc,title) # for problem 1, won't plot for other problems
	return weighed_weak_learners

if __name__ == '__main__':
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	print "============================================="
	k_folds = np.array_split(spambase,K)
	i = int(np.random.rand()*K)
	plt.clf()
	plt.axis([0, 1, 0, 1])
	plt.title("ROC curves for AdaBoosting")
	plt.ylabel("True Positive Rate")
	plt.xlabel("False Positive Rate")
	print "================================Optimal Weak Learner======================================="
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	ada_boosting(train,test)
	print "================================Random Weak Learner========================================"
	ada_boosting(train,test,weak_learner_random,"Randomly Chosen")
	plt.legend(legends, loc='lower right')
	plt.savefig("p1_roc.png")
