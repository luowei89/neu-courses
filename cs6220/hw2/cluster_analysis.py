"""
cluster_analysis.py
"""
import numpy as np

def purity(labels,membership):
	clustered = 0
	ls = np.unique(labels)
	for l in ls:
		clustered = clustered + np.max(np.sum(membership[labels==l],axis=0))
	return clustered/float(len(labels))

def nmi(labels,membership):
	ls = np.unique(labels)
	k = len(ls)
	N = float(len(labels))
	ground_truth = np.zeros(k)
	for i in range(k):
		ground_truth[i] = len(labels[labels==ls[i]])
	ho = h(ground_truth)
	hc = h(np.sum(membership,axis=0))
	label_mem = translate_member(labels)
	ioc = iab(label_mem,membership)
	return ioc/np.sqrt(ho*hc)

def h(a):
	N = float(np.sum(a))
	return -1 * np.sum([x/N*np.log(x/N) for x in a])

def iab(mem_a,mem_b):
	ioc = 0
	m,k = mem_a.shape
	count_a = np.sum(mem_a,axis=0)
	count_b = np.sum(mem_b,axis=0)
	for i in range(k):
		for j in range(k):
			a_and_b = and_count(mem_a[:,i] == 1,mem_b[:,j] == 1)
			if a_and_b > 0:
				ioc = ioc + a_and_b/float(m)*np.log(m*a_and_b/float(count_a[i]*count_b[j]))
	return ioc

def and_count(a,b):
	count = 0
	for i in range(len(a)):
		if a[i] and b[i]:
			count  = count + 1
	return count

def translate_member(a):
	k = len(np.unique(a))
	m = len(a)
	membership = np.zeros((m,k))
	for i in range(m):
		membership[i][a[i]-1] = 1
	return membership

if __name__ == '__main__':
	# question 1
	ground_truth_label = np.array([3,3,1,1,1,4,3,3,4,2,4,2,1,2,3,2,1,2,4,4])
	output_label = np.array([2,2,3,3,3,4,2,2,3,1,4,1,3,1,2,1,2,1,4,1])
	print purity(ground_truth_label,translate_member(output_label))
	print nmi(ground_truth_label,translate_member(output_label))