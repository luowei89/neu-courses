#! /usr/bin/env python
"""
K-means algorithm for clustering
"""
import sys
import numpy as np
import plot_scatter as ps
import cluster_analysis as ca

MAX_ITER = 500

def k_means(X,k):
	member = init(X,k)
	means = calculate_means(X,member)
	for i in range(MAX_ITER):
		old_member = np.copy(member)
		member = update_member(X,means,member)
		if (member == old_member).all():
			print "converge at iteration %d" %i
			break;
		means = calculate_means(X,member)
	return member

def init(X,k):
	m,d = X.shape
	membership = np.zeros((m,k))
	for i in range(m):
		index = int(np.random.rand()*k)
		membership[i][index] = 1
	return membership

def calculate_means(X,member):
	m,d = X.shape
	counts = np.sum(member,axis=0)
	k = len(counts)
	means = np.zeros((k,d))
	for i in range(m):
		for j in range(k):
			if member[i][j] == 1:
				means[j] += X[i]
	for n in range(k):
		means[n] = means[n]/counts[n]
	return means

def update_member(X,means,member):
	m,d = X.shape
	k = len(means)
	for i in range(m):
		for j in range(k):
			member[i][j] = distance(X[i],means[j])
		member[i] = member[i] == min(member[i])
	return member

def distance(x1,x2):
	return np.sum(np.abs(x1-x2))

if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) < 1:
		print "usage: python k_means.py dataset_file"
	else:
		dataset = args[0]
		X = np.loadtxt(dataset)
		m,d = X.shape
		k = len(np.unique(X[:,d-1]))
		member = k_means(X[:,:d-1],k)
		ps.plot_scatter(X[:,:d-1],member,"K-means with %s" %dataset)
		print "Purity is %f" %ca.purity(X[:,d-1],member)
		print "NMI is %f" %ca.nmi(X[:,d-1],member)