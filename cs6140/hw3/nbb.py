"""
Naive Bayes Model with Bernoulli (Boolean) random variables
"""
import numpy as np
import errorRates as er

K = 10

def bernoulli_learn(D):
	n = D.shape[1]
	X = D[:,:n-1]
	X0 = D[:,:n-1][D[:,n-1]==0]
	X1 = D[:,:n-1][D[:,n-1]==1]
	phi = len(X1)/float(len(D))
	mu,prob = {},{}
	mu[0] = np.mean(X0, axis=0)
	mu[1] = np.mean(X1, axis=0)
	prob[0] = laplace_prob(X0,mu[0])
	prob[1] = laplace_prob(X1,mu[1])
	return phi,mu,prob

def laplace_prob(X,threshold):
	counts = np.ones(len(threshold))
	for x in X:
		counts += x <= threshold
	return counts/float(len(X)+2)

def bernoulli_pridect(X,phi,thres,prob):
	return [bernoulli_pridect_single(x,phi,thres,prob) for x in X]

def bernoulli_pridect_single(x,phi,thres,prob):
	p0 = bernoulli_prob(x,thres[0],prob[0]) + np.log(1-phi)
	p1 = bernoulli_prob(x,thres[1],prob[1]) + np.log(phi)
	return 1 if p1 > p0 else 0

def bernoulli_prob(x,thres,prob):
	probs = [prob[i] if x[i] <= thres[i] else (1-prob[i]) for i in range(len(x))]
	return sum(np.log(probs)) # log to avoid underflow

if __name__ == "__main__":
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	n = spambase.shape[1]
	err_rates = np.zeros((K,3))
	k_folds = np.array_split(spambase,K)

	print "============================================="
	print "naive bayes classifier with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))

		phi,threshold,prob = bernoulli_learn(train)
		y_test = bernoulli_pridect(test[:,:n-1],phi,threshold,prob)
		errors = er.error_rates(y_test,test[:,n-1])
		err_rates[i] = errors
		print errors
		#print "\\hline"#latex print table
		#print "%d&%f&%f&%f\\\\" %(i+1,errors[0],errors[1],errors[2])#latex print table
		
	print "the average test error rate is:" 
	print np.mean(err_rates,axis=0)
	print "============================================="