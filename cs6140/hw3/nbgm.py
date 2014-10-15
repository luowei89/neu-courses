"""
Naive Bayes with Gaussian Mixtures
"""
import numpy as np
import matplotlib.pyplot as plt
import errorRates as er
import emgm
import time

K_FOLDS=10

plot_legend = []

def nbgm(D,num_g):
	n = D.shape[1]
	X = D[:,:n-1]
	X0 = D[:,:n-1][D[:,n-1]==0]
	X1 = D[:,:n-1][D[:,n-1]==1]
	phi = len(X1)/float(len(D))
	params = {}
	params[0],params[1] = [],[]
	for i in range(n-1):
		print "processing feature %d..." %i
		start = time.time()
		params[0].append(emgm.emgm(np.matrix(X0[:,i]).T,num_g))
		params[1].append(emgm.emgm(np.matrix(X1[:,i]).T,num_g))
		print "%f seconds used." %(time.time() - start)
	return phi,params

def nbgm_log_odds(X,phi,params):
	return np.array([nbgm_log_odd(x,phi,params) for x in X])

def nbgm_log_odd(x,phi,params):
	p0 = nbgm_log_prob(x,params[0]) + np.log(1-phi)
	p1 = nbgm_log_prob(x,params[1]) + np.log(phi)
	return p1 - p0

def nbgm_log_prob(x,params):
	log_prob = 0
	for i in range(len(x)):
		log_prob += gaussians_log_pdf(x[i],params[i])
	return log_prob

def gaussians_log_pdf(x,params):
	pi = params['pi']
	mu = np.hstack(np.array(params['mu']))
	sigma = np.hstack(np.vstack(params['sigma']))
	i = np.argmax(pi)
	log_pdf_x = -0.5*np.log(2*np.pi*sigma[i])-0.5*(x-mu[i])**2/sigma[i]
	return log_pdf_x if log_pdf_x < 0 else 0 # when pdf > 1 set it to 1

def plotROC(log_prob_diffs,labels,print_type):
	taus = np.unique(log_prob_diffs)
	taus = np.append(np.min(log_prob_diffs)-1,taus)

	tprs,fprs = np.zeros(len(taus)),np.zeros(len(taus))
	for i in range(len(taus)):
		y = 1*(log_prob_diffs > taus[i])
		tprs[i],fprs[i] = er.tp_fp_rates(y,labels)
	plt.plot(fprs, tprs)
	auc = nbgm_auc(fprs, tprs)
	plot_legend.append("%s (AUC:%f)" %(print_type, auc))

def nbgm_auc(xs,ys):
	X = np.vstack((xs,ys))
	X_sort = X[:,np.argsort(X[0])]
	area = 0.0
	for i in range(len(X_sort[0])-1):
		x1,y1 = X_sort[:,i]
		x2,y2 = X_sort[:,i+1]
		area += (x2-x1)*(y1+y2)*0.5
	return area

def k_folds(spambase,k_gaussians):
	n = spambase.shape[1]
	err_rates = np.zeros(K_FOLDS)
	k_folds = np.array_split(spambase,K_FOLDS)
	print "============================================="
	print "Naive Bayes Classifier with Gaussian Mixtures"
	print "(%d folds cross-validation...)" %K_FOLDS
	for i in range(1):
		print "iteration %d..." %i
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))
		phi,params = nbgm(train,k_gaussians)
		log_odds = nbgm_log_odds(test[:,:n-1],phi,params)
		y_test = log_odds > 0
		err_rates[i] = np.mean((y_test-test[:,n-1])**2)
		print "error rate is: %f" %err_rates[i]
		if i == 0:
			plotROC(log_odds,test[:,n-1],"%d Gaussians" %k_gaussians)
	
	print "the average test error rate is:" 
	print np.mean(err_rates)
	print "============================================="

if __name__ == "__main__":
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	plt.axis([0, 1, 0, 1])
	plt.title("ROC curves for Gaussian Mixtures")
	plt.ylabel("True Positive Rate")
	plt.xlabel("False Positive Rate")

	k_folds(spambase,1)
	k_folds(spambase,2)
	k_folds(spambase,4)
	k_folds(spambase,9)

	plt.legend(plot_legend, loc='lower right')
	plt.savefig("ROC_Gaussian_Mixtures.png")