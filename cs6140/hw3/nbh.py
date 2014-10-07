"""
Naive Bayes Model with n-bins histogram
"""
import numpy as np

K = 10

def histogram_learn(D,n_bins):
	n = D.shape[1]
	X = D[:,:n-1]
	X0 = D[:,:n-1][D[:,n-1]==0]
	X1 = D[:,:n-1][D[:,n-1]==1]
	phi = len(X1)/float(len(D))
	predictor = {}
	predictor[0] = histogram_predictor(X0,n_bins)
	predictor[1] = histogram_predictor(X1,n_bins)
	return phi,predictor

def histogram_predictor(X, n_bins):
	predictor = {}
	m = X.shape[1]
	for i in range(m):
		x = X[:,i]
		predictor[i] = {}
		predictor[i]["thres"] = bucket(x,n_bins)
		predictor[i]["probs"] = laplace_prob(x,predictor[i]["thres"])
	return predictor

def laplace_prob(x,thres):
	n_bins = len(thres)-1
	counts = np.ones(n_bins)
	for xi in x:
		for i in range(n_bins):
			if xi > thres[i] and xi <= thres[i+1]:
				counts[i] += 1
				break
	return counts/float(len(x)+n_bins)


def bucket(x,n):
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

def histogram_predict(X,phi,predictor):
	return [histogram_predict_single(x,phi,predictor) for x in X]

def histogram_predict_single(x,phi,predictor):
	p0 = histogram_prob(x,predictor[0]) * (1-phi)
	p1 = histogram_prob(x,predictor[1]) * phi
	return 1 if p1 > p0 else 0

def histogram_prob(x,predictor):
	probs = [caculate_one_prob(x[i],predictor[i]) for i in range(len(x))]
	return np.prod(probs)

def caculate_one_prob(x,predictor):
	thres = predictor["thres"]
	probs = predictor["probs"]
	n_bins = len(probs)
	for i in range(n_bins):
		if x > thres[i] and x <= thres[i+1]:
			return probs[i]
	return 0


def navie_bayes_histogram(spambase,n_bins):
	n = spambase.shape[1]
	train_errs = np.zeros(K)
	errs = np.zeros(K)

	k_folds = np.array_split(spambase,K)

	print "============================================="
	print "naive bayes classifier (histogram %d-bins)" %n_bins
	print "with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))
		phi,predictor = histogram_learn(train,n_bins)
		y_test = histogram_predict(test[:,:n-1],phi,predictor)
		errs[i] = np.mean((y_test-test[:,n-1])**2)
		y_train = histogram_predict(train[:,:n-1],phi,predictor)
		train_errs[i] = np.mean((y_train-train[:,n-1])**2)
		print "train error: %f, test error: %f" %(train_errs[i], errs[i])
	print "the average train error rate is: %f" %np.mean(train_errs)
	print "the average test error rate is: %f" %np.mean(errs)
	print "============================================="

if __name__ == "__main__":
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	navie_bayes_histogram(spambase,4)

	