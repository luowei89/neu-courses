import numpy as np
from scipy import stats

EUCLIDIAN = 'E' # Euclidian Distance
COSINE = 'C' # Cosine Distance
GAUSSIAN = 'G' # Gaussian Kernel
PLYNOMIAL = 'P' # Plynomial Degree-2 Kernel

class KNN:
	def __init__(self,k,dist_fun=EUCLIDIAN,sigma=1.2):
		self.k = k
		self.sigma=sigma
		self.norm_mean = None
		self.norm_std = None
		self.set_dist_fun(dist_fun)

	def fit(self,pts):
		m,n = pts.shape
		self.points = self.normalize(pts[:,:n-1])
		self.labels = pts[:,n-1]

	def euclidian_distance(self,x1,x2):
		dist = x1 - x2
		return np.dot(dist,dist) # no need to clculate sqrt

	def cosine_distance(self,x1,x2):
		return -np.dot(x1,x2)/np.sqrt(np.dot(x1,x1)*np.dot(x2,x2))

	def gaussian_kernel(self,x1,x2):
		diff = x1 - x2
		return -np.exp(-0.5*np.dot(diff,diff)/np.square(self.sigma))

	def plynomial_kernel(self,x1,x2):
		return -np.square(np.dot(x1,x2)+100)

	def set_k(self,k):
		self.k = k

	def set_dist_fun(self,dist_fun):
		if dist_fun == COSINE:
			self.dist_fun = self.cosine_distance
		elif dist_fun == GAUSSIAN:
			self.dist_fun = self.gaussian_kernel
		elif dist_fun == PLYNOMIAL:
			self.dist_fun = self.plynomial_kernel
		else:
			self.dist_fun = self.euclidian_distance

	def predict(self,pts):
		return map(self.predict_one,self.normalize(pts))

	def predict_one(self,p):
		distances = [self.dist_fun(p,pp) for pp in self.points]#map(lambda pp: self.dist_fun(p,pp),self.points)
		labels = self.labels[np.argsort(distances)][:self.k]
		return stats.mode(labels)[0][0]	

	def normalize(self,X):
		if self.norm_mean == None and self.norm_std == None:
			self.norm_mean = np.mean(X,axis=0)
			self.norm_std = np.std(X,axis=0)
		return (X-self.norm_mean)/self.norm_std

def digits_knn(knn,k,fun):
	knn.set_k(k)
	knn.set_dist_fun(fun)
	predicted = knn.predict(test_X)
	acc = (predicted==test_y).mean()
	print ' - k=%d,acc: %f' %(k,acc)	

if __name__ == '__main__':
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	k_folds = np.array_split(spambase,10)
	i = int(np.random.rand()*10)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	d = test.shape[1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	print "============================================="
	knn = KNN(3)
	knn.fit(train)
	predicted = knn.predict(test_X)
	acc = 1-np.logical_xor(predicted,test_y).mean()
	print 'KNN k=3,acc: %f' %acc
	knn.set_k(5)
	predicted = knn.predict(test_X)
	acc = 1-np.logical_xor(predicted,test_y).mean()
	print 'KNN k=5,acc: %f' %acc	
	knn.set_k(7)
	predicted = knn.predict(test_X)
	acc = 1-np.logical_xor(predicted,test_y).mean()
	print 'KNN k=7,acc: %f' %acc	
	print "============================================="
	print "loading digits data..."
	train = np.loadtxt("../hw5/digits/train_20.txt")
	test = np.loadtxt("../hw5/digits/test.txt")
	# ===== normalize =====
	d = train.shape[1]
	test_X = test[:,:d-1]
	test_y = test[:,d-1]
	print "============================================="
	knn = KNN(1)
	knn.fit(train)
	print 'KNN with Cosine Distance:'
	digits_knn(knn,1,COSINE)
	digits_knn(knn,3,COSINE)
	digits_knn(knn,7,COSINE)
	print "============================================="
	print 'KNN with Gaussian Kernel:'
	digits_knn(knn,1,GAUSSIAN)
	digits_knn(knn,3,GAUSSIAN)
	digits_knn(knn,7,GAUSSIAN)
	print "============================================="
	print 'KNN with Plynomial Degree-2 Kernel:'
	digits_knn(knn,1,PLYNOMIAL)
	digits_knn(knn,3,PLYNOMIAL)
	digits_knn(knn,7,PLYNOMIAL)

		