import numpy as np
import time
C = 0.5

LINEAR1 = 'L1'
LINEAR2 = 'L2'
GAUSSIAN = 'G'

class SVM:
	def __init__(self,D,kernal=LINEAR1):
		m,n = D.shape
		self.norm_mean = None
		self.norm_std = None
		self.X = self.normalize(D[:,:n-1])
		self.y = 2*(D[:,n-1]-0.5)
		self.alpha = np.zeros(m)
		self.b = 0.0
		if kernal == GAUSSIAN:
			self.kernal_fun = self.gaussian_kernal
			self.kernal_fun_test = self.gaussian_kernal_test
		elif kernal == LINEAR2:
			self.kernal_fun = self.linear_kernal2
			self.kernal_fun_test = self.linear_kernal2
		else:
			self.kernal_fun = self.linear_kernal1
			self.kernal_fun_test = self.linear_kernal2

	def normalize(self,X):
		if self.norm_mean == None and self.norm_std == None:
			self.norm_mean = np.mean(X,axis=0)
			self.norm_std = np.std(X,axis=0)
		return (X-self.norm_mean)/self.norm_std

	def learn(self):
		self.K = self.kernal_fun(self.X)
		print '-'
		m = len(self.X)
		updates = m
		examine_all = True
		while updates > 0 or examine_all:
			updates = 0
			for i in range(m):
				if self.violate_KKT(i,examine_all):
					Ei = self.f(i) - self.y[i]
					max_diffE = 0
					for j in range(m):
						Ej = self.f(j)-self.y[j]
						diffE =  abs(Ei-Ej)
						if diffE > max_diffE:
							max_diffE = diffE
							max_index = j
							max_Ej = Ej
					j = max_index
					Ej = max_Ej
					eta = self.K[i,i] + self.K[j,j] - 2 * self.K[i,j]
					alphaj = self.alpha[j] + self.y[j]*(Ei-Ej)/eta
					alphaj = self.clip_alphaj(alphaj,i,j)
					if alphaj == self.alpha[j]:
						continue
					alphai = self.alpha[i] + self.y[i]*self.y[j]*(self.alpha[j]-alphaj)
					self.b = self.update_b(i,j,alphai,alphaj,Ei,Ej)
					self.alpha[i] = alphai
					self.alpha[j] = alphaj
					updates += 1
			if examine_all==True:
				examine_all = False
			elif updates == 0:
				examine_all = True
			print updates
		del self.K
	
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
				K[i,j] = np.exp(-0.5*sum((self.X[i]-X[j])**2)) # sigma = 1
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

	def violate_KKT(self,i,examine_all):
		yf = self.y[i]*self.f(i)
		if self.alpha[i] == 0.0:
			return yf < 1.0 and examine_all
		elif self.alpha[i] == C:
			return yf > 1.0 and examine_all
		else:
			return abs(yf - 1.0) > 1e-6

	def clip_alphaj(self,alphaj,i,j):
		if self.y[i] == self.y[j]:
			L = max(0.0,self.alpha[i]+self.alpha[j]-C)
			H = min(C,self.alpha[i]+self.alpha[j])
		else:
			L = max(0.0,self.alpha[j]-self.alpha[i])
			H = min(C,self.alpha[j]-self.alpha[i]+C)
		if alphaj < L:
			return L
		elif alphaj > H:
			return H
		else:
			return alphaj

	def update_b(self,i,j,alphai,alphaj,Ei,Ej):
		bi = self.b - Ei + (self.alpha[i]-alphai)*self.y[i]*self.K[i,i]+(self.alpha[j]-alphaj)*self.y[j]*self.K[j,i]
		bj = self.b - Ej + (self.alpha[i]-alphai)*self.y[i]*self.K[i,j]+(self.alpha[j]-alphaj)*self.y[j]*self.K[j,j]
		if alphai > 0 and alphai < C:
			return bi
		elif alphaj > 0 and alphaj < C:
			return bj
		else:
			return (bi+bj)/2.0

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

if __name__ == '__main__':
	train,test = load_data_spambase()
	d = test.shape[1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	svm = SVM(train,kernal=GAUSSIAN)
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

		