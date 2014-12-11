'''
Copy of problem1, with window implementation
'''
import numpy as np
from scipy import stats

EUCLIDIAN = 'E' # Euclidian Distance
COSINE = 'C' # Cosine Distance

class KNN:
	def __init__(self,r,dist_fun=EUCLIDIAN,sigma=1e-2):
		self.r = r
		self.norm_mean = None
		self.norm_std = None
		self.sigma = sigma
		self.set_dist_fun(dist_fun)

	def fit(self,pts):
		m,n = pts.shape
		self.points = self.normalize(pts[:,:n-1])
		self.labels = pts[:,n-1]

	def euclidian_distance(self,x1,x2):
		dist = x1 - x2
		return np.dot(dist,dist) # no need to clculate sqrt

	def cosine_distance(self,x1,x2):
		return 1-np.dot(x1,x2)/np.sqrt(np.dot(x1,x1)*np.dot(x2,x2))

	def set_r(self,r):
		self.r = r

	def set_dist_fun(self,dist_fun):
		if dist_fun == COSINE:
			self.dist_fun = self.cosine_distance
		else:
			self.dist_fun = self.euclidian_distance

	def predict(self,pts):
		return map(self.predict_one,self.normalize(pts))

	def predict_one(self,p):
		distances = map(lambda pp: self.dist_fun(p,pp),self.points)
		labels = self.labels[np.array(distances) < self.r]
		if len(labels) == 0:
			return self.labels[np.argsort(distances)][:1]
		return stats.mode(labels)[0][0]	

	def normalize(self,X):
		if self.norm_mean == None and self.norm_std == None:
			self.norm_mean = np.mean(X,axis=0)
			self.norm_std = np.std(X,axis=0)
		return (X-self.norm_mean)/self.norm_std

def digits_knn(knn,r,fun):
	knn.set_r(r)
	knn.set_dist_fun(fun)
	predicted = knn.predict(test_X)
	acc = (predicted==test_y).mean()
	print ' - acc: %f' %acc

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
	knn = KNN(50)
	knn.fit(train)
	predicted = knn.predict(test_X)
	acc = 1-np.logical_xor(predicted,test_y).mean()
	print 'KNN r=50,acc: %f' %acc
	
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
	print 'KNN (r=0.05) with Cosine Distance:'
	digits_knn(knn,0.05,COSINE)
		