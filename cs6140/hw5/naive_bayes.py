"""
Naive Bayes Classifier, Copied from hw3
"""
import numpy as np
import matplotlib.pyplot as plt
#import errorRates as er

TP_BERNOULLI = "Bernoulli"
TP_GAUSSIAN = "Gaussian"
TP_HISTOGRAM = "Histogram"

K_FOLDS = 10
DEFAULT_TAU = 0

plot_legend = []

def naive_bayes_learn(D,c_type,n_bins=4):
	n = D.shape[1]
	X = D[:,:n-1]
	X0 = D[:,:n-1][D[:,n-1]==0]
	X1 = D[:,:n-1][D[:,n-1]==1]
	phi = len(X1)/float(len(D))
	paras = None
	if TP_BERNOULLI == c_type:
		paras = learn_berboulli(X0,X1)
	elif TP_GAUSSIAN == c_type:
		paras = learn_gaussian(X0,X1,X)
	elif TP_HISTOGRAM == c_type:
		paras = learn_histogram(X0,X1,n_bins)
	return phi,paras

def learn_berboulli(X0,X1):
	params = {}
	params[0],params[1] = {},{}
	params[0]["mu"] = np.mean(X0, axis=0)
	params[1]["mu"] = np.mean(X1, axis=0)
	params[0]["prob"] = laplace_prob_boolean(X0,params[0]["mu"])
	params[1]["prob"] = laplace_prob_boolean(X1,params[1]["mu"])
	return params

def learn_gaussian(X0,X1,X):
	params = {}
	params[0],params[1] = {},{}
	params[0]["mu"] = np.mean(X0, axis=0)
	params[1]["mu"] = np.mean(X1, axis=0)
	params[0]["sigma"] = fore_back_variance(X0,X)
	params[1]["sigma"] = fore_back_variance(X1,X)
	return params

def learn_histogram(X0,X1,n_bins):
	predictor = {}
	predictor[0] = histogram_predictor(X0,n_bins)
	predictor[1] = histogram_predictor(X1,n_bins)
	return predictor

def histogram_predictor(X, n_bins):
	predictor = {}
	m = X.shape[1]
	for i in range(m):
		x = X[:,i]
		predictor[i] = {}
		predictor[i]["thres"] = bucket(x,n_bins)
		predictor[i]["probs"] = laplace_prob_bins(x,predictor[i]["thres"])
	return predictor

def laplace_prob_boolean(X,threshold):
	counts = np.ones(len(threshold))
	for x in X:
		counts += x <= threshold
	return counts/float(len(X)+2)

def laplace_prob_bins(x,thres):
	n_bins = len(thres)-1
	counts = np.ones(n_bins)
	for xi in x:
		for i in range(n_bins):
			if xi > thres[i] and xi <= thres[i+1]:
				counts[i] += 1
				break
	return counts/float(len(x)+n_bins)

def fore_back_variance(fX,bX):
	foreground = np.var(fX, axis=0)
	background = np.var(bX, axis=0)
	l = len(bX)/(len(bX)+2.0)
	return l * foreground + (1 - l) * background

def bucket(x,n):
	if n == 2: # Bernoulli?
		return np.array([-np.inf,np.mean(x),np.inf])
	if n == 4:
		return bucket_4(x)
	else:
		return bucket_other(x,n)

def bucket_4(x):
	overall_mean = np.mean(x)
	low_mean = np.mean(x[x[:]<=overall_mean])
	high_mean = np.inf # in case x values are identical
	if len(x[x[:]>overall_mean]) > 0:
		np.mean(x[x[:]>overall_mean])
	return np.array([-np.inf,low_mean,overall_mean,high_mean,np.inf])

def bucket_other(x,n):
	min_x = np.min(x)
	max_x = np.max(x)
	step = (max_x - min_x)/float(n)
	thresholds = np.zeros(n+1)
	thresholds[0] = -np.inf
	thresholds[n] = np.inf
	for i in range(1,n):
		thresholds[i] = i*step+min_x
	return thresholds
"""
Code below for prediction
"""
def naive_bayes_predict(X,c_type,phi,params,tau):
	probs_diff = naive_bayes_log_prob_diff(X,c_type,phi,params)
	return 1*(probs_diff > tau)

def naive_bayes_log_prob_diff(X,c_type,phi,params):
	return np.array([naive_bayes_diff_prob(x,c_type,phi,params) for x in X])

