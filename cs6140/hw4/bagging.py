import numpy as np
import cart,node,time

T = 50
K = 10

def bagging(train):
	N,d = train.shape
	dts = {}
	for i in range(T):
		s = time.time()
		train_i = train[np.random.randint(N, size=N)]
		dts[i] = cart.fitTree(node.Node(),train_i,0,False,5)
		print "decision tree %d, time %f" %(i,time.time()-s)
	return dts

def bagging_predict(test,dts):
	N,d = test.shape
	ys = np.zeros((N,len(dts)))
	for ti in dts:
		ys[:,i] = cart.predict(test[:,:d-1],dts[ti])
	y = np.mean(ys,axis=1)
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
	y = bagging_predict(test,dts)
	labels = test[:,d-1]
	err = np.sum(np.logical_xor(y,labels))/float(m)
	print err
