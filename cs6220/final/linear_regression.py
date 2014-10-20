import numpy

def caculateW(X,y):
	X1 = addOnes(X)
	XtX = numpy.matrix(numpy.dot(X1.T,X1))
	XtY = numpy.dot(X1.T,y)
	w = numpy.dot(numpy.linalg.pinv(XtX),XtY)
	return numpy.squeeze(numpy.asarray(w))

def predict(X,w):
	X1 = addOnes(X)
	return numpy.dot(X1,w).tolist()

def addOnes(X):
	ones = numpy.array([numpy.ones(X.shape[0])]).T
	return numpy.hstack((ones,X))