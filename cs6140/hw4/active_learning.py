import numpy as np
import ada_boosting as ab
import uci_data as ucid
import matplotlib.pyplot as plt

def active_learning_uci(data_set,c):
	data,config = ucid.data_path(data_set)
	D = ucid.parse_data(data,config)
	active_learning(D,data_set,c)

def active_learning(D,data_set,c):
	print "================================================================================"
	print "Active Learning on %s dataset with %d%% actively-built training set." %(data_set,c)
	N,d = D.shape
	size=c*N/100
	rand_idndex = np.zeros(len(D),dtype=bool)
	rand_idndex[:N/10] = True
	np.random.shuffle(rand_idndex)
	test = D[rand_idndex]
	train_remain = D[np.logical_not(rand_idndex)]
	add_train_idx = new_idx([],train_remain,5*N/100)
	train = train_remain[add_train_idx]
	train_remain = train_remain[np.logical_not(add_train_idx)]
	train_remain_random = np.copy(train_remain)
	train_random = np.copy(train)
	wwls,xs,ys,wwls_random,xs_random,ys_random = [],[],[],[],[],[]
	while (len(train) < N/2):
		add_train_idx = new_idx(wwls,train_remain,size)
		add_train = train_remain[add_train_idx]
		train_remain = train_remain[np.logical_not(add_train_idx)]
		train = np.vstack((train,add_train))
		wwls = ab.ada_boosting(train,test)
		err = ab.error_rate(ab.ada_predict(test[:,:d-1],wwls),test[:,d-1])
		xs.append(len(train)/float(N))
		ys.append(err)
	while (len(train_random) < N/2):
		add_train_idx_random = new_idx([],train_remain_random,size)
		add_train_random = train_remain_random[add_train_idx_random]
		train_remain_random = train_remain_random[np.logical_not(add_train_idx_random)]
		if len(train_random) == 0:
			train_random = add_train_random
		else:
			train_random = np.vstack((train_random,add_train_random))
		wwls_random = ab.ada_boosting(train_random,test)
		err_random = ab.error_rate(ab.ada_predict(test[:,:d-1],wwls_random),test[:,d-1])
		xs_random.append(len(train_random)/float(N))
		ys_random.append(err_random)
	plt.clf()
	plt.plot(xs,ys)
	plt.plot(xs_random,ys_random)
	plt.legend(['Active Learning','Random Choose'], loc='upper right')
	plt.savefig("p3_err.png")

def new_idx(wwls,train_remain,size):
	if len(wwls) == 0:
		idx = np.zeros(len(train_remain),dtype=bool)
		idx[:size] = True
		np.random.shuffle(idx)
	else:
		d = train_remain.shape[1]
		fx = ab.f_X(train_remain[:,:d-1],wwls)
		threshold = np.sort(np.abs(fx))[size]
		idx = np.abs(fx) <= threshold
	return idx

if __name__ == '__main__':
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	print "============================================="
	active_learning(spambase,"spambase",5)
	active_learning_uci("crx",2)
	