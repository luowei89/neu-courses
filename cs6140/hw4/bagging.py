import numpy as np
import cart,node,time
import matplotlib.pyplot as plt

T = 50
K = 10

def bagging(train):
	N,d = train.shape
	dts = {}
	for i in range(T):
		s = time.time()
		train_i = train[np.random.randint(N, size=N)]
		dts[i] = cart.fitTree(node.Node(),train_i,0,False,5)
		print "decision tree %d, time %fs" %(i,time.time()-s)
	return dts

def bagging_predict(test,dts):
	N,d = test.shape
	ys = np.zeros((len(dts),N))
	for ti in dts:
		ys[ti] = cart.predict(test[:,:d-1],dts[ti])#dts[ti].predict(test[:,:d-1])
		print "decision tree %d, err %f" %(ti,np.sum(np.logical_xor(ys[ti],test[:,d-1]))/float(N))
	y = np.mean(ys,axis=0)
	return y > 0.5

if __name__ == '__main__':
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	k_folds = np.array_split(spambase,K)
	i = int(np.random.rand()*K)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	print "============================================="
	dts = bagging(train)
	m,d = test.shape
	labels = test[:,d-1]
	y = bagging_predict(test,dts)
	err = np.sum(np.logical_xor(y,labels))/float(m)
	print err
