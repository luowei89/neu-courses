import numpy as np

LINEAR = 'L'
GAUSSIAN = 'G'

class Perceptron:
	def __init__(self,X,y,kernel=LINEAR,sigma=1e-3):
		self.m = np.zeros(len(X))
		self.X = self.transform(X,y)
		self.y = y
		self.sigma = sigma
		if kernel == GAUSSIAN:
			self.kernal_fun = self.gaussian_kernal
		else:
			self.kernal_fun = self.linear_kernal

	def transform(self,X,y):
		trans_X = np.zeros(X.shape)
		for i in range(len(X)):
			trans_X[i] = X[i] * y[i]
		return trans_X

	def linear_kernal(self,X):
		return np.dot(self.X,X.T)

	def gaussian_kernal(self,X):
		m = len(self.X)
		n = len(X)
		K = np.zeros((m,n))
		for i in range(m):
			for j in range(n):
				diff = self.X[i]-X[j]
				K[i,j] = np.exp(-0.5*np.dot(diff,diff)/np.square(self.sigma))
		return K

	def learn(self):
		K = self.kernal_fun(self.X)
		total_mistake = -1
		iteration = 0
		while total_mistake != 0:
			total_mistake = 0
			for i in range(len(self.m)):
				if np.dot(self.m,K[i]) <= 0:
					self.m[i] += 1
					total_mistake += 1
			iteration += 1
			print "Iteration %d, total_mistake %d" %(iteration,total_mistake)

	def predict(self,X):
		K = self.kernal_fun(X)
		return 2*((np.dot(self.m,K) > 0)-0.5)

if __name__ == '__main__':
	print "============================================="
	print "loading perceptron data..."
	perceptron_data = np.loadtxt("../dataset/perceptronData.txt")
	m,n = perceptron_data.shape
	X = perceptron_data[:,0:n-1]
	y = perceptron_data[:,n-1]
	ones = np.array([np.ones(m)]).T
	X = np.hstack((ones,X))
	print "============================================="
	print 'Train with linear kernel:'
	p = Perceptron(X,y)
	p.learn()
	print 'Accuracy: %f' %(p.predict(X) == y).mean()
	print "============================================="
	print 'Train with Gaussian kernel:'
	p = Perceptron(X,y,GAUSSIAN)
	p.learn()
	print 'Accuracy: %f' %(p.predict(X) == y).mean()
	print "============================================="
	
	print "============================================="
	print "loading twoSpirals data..."
	twoSpirals = np.loadtxt("../dataset/twoSpirals.txt")

	np.random.shuffle(twoSpirals)
	k_folds = np.array_split(twoSpirals,2)

	m,n = twoSpirals.shape
	train_X = k_folds[0][:,0:n-1]
	train_y = k_folds[0][:,n-1]
	test_X = k_folds[1][:,0:n-1]
	test_y = k_folds[1][:,n-1]
	ones = np.array([np.ones(len(train_X))]).T
	train_X = np.hstack((ones,train_X))
	ones = np.array([np.ones(len(test_X))]).T
	test_X = np.hstack((ones,test_X))
	print "============================================="
	print 'Train with Gaussian kernel:'
	p = Perceptron(train_X,train_y,GAUSSIAN,1e-2)
	p.learn()
	print 'Accuracy: %f' %(p.predict(test_X) == test_y).mean()
	print "============================================="
	
#sigma	acc
#0.001 	1.000000
#0.002	0.999000
#0.003	0.990000
#0.004	0.972000
#0.005	0.942000
#0.006	0.906000
#0.007	0.878000
#0.008	0.845000
#0.009	0.774000
#0.010 	0.758000