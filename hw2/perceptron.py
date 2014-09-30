import numpy as np

def perceptron(X,y):
	trans_X = transform(X,y)
	w = np.zeros(X.shape[1])
	total_mistake = -1
	iteration = 0
	while total_mistake != 0:
		total_mistake = 0
		for i in range(len(trans_X)):
			xi = trans_X[i]
			if np.dot(w,xi) <= 0:
				w = w + xi
				total_mistake += 1
		iteration += 1
		print "Iteration %d, total_mistake %d" %(iteration,total_mistake)
	return w

def transform(X,y):
	trans_X = np.zeros(X.shape)
	for i in range(len(X)):
		trans_X[i] = X[i] * y[i]
	return trans_X
