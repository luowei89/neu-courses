"""
Gaussian Discriminant Analysis
"""
import numpy as np

K = 10

def gda_learn(D):
	n = D.shape[1]
	X = D[:,:n-1]
	X0 = D[:,:n-1][D[:,n-1]==0]
	X1 = D[:,:n-1][D[:,n-1]==1]
	phi = len(X1)/float(len(D))
	mu0 = np.mean(X0, axis=0)
	mu1 = np.mean(X1, axis=0)
	cov_m = np.cov(X.T)
	return phi,mu0,mu1,cov_m

def gda_pridect(X,mu0,mu1,cov_m):
	m_det = np.linalg.det(cov_m)
	m_inv = np.linalg.pinv(cov_m)
	return [gda_pridect_single(x,mu0,mu1,m_det,m_inv) for x in X]

def gda_pridect_single(x,mu0,mu1,m_det,m_inv):
	p0 = prob(x,mu0,m_det,m_inv)
	p1 = prob(x,mu1,m_det,m_inv)
	return 1 if p1 > p0 else 0

def prob(x,mu,m_det,m_inv):
	diff_m = np.matrix(x-mu)
	return np.exp(-0.5*np.dot(np.dot(diff_m,m_inv),diff_m.T))/np.sqrt(2*np.pi*m_det)

if __name__ == "__main__":
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	n = spambase.shape[1]
	train_errs = np.zeros(K)
	errs = np.zeros(K)

	k_folds = np.array_split(spambase,K)

	print "============================================="
	print "running gda with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))

		phi,mu0,mu1,cov_m = gda_learn(train)
		y_test = gda_pridect(test[:,:n-1],mu0,mu1,cov_m)
		errs[i] = np.mean((y_test-test[:,n-1])**2)
		y_train = gda_pridect(train[:,:n-1],mu0,mu1,cov_m)
		train_errs[i] = np.mean((y_train-train[:,n-1])**2)
		print "train error: %f, test error: %f" %(train_errs[i], errs[i])
	print "the average train error rate is: %f" %np.mean(train_errs)
	print "the average test error rate is: %f" %np.mean(errs)
	print "============================================="