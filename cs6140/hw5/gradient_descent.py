"""
Gradient Descent for Linear/Logistic Regression, Copied from hw2
"""
import numpy as np
import math

def gradient_descent(X,y,alpha,iters,linear):
	w = np.zeros(X.shape[1])
	h = linear_h if linear else logistic_h
	m = len(y)
	n = len(w)
	old_w = np.copy(w)
	for k in range(iters):
		for i in range(m):
			w = w - alpha*(h(w,X[i])-y[i])*X[i]
		if sum(abs(old_w - w)) < 1e-10:
			return w
		else:
			old_w = np.copy(w)
		alpha = alpha * 0.9
	return w

def linear_h(w,x):
    return np.dot(w,x)

def logistic_h(w,x):
	return 1/(1 + np.exp(-np.dot(w,x)))

def extract_data(D):
	m = D.shape[0]
	n = D.shape[1]
	X = D[:,0:n-1]
	y = D[:,n-1]
	ones = np.array([np.ones(m)]).T
	X = np.hstack((ones,X))
	return X,y

def normalize(X):
	"""
	returns a normalized version of X where the mean value
	 of each feature is 0 and the standard deviation is 1.
	"""
	means = np.mean(X,axis=0)
	stds = np.std(X,axis=0)
	means[0] = 0
	stds[0] = 1
	X_norm = (X-means)/stds
	return X_norm,means,stds

def normalizeMS(X,means,stds):
	"""
	normalize X with means and stds given
	"""
	X_norm = (X-means)/stds
	return X_norm

def predict(X,w):
	return np.dot(X,w)

def predict_boolean(X,w,threshold):
	X_predict = predict(X,w)
	for i in range(len(X_predict)):
		X_predict[i] = 0 if X_predict[i] < threshold else 1
	return X_predict