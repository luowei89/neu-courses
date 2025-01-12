import numpy
import cart
import node
import regression
import confusionMatrix as cm

import time

K = 10
MAX_DEPTH_RT = 2
MAX_DEPTH_DT = 5

if __name__ == "__main__":

	print "============================================="
	print "loading housing data..."
	housing_train = numpy.loadtxt("../dataset/housing/housing_train.txt")
	housing_test = numpy.loadtxt("../dataset/housing/housing_test.txt")
	n = housing_train.shape[1]	
	
	print "building regression tree for housing dataset..."
	tree = cart.fitTree(node.Node(),housing_train,0,True,MAX_DEPTH_RT)
	
	print "predict for housing training data, mse is:"
	htrain_predict = cart.predict(housing_train[:,0:n-1],tree)
	htrain_labels = housing_train[:,n-1]
	print numpy.mean((htrain_predict-htrain_labels)**2)

	print "predict for housing test data, mse is:"
	htest_predict = cart.predict(housing_test[:,0:n-1],tree)
	htest_labels = housing_test[:,n-1]
	print numpy.mean((htest_predict-htest_labels)**2)
	print "============================================="
	
	print "loading spambase data..."
	spambase = numpy.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	numpy.random.shuffle(spambase)
	s_n = spambase.shape[1]	

	k_folds = numpy.array_split(spambase,K)
	mses = numpy.zeros(K)
	# for hw2
	mses_train = numpy.zeros(K)
	conf_m = numpy.zeros(4,dtype=int)
	# end
	
	print "building decision tree with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		start = time.time()

		test = k_folds[i]
		train = numpy.vstack(numpy.delete(k_folds, i, axis=0))
		tree = cart.fitTree(node.Node(),train,0,False,MAX_DEPTH_DT)
		predict = cart.predict(test[:,0:s_n-1],tree)
		labels = test[:,s_n-1]
		mses[i] = numpy.mean((predict-labels)**2)
		print "mse is %f, time is %f seconds." %(mses[i],(time.time()-start))
		# added for hw2
		predict_train = cart.predict(train[:,0:s_n-1],tree)
		labels_train = train[:,s_n-1]
		mses_train[i] = numpy.mean((predict_train-labels_train)**2)
		conf_m += cm.confusionMatrix(predict,labels)
		# end

	# for hw2]
	print "the average acc (train) is: %f" %(1-numpy.mean(mses_train))
	print "the average acc (test) is: %f" %(1-numpy.mean(mses))
	print "the confusion matrix is: (TP,FP,TN,FN)"
	print conf_m/K
	# end
	print "============================================="
	print ""
	print "=================linear regression================="	
	h_X = housing_train[:,:n-1]
	h_y = housing_train[:,n-1]
	h_X_test = housing_test[:,:n-1]
	h_y_test = housing_test[:,n-1]
	print "training with housing training data..."
	h_X_norm,h_X_test_norm = regression.normalize(h_X,h_X_test)
	w = regression.caculateW(h_X_norm,h_y)
	mse_h_train = numpy.mean((regression.predict(h_X_norm,w) - h_y)**2)
	mse_h_test = numpy.mean((regression.predict(h_X_test_norm,w) - h_y_test)**2)
	print "for housing training data mse is %f" %mse_h_train
	print "for housing test data mse is %f" %mse_h_test
	
	mses = numpy.zeros(K)
	
	print "linear regression with spambase dataset with %d folds cross-validation..." %K
	for i in range(K):
		test = k_folds[i]
		train = numpy.vstack(numpy.delete(k_folds, i, axis=0))
		s_X = train[:,:s_n-1]
		s_y = train[:,s_n-1]
		s_t_X = test[:,:s_n-1]
		s_t_y = test[:,s_n-1]
		s_X_norm,s_t_X_norm = regression.normalize(s_X,s_t_X)
		w = regression.caculateW(s_X_norm,s_y)
		predict = regression.predict_0_1(s_t_X_norm,w)
		mses[i] = numpy.mean((predict-s_t_y)**2)

		# added for hw2
		predict_train = cart.predict(train[:,0:s_n-1],tree)
		labels_train = train[:,s_n-1]
		mses_train[i] = numpy.mean((predict_train-labels_train)**2)
		conf_m += cm.confusionMatrix(predict,labels)
		# end

	# for hw2
	print "the average acc (train) is: %f" %(1-numpy.mean(mses_train))
	print "the average acc (test) is: %f" %(1-numpy.mean(mses))
	# end
	print "==================================================="
