"""
plot_scatter.py
"""
import numpy as np
import matplotlib.pyplot as plt

colors = ['r','g','b','c','m','y','k']

def plot_scatter(X,member,title):
	m,k = member.shape
	x = []
	y = []
	for i in range(k):
		x.append([])
		y.append([])
	for i in range(m):
		for j in range(k):
			if member[i][j] == 1:
				# 2 dimention only
				x[j].append(X[i][0])
				y[j].append(X[i][1])
	plt.clf()
	plt.title(title)
	for i in range(k):
		plt.scatter(x[i],y[i],color=colors[i])
	plt.savefig("%s.png" %title)


if __name__ == '__main__':
	X = np.array([[1,2],[2,3],[3,4]])
	member = np.array([[1,0],[0,1],[0,1]])
	plot_scatter(X,member,"1")