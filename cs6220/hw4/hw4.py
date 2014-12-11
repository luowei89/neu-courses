import numpy as np
import networkx as nx

def dtw(a,b):
	m = len(a)
	n = len(b)
	D = np.zeros((n,m))
	x = np.abs(b-a[0])
	y = np.abs(a-b[0])
	for i in range(n):
		D[i][0] = sum(x[:i+1])
	for i in range(m):
		D[0][i] = sum(y[:i+1])

	for i in range(1,n):
		for j in range(1,m):
			D[i][j] = min(D[i-1,j],D[i,j-1],D[i-1,j-1])+abs(b[i]-a[j])

	for line in D.astype(int):
		print line.tolist()


def adj_matrix():
	links = [(1,3),(1,4),(2,3),(3,2),(3,4),(3,5),(3,6),(4,1),(4,4),(5,6),(6,2)]
	A = [[0.0 for i in range(6)] for j in range(6)]
	for i,j in links:
		A[j-1][i-1]=1.0
	for a in A: print a

	M = A/np.sum(A,axis=0)
	for m in M: print m

	M_s = 0.8*M+0.2*(1.0/6)
	for m in M_s: print m
	print np.sum(M_s,axis=0)

	print 1.0/30
	print 13.0/30
	print 5.0/6
	print 7.0/30

	G = nx.DiGraph(links)
	pr = nx.pagerank(G)
	r = np.array([pr[i+1] for i in range(6)])
	print r
	print np.dot(M_s,r)

	r0 = np.array([1.0/6 for i in range(6)])
	
	while True:
		r1 = np.dot(M_s,r0)
		if (r1 == r0).all():
			break
		r0 = r1
	print r0
	print np.dot(M_s,r0)
	print 0.8*np.dot(M,r0)+0.2*(1.0/6)

	M_s = 0.8*M+0.2*np.array([[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
	for m in M_s: print m
	print '----------'
	print np.sum(M_s,axis=0)

	while True:
		r1 = np.dot(M_s,r0)
		if (r1 == r0).all():
			break
		r0 = r1
	print r0
	print np.dot(M_s,r0)
	print 0.8*np.dot(M,r0)+0.2*np.array([1,0,0,0,0,0])

if __name__ == '__main__':
	a = np.array([71, 73, 80, 80, 80, 78, 76, 75, 73, 71, 71, 71, 73, 75, 76, 76, 68, 76, 76, 75])
	b = np.array([69, 69, 73, 79, 80, 79, 78, 76, 73, 72, 71, 70, 70, 69, 69, 69, 71, 73, 75, 76])
	#dtw(a,b)
	adj_matrix()