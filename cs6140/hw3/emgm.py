"""
EM with Gaussian Mixture
"""
import numpy as np
import copy

MAX_ITER = 500
TOL = 10**(-2)
def emgm(X,k):
	params = init(X,k)
	for i in range(MAX_ITER):
		print "iteration %d..." %i
		old_p = copy.deepcopy(params)
		params = expectation(X,params)
		params = maximization(X,params)
		if converge(old_p,params):
			print "converge at iteration %d" %i
			break
		np.sum(params['z'],axis=0)
	return params

def converge(old,new):
	conv_mu = np.sum(np.abs(old['mu'] - new['mu'])) < TOL
	conv_pi = np.sum(np.abs(old['pi'] - new['pi'])) < TOL
	conv_sigma = np.sum(np.abs(old['sigma'] - new['sigma'])) < TOL
	conv_z = np.sum(np.abs(old['z'] - new['z'])) < TOL
	return conv_mu and conv_pi and conv_sigma and conv_z

def init(X,k):
	params = {}
	m,d = X.shape
	rand_inx = np.random.randint(m,size=k)
	params['mu'] = X[rand_inx]
	params['sigma'] = np.ones((k,d,d))
	for i in range(k):
		rand_inx = np.random.randint(m,size=20)
		params['sigma'][i] = np.cov(X[rand_inx].T)
	params['z'] = np.zeros((m,k))	
	for i in range(m):
		index = int(np.random.rand()*k)
		params['z'][i][index] = 1
	params['pi'] = np.sum(params['z'],axis=0)/np.sum(params['z'])
	return params

def expectation(X,params):
	pi = params['pi']
	mu = params['mu']
	sigma = params['sigma']
	m,d = X.shape
	n = len(mu)
	for i in range(m):
		for j in range(n):
			exp = -0.5*np.dot(np.dot((X[i]-mu[j]),np.linalg.pinv(sigma[j])),(X[i]-mu[j]))
			params['z'][i][j] = (2*np.pi)**(-d/2)*np.linalg.det(sigma[j])**(-1/2)*np.exp(exp)
		params['z'][i] = params['z'][i] == np.max(params['z'][i])
	return params

def maximization(X,params):
	mu = params['mu']
	z = params['z']
	m,d = X.shape
	k = len(mu)
	for i in range(k):
		sigma = np.zeros(params['sigma'][i].shape)
		mu = np.zeros(params['mu'][i].shape)
		pi = 0
		for j in range(m):
			sigma += z[j][i]*np.dot(np.matrix(X[j]-params['mu'][i]).T,np.matrix(X[j]-params['mu'][i]))
			mu += z[j][i]*X[j]
			pi += z[j][i]
		params['sigma'][i] = sigma/pi
		params['mu'][i] = mu/pi
		params['pi'][i] = pi/m
	return params

def print_params(params):
	k = len(params['mu'])
	for i in range(k):
		print "-----------------"
		print "Gaussian %d" %(i+1)
		print "-----------------"
		print "mean:"
		print params['mu'][i]
		print "-----------------"
		print "covariance"
		print params['sigma'][i]
		print "-----------------"
		print "# points:"
		print np.sum(params['z'],axis=0)[i]	
		print "-----------------"	

if __name__ == "__main__":
	print "============================================="
	print "loading 2 gaussian 2-dim data..."
	gaussian2 = np.loadtxt("../dataset/2gaussian.txt")

	params = emgm(gaussian2,2)
	print_params(params)

	print "============================================="
	print "loading 3 gaussian 2-dim data..."
	gaussian3 = np.loadtxt("../dataset/3gaussian.txt")

	params = emgm(gaussian3,3)
	print_params(params)