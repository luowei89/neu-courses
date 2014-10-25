#! /usr/bin/env python
"""
EM with Gaussian Mixture
"""
import sys
import numpy as np
import plot_scatter as ps
import cluster_analysis as ca

MAX_ITER = 500

def emgm(X,k):
	params = init(X,k)
	for i in range(MAX_ITER):
		old_z = np.copy(params['z'])
		params = expectation(X,params)
		params = maximization(X,params)
		if (old_z == params['z']).all():
			print "converge at iteration %d" %i
			break
	return params

def init(X,k):
	params = {}
	m,d = X.shape
	rand_inx = np.random.randint(m,size=k)
	params['mu'] = X[rand_inx]
	params['sigma'] = np.ones((k,d,d))
	for i in range(k):
		rand_inx = np.random.randint(m,size=20)
		params['sigma'][i] = np.cov(X[rand_inx].T) + np.identity(d)*1e-6
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
	sigma_inv = [np.linalg.pinv(sigma_j) for sigma_j in sigma]
	sigma_det = [np.linalg.det(sigma_j) for sigma_j in sigma]
	for i in range(m):
		for j in range(n):
			exp = -0.5*np.dot(np.dot((X[i]-mu[j]),sigma_inv[j]),(X[i]-mu[j]))
			params['z'][i][j] = (2*np.pi)**(-d/2)*sigma_det[j]**(-1/2)*np.exp(exp)
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
		if pi != 0:
			params['sigma'][i] = sigma/pi + np.identity(d)*1e-6
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
		print int(np.sum(params['z'],axis=0)[i])
		print "-----------------"	

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) < 1:
		print "usage: python em.py dataset_file"
	else:
		dataset = args[0]
		X = np.loadtxt(dataset)
		m,d = X.shape
		k = len(np.unique(X[:,d-1]))
		params = emgm(X[:,:d-1],k)
		ps.plot_scatter(X[:,:d-1],params['z'],"EM with %s" %dataset)
		print "Purity is %f" %ca.purity(X[:,d-1],params['z'])
		print "NMI is %f" %ca.nmi(X[:,d-1],params['z'])