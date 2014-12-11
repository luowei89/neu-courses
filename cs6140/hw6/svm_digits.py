import numpy as np
from scipy import stats
import svm

def svm_digits():
	print "============================================="
	print "loading digits data..."
	train = np.loadtxt("../hw5/digits/train_20.txt")
	test = np.loadtxt("../hw5/digits/test.txt")
	# ===== normalize =====
	d = train.shape[1]
	train_X = train[:,:d-1]
	train_y = train[:,d-1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	norm_mean = np.mean(train_X,axis=0)
	norm_std = np.std(train_X,axis=0)
	train_X = (train_X-norm_mean)/norm_std
	test_X = (test_X-norm_mean)/norm_std
	print "============================================="
	print "Training 45 svms..."
	classes = np.unique(train[:,d-1])
	trains = {}
	svms = {}
	for c in classes:
		trains[c] = train_X[train_y==c],train_y[train_y==c]

	for i in range(len(classes)):
		for j in range(i+1,len(classes)):
			train_Xi,train_yi = trains[i]
			train_Xj,train_yj = trains[j]
			train_Xij = np.vstack((train_Xi,train_Xj))
			train_yij = np.append(train_yi,train_yj)
			train_yij = train_yij == j
			train_ij = np.hstack((train_Xij,np.matrix(train_yij).T))
			np.random.shuffle(train_ij)
			svms[(i,j)] = svm.SVM(np.array(train_ij),kernel=svm.GAUSSIAN)
			svms[(i,j)].learn()

	print "============================================="
	print "Testing..."
	m,d = test.shape
	predicted_matrix = np.zeros((m,len(svms)))
	svm_i = 0
	for i,j in svms:
		predicted_bool = svms[(i,j)].predict(test_X)
		predicted_value = np.zeros(m)
		predicted_value[np.logical_not(predicted_bool)] = i
		predicted_value[predicted_bool] = j
		predicted_matrix[:,svm_i] = predicted_value
		svm_i += 1
	predicted = stats.mode(predicted_matrix,axis=1)[0].T[0]
	print 'Testing accuracy: %f' %((predicted == test_y).mean())
	print "============================================="

if __name__ == '__main__':
	svm_digits()
