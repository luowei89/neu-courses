import numpy as np
import gradientDescent as gd
import confusionMatrix as cm
import plotROC as plt

import time

def problem1():

	alpha = 0.01 # gradient descent learning rate for housing
	beta = 0.002 # gradient descent (linear) learning rate for spambase
	gama = 0.02 # gradient descent (logistic) learning rate for spambase
	iterations = 1000 # gradient descent maximum iterations
	linear = True
	logistic = False
	threshold = 0.4
	K = 10

	print "============================================="
	print "loading housing data..."
	housing_train = np.loadtxt("../dataset/housing/housing_train.txt")
	housing_test = np.loadtxt("../dataset/housing/housing_test.txt")
	
	h_X,h_y = gd.extractData(housing_train)
	ht_X,ht_y = gd.extractData(housing_test)
	
	print "training for linear regression with gradient descent..."
	w = np.zeros(h_X.shape[1])
	h_X_norm,h_X_means,h_X_stds = gd.normalize(h_X)
	w = gd.gradientDescent(h_X_norm,h_y,w,alpha,iterations,linear)

	print "predict for housing training data, mse is:"
	htrain_predict = gd.predict(h_X_norm,w)
	print np.mean((htrain_predict-h_y)**2)

	print "predict for housing test data, mse is:"
	ht_X_norm = gd.normalizeMS(ht_X,h_X_means,h_X_stds)
	htest_predict = gd.predict(ht_X_norm,w)
	print np.mean((htest_predict-ht_y)**2)
	print "============================================="
	
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	k_folds = np.array_split(spambase,K)
	mses = np.zeros(K)
	conf_m = np.zeros(4)
	
	print "============================================="
	print "training (linear regression with gradient descent)" 
	print "with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		start = time.time()

		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))

		train_X,train_y = gd.extractData(train)
		test_X,test_y = gd.extractData(test)

		w = np.zeros(train_X.shape[1])
		train_X_norm,t_means,t_stds =  gd.normalize(train_X)
		w = gd.gradientDescent(train_X_norm,train_y,w,beta,iterations,linear)

		test_X_norm = gd.normalizeMS(test_X,t_means,t_stds)

		predict = gd.predictBoolean(test_X_norm,w,threshold)

		mses[i] = np.mean((predict-test_y)**2)
		print "mse is %f, time is %f seconds." %(mses[i],(time.time()-start))
		conf_m += cm.confusionMatrix(predict,test_y)

	#plot ROC for last iteration
	plt.plotROC(test_X_norm,test_y,w,"ROC_linear_regression.jpg")

	conf_m = conf_m/K
	print "the average mse is: %f" %np.mean(mses)
	print "the confusion matrix is: (TPR,FPR,TNR,FNR)"
	print conf_m
	print "============================================="
	
	mses = np.zeros(K)
	conf_m = np.zeros(4)

	print "training (logistic regression with gradient descent)" 
	print "with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		start = time.time()

		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))

		train_X,train_y = gd.extractData(train)
		test_X,test_y = gd.extractData(test)

		w = np.zeros(train_X.shape[1])
		train_X_norm,t_means,t_stds =  gd.normalize(train_X)
		w = gd.gradientDescent(train_X_norm,train_y,w,gama,iterations,logistic)

		test_X_norm = gd.normalizeMS(test_X,t_means,t_stds)

		predict = gd.predictBoolean(test_X_norm,w,threshold)

		mses[i] = np.mean((predict-test_y)**2)
		print "mse is %f, time is %f seconds." %(mses[i],(time.time()-start))
		conf_m += cm.confusionMatrix(predict,test_y)

	#plot ROC for last iteration
	plt.plotROC(test_X_norm,test_y,w,"ROC_logistic_regression.jpg")

	conf_m = conf_m/K
	print "the average mse is: %f" %np.mean(mses)
	print "the confusion matrix is: (TPR,FPR,TNR,FNR)"
	print conf_m
	print "============================================="

if __name__ == "__main__":
	problem1()