def naive_bayes_diff_prob(x,c_type,phi,params):
	p0 = naive_bayes_prob(x,c_type,params[0]) + np.log(1-phi)
	p1 = naive_bayes_prob(x,c_type,params[1]) + np.log(phi)
	return p1 - p0

def naive_bayes_prob(x,c_type,param):
	log_probs = np.array([])
	if TP_BERNOULLI == c_type:
		log_probs = [bernoulli_log_prob(x[i],param["mu"][i],param["prob"][i]) for i in range(len(x))]
	elif TP_GAUSSIAN == c_type:
		log_probs = [gaussian_log_prob(x[i],param["mu"][i],param["sigma"][i]) for i in range(len(x))]
	elif TP_HISTOGRAM == c_type:
		log_probs = [histogram_log_prob(x[i],param[i]) for i in range(len(x))]
	return sum(log_probs)

def bernoulli_log_prob(x,mu,prob):
	prob_x = prob if x <= mu else (1-prob)
	return np.log(prob_x)

def gaussian_log_prob(x,mu,sigma):
	log_pdf_x = -0.5*np.log(2*np.pi*sigma)-0.5*(x-mu)**2/sigma
	return log_pdf_x if log_pdf_x < 0 else 0 # when pdf > 1 set it to 1

def histogram_log_prob(x,predictor):
	prob = 0
	thres = predictor["thres"]
	probs = predictor["probs"]
	n_bins = len(probs)
	for i in range(n_bins):
		if x > thres[i] and x <= thres[i+1]:
			prob = probs[i]
	return np.log(prob)

def naive_bayes_k_folds(data,c_type,n_bins=4):
	n = data.shape[1]
	err_rates = np.zeros((K_FOLDS,3))
	k_folds = np.array_split(data,K_FOLDS)

	print_type = c_type
	if TP_HISTOGRAM == c_type:
		print_type = "%d-bins %s" %(n_bins,c_type)

	print "============================================="
	print "Naive Bayes Classifier (%s)" %print_type
	print "With %d folds cross-validation..." %K_FOLDS
	for i in range(K_FOLDS):
		print "iteration %d..." %i
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))
		phi,params = naive_bayes_learn(train,c_type,n_bins)
		log_prob_diffs = naive_bayes_log_prob_diff(test[:,:n-1],c_type,phi,params)
		y_test = log_prob_diffs > DEFAULT_TAU
		errors = er.error_rates(y_test,test[:,n-1])
		err_rates[i] = errors
		print errors
		if i == 0:
			plotROC(log_prob_diffs,test[:,n-1],print_type)
		
	print "the average test error rate is:" 
	print np.mean(err_rates,axis=0)
	print "============================================="

def plotROC(log_prob_diffs,labels,print_type):
	taus = np.unique(log_prob_diffs)
	taus = np.append(np.min(log_prob_diffs)-1,taus)

	tprs,fprs = np.zeros(len(taus)),np.zeros(len(taus))
	for i in range(len(taus)):
		y = 1*(log_prob_diffs > taus[i])
		tprs[i],fprs[i] = er.tp_fp_rates(y,labels)
	plt.plot(fprs, tprs)
	auc = naive_bayes_auc(fprs, tprs)
	plot_legend.append("%s (AUC:%f)" %(print_type, auc))

def naive_bayes_auc(xs,ys):
	X = np.vstack((xs,ys))
	X_sort = X[:,np.argsort(X[0])]

	area = 0.0
	for i in range(len(X_sort[0])-1):
		x1,y1 = X_sort[:,i]
		x2,y2 = X_sort[:,i+1]
		area += (x2-x1)*(y1+y2)*0.5

	return area

if __name__ == "__main__":
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	plt.axis([0, 1, 0, 1])
	plt.title("ROC curves for Naive Bayes Classifier")
	plt.ylabel("True Positive Rate")
	plt.xlabel("False Positive Rate")

	naive_bayes_k_folds(spambase,TP_BERNOULLI)
	naive_bayes_k_folds(spambase,TP_GAUSSIAN)
	naive_bayes_k_folds(spambase,TP_HISTOGRAM)
	naive_bayes_k_folds(spambase,TP_HISTOGRAM,9)

	plt.legend(plot_legend, loc='lower right')
	plt.savefig("ROC_Naive_Bayes.png")