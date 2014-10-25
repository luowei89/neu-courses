#! /usr/bin/env python
"""
DBSCAN
"""
import sys
import numpy as np
import plot_scatter as ps
import cluster_analysis as ca

def dbscan(D,eps,minPts):
	cluster_label = -1*np.ones(len(D))
	cluster = -1
	for i in range(len(D)):
		if cluster_label[i] == -1:
			neighborPts = regionQuery(i,D,eps)
			if len(neighborPts) < minPts:
				cluster_label[i] = -2 # noise
			else :
				cluster = cluster + 1
				cluster_label = expand_cluster(i,neighborPts,D,cluster,eps,minPts,cluster_label)
	return cluster_label

def regionQuery(index,D,eps):
	p = D[index]
	distances = np.array([distance(p,x) for x in D])
	indexes, = np.where(distances <= eps)
	return indexes

def distance(x1,x2):
	return np.sqrt(np.sum((x1-x2)**2))

def expand_cluster(i,neighborPts,D,cluster,eps,minPts,cluster_label):
	cluster_label[i] = cluster
	array_updated = True
	while array_updated:
		array_updated = False
		for j in neighborPts:
			if cluster_label[j] == -1:
				array_updated = True
				neighborPts_ = regionQuery(j,D,eps)
				if len(neighborPts_) >= minPts:
					neighborPts = np.append(neighborPts,neighborPts_)
				cluster_label[j] = cluster
	return cluster_label

def translate_member(a):
	k = len(np.unique(a))
	m = len(a)
	membership = np.zeros((m,k))
	for i in range(m):
		if a[i] == -2:
			membership[i][k-1] = 1
		else:
			membership[i][a[i]] = 1
	return membership

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) < 3:
		print "usage: python dbscan.py dataset_file eps minPts"
	else:
		dataset = args[0]
		eps = float(args[1])
		minPts = int(args[2])
		X = np.loadtxt(dataset)
		m,d = X.shape
		k = len(np.unique(X[:,d-1]))
		#dataset1 0.7,15
		#dataset2 0.9,5
		#dataset3 0.3,10
		member = translate_member(dbscan(X[:,:d-1],eps,minPts))
		ps.plot_scatter(X[:,:d-1],member,"DBSCAN with %s" %dataset)
		print "Purity is %f" %ca.purity(X[:,d-1],member)
		print "NMI is %f" %ca.nmi(X[:,d-1],member)