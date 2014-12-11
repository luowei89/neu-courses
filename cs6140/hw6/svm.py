import numpy as np
import time
C = 1
tol = 1e-3
eps= 1e-3

LINEAR1 = 'L1'
LINEAR2 = 'L2'
GAUSSIAN = 'G'

class SVM:
	def __init__(self,D,kernel=LINEAR1):
		m,n = D.shape
		self.norm_mean = None
		self.norm_std = None
		self.X = self.normalize(D[:,:n-1])
		self.y = 2*(D[:,n-1]-0.5)
		self.alpha = np.zeros(m)
		self.b = 0.0
		if kernel == GAUSSIAN:
			self.kernal_fun = self.gaussian_kernal
			self.kernal_fun_test = self.gaussian_kernal_test
		elif kernel == LINEAR2:
			self.kernal_fun = self.linear_kernal2
			self.kernal_fun_test = self.linear_kernal2
		else:
			self.kernal_fun = self.linear_kernal1
			self.kernal_fun_test = self.linear_kernal1

	def normalize(self,X):
		if self.norm_mean == None and self.norm_std == None:
			self.norm_mean = np.mean(X,axis=0)
			self.norm_std = np.std(X,axis=0)
		return (X-self.norm_mean)/self.norm_std

	def learn(self):
		self.K = self.kernal_fun(self.X)
		m = len(self.X)
		num_changed = 0
		examine_all = True
		while num_changed > 0 or examine_all:
			num_changed = 0
			for i in range(m):
				if examine_all or (self.alpha[i] > 0 and self.alpha[i] < C):
					num_changed += self.examine_example(i)
			if examine_all == True:
				examine_all = False
			elif num_changed == 0:
				examine_all = True
			print num_changed
		del self.K
	
	def examine_example(self,i):
		self.E = [None] * len(self.alpha)#np.dot(self.alpha*self.y,self.K)+self.b - self.y
		self.E[i] = self.f(i) - self.y[i]
		ri = self.E[i] * self.y[i]
		if (ri < -tol and self.alpha[i] < C) or (ri > tol and self.alpha[i] > 0):
			ins, = np.where(np.logical_and(self.alpha > 0, self.alpha < C)) # indexes where 0 < alpha < C
			if len(ins) > 1:
				j = self.pick_alphaj(i,ins)
				if self.take_step(i,j):
					return 1
			np.random.shuffle(ins)
			for j in ins:
				if self.E[j] is None: self.E[j] = self.f(i)-self.y[j]
				if self.take_step(i,j):
					return 1
			all_ins = range(len(self.alpha))	
			np.random.shuffle(all_ins)
			for j in all_ins:
				if self.E[j] is None: self.E[j] = self.f(i)-self.y[j]
				if self.take_step(i,j):
					return 1
		del self.E
		return 0

	def pick_alphaj(self,i,ins):
		max_abs = -1
		for j in ins:
			if self.E[j] is None: self.E[j] = self.f(i)-self.y[j]
			diff_abs =  abs(self.E[i]-self.E[j])
			if diff_abs > max_abs:
				max_abs = diff_abs
				max_index = j
		return max_index

	def take_step(self,i,j):
		if i == j: return False
		s = self.y[i]*self.y[j]
		if self.y[i] == self.y[j]:
			L = max(0.0,self.alpha[i]+self.alpha[j]-C)
			H = min(C,self.alpha[i]+self.alpha[j])
		else:
			L = max(0.0,self.alpha[j]-self.alpha[i])
			H = min(C,self.alpha[j]-self.alpha[i]+C)
		if L == H:
			return False
		eta = self.K[i,i] + self.K[j,j] - 2 * self.K[i,j]
		if eta > 0:
			alphaj = self.alpha[j] + self.y[j]*(self.E[i]-self.E[j])/eta
			if alphaj < L : alphaj = L
			elif alphaj > H : alphaj = H
		else:
			fi = self.y[i]*(self.E[i]+self.b)-self.alpha[i]*self.K[i,i]-s*self.alpha[j]*self.K[i,j]
			fj = self.y[j]*(self.E[j]+self.b)-s*self.alpha[j]*self.K[i,j]--self.alpha[j]*self.K[j,j]
			Li = self.alpha[i]+s*(self.alpha[j]-L)
			Hi = self.alpha[i]+s*(self.alpha[j]-H)
			Lobj = Li*fi+L*fj+0.5*Li*Li*self.K[i,i]+0.5*L*L*self.K[j,j]+s*L*Li*self.K[i,j]
			Hobj = Hi*fi+H*fj+0.5*Hi*Hi*self.K[i,i]+0.5*H*H*self.K[j,j]+s*H*Hi*self.K[i,j]
			if Lobj < Hobj - eps:
				alphaj = L
			elif Lobj > Hobj + eps:
				alphaj = H
			else:
				alphaj = self.alpha[j]
		if abs(alphaj - self.alpha[j]) <= eps * (alphaj + self.alpha[j] + eps):
			return False
		alphai = self.alpha[i] + s*(self.alpha[j]-alphaj)
		bi = self.b - self.E[i] + (self.alpha[i]-alphai)*self.y[i]*self.K[i,i]+(self.alpha[j]-alphaj)*self.y[j]*self.K[j,i]
		bj = self.b - self.E[j] + (self.alpha[i]-alphai)*self.y[i]*self.K[i,j]+(self.alpha[j]-alphaj)*self.y[j]*self.K[j,j]
		if alphai > 0 and alphai < C:
			self.b = bi
		elif alphaj > 0 and alphaj < C:
			self.b = bj
		else:
			self.b = (bi+bj)/2.0
		self.alpha[i] = alphai
		self.alpha[j] = alphaj
		del self.E
		return True

	def linear_kernal1(self,X):
		return np.dot(self.X,X.T)

	def linear_kernal2(self,X):
		K = np.dot(self.X,X.T)
		return K**2

	def gaussian_kernal(self,X):
		# for training only
		m = len(self.X)
		K = np.zeros((m,m))
		for i in range(m):
			for j in range(i,m):
				K[i,j] = np.exp(-1.0*sum((self.X[i]-X[j])**2)/2) # sigma = 1
				K[j,i] = K[i,j]
		return K

	def gaussian_kernal_test(self,X):
		# for testing only
		m = len(self.X)
		n = len(X)
		K = np.zeros((m,n))
		for i in range(m):
			for j in range(n):
				if self.alpha[i] > 0:
					K[i,j] = np.exp(-1.0*sum((self.X[i]-X[j])**2)/2) # sigma = 1
		return K

	def f(self,i):
		return np.dot(self.alpha*self.y,self.K.T[i])+self.b

	def predict(self,X):
		X_norm = self.normalize(X)
		self.K = self.kernal_fun_test(X_norm)
		predicted = np.array([self.f(i) for i in range(len(X))])
		del self.K
		return predicted > 0

def load_data_spambase():
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	k_folds = np.array_split(spambase,10)
	i = int(np.random.rand()*10)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	print "============================================="
	return train,test		

def ten_folds():
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	k_folds = np.array_split(spambase,10)
	acc = np.zeros(10)
	print "============================================="
	for i in range(10):
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))
		acc[i] = one_fold(train,test)
		print "============================================="
	print 'Average accuracy: %f' %np.mean(acc)
	return train,test

def one_fold(train,test):
	d = test.shape[1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	svm = SVM(train,kernel=LINEAR1)
	train_time = time.time()
	svm.learn()
	train_time = time.time() - train_time
	print 'Training time: %fs' %train_time
	test_time = time.time()
	predicted = svm.predict(test_X)
	test_time = time.time() - test_time
	print 'Testing time: %fs' %test_time
	acc = 1-np.logical_xor(predicted,test_y).mean()
	print 'Testing accuracy: %f' %acc
	return acc
		
if __name__ == '__main__':
	ten_folds()

		
