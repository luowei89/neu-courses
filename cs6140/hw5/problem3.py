import numpy as np
import gradient_descent as gd
from sklearn import linear_model

alpha = 0.1 # learning rate for gradient descent
l = 0.01    # lambda for lagrange multipliers
MAX_ITER = 1000

def logistic_regression(train_X,train_y,test_X,test_y):
	print "Logistic Regression with Gradient Descent..."
	w = gd.gradient_descent(train_X,train_y,alpha,MAX_ITER,False)
	predicted = gd.predict_boolean(test_X,w,0.4)
	acc = np.sum(predicted==test_y)/float(len(test_y))
	print "Logistic Regression, Accuracy: %f" %acc

def sklearn_regularized_regression(train_X,train_y,test_X,test_y):
	lasso = linear_model.Lasso(alpha=l)
	lasso.fit(train_X,train_y)
	predicted_l = lasso.predict(test_X) > 0.42
	acc_l = np.sum(predicted_l==test_y)/float(len(test_y))
	print "Sklearn LASSO Regularized Regression, Accuracy: %f" %acc_l

def ridge_logistic_regression(train_X,train_y,test_X,test_y):
	w = gradient_descent_ridge(train_X,train_y,alpha)
	predicted = gd.predict_boolean(test_X,w,0.4)
	acc = np.sum(predicted==test_y)/float(len(test_y))
	print "RIDGE Logistic Regression, Accuracy: %f" %acc

def gradient_descent_ridge(X,y,alpha):
	m,d = X.shape
	w = np.zeros(d)
	old_w = np.copy(w)
	for k in range(MAX_ITER):
		for i in range(m):
			w = w - alpha*((logistic_h(w,X[i])-y[i])*X[i]+l*w)
		if sum(abs(old_w - w)) < 1e-10:
			return w
		else:
			old_w = np.copy(w)
		alpha = alpha * 0.9
	return w	

def logistic_h(w,x):
	return 1/(1 + np.exp(-np.dot(w,x)))

if __name__ == '__main__':
	print "============================================="
	print "loading spambase polluted data..."
	train_X = np.loadtxt("../dataset/spam_polluted/train_feature.txt")
	train_y = np.loadtxt("../dataset/spam_polluted/train_label.txt")
	test_X = np.loadtxt("../dataset/spam_polluted/test_feature.txt")
	test_y = np.loadtxt("../dataset/spam_polluted/test_label.txt")
	print "============================================="
	train_X_norm,t_means,t_stds =  gd.normalize(np.concatenate((np.ones((len(train_X),1)),train_X),1))
	test_X_norm = gd.normalizeMS(np.concatenate((np.ones((len(test_X),1)),test_X),1),t_means,t_stds)

	np.seterr(over="ignore") # ignore overflow in exp
	logistic_regression(train_X_norm,train_y,test_X_norm,test_y)
	print "============================================="
	sklearn_regularized_regression(train_X_norm,train_y,test_X_norm,test_y)
	print "============================================="
	ridge_logistic_regression(train_X_norm,train_y,test_X_norm,test_y)
	print "============================================="