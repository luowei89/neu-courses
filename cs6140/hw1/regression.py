import numpy

def normalize(X_train,X_test):
	"""
	Shift and scale normalization on all features
	"""
	X = numpy.vstack((X_train,X_test))
	X_norm = numpy.zeros(X.shape)
	for i in range(X.shape[1]):
		x = X[:,i]
		min_x = numpy.min(x)
		max_x = numpy.max(x)
		X_norm[:,i] = (x-min_x)/float(max_x-min_x)
	return X_norm[:X_train.shape[0],:],X_norm[X_train.shape[0]:,:]

def caculateW(X,y):
	X1 = addOnes(X)
	XtX = numpy.matrix(numpy.dot(X1.T,X1))
	XtY = numpy.dot(X1.T,y)
	w = numpy.dot(numpy.linalg.pinv(XtX),XtY)
	return numpy.squeeze(numpy.asarray(w))

def predict(X,w):
	X1 = addOnes(X)
	return numpy.dot(X1,w)

def predict_0_1(X,w):
	X_predict = predict(X,w)
	for i in range(len(X_predict)):
		X_predict[i] = 0 if X_predict[i] < 0.5 else 1
	return X_predict

def addOnes(X):
	ones = numpy.array([numpy.ones(X.shape[0])]).T
	return numpy.hstack((ones,X))