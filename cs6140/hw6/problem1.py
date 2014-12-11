import numpy as np
from sklearn import svm
from scipy import stats

# svm_light
# <line> .=. <target> <feature>:<value> <feature>:<value> ... <feature>:<value> # <info>
def to_svm_light(D,output):
	m,d = D.shape
	output_f = open('svm_light/spambase_%s.dat' %output,'w')
	for line_dat in D:
		line = "%d" %(2*(line_dat[d-1]-0.5))
		for i in range(d-1):
			line = line + " %d:%f" %(i+1,line_dat[i])
		line = line + "\n"
		output_f.write(line)
	output_f.close()

def multi_to_svm_light(D,output):
	m,d = D.shape
	labels = np.unique(D[:,d-1])
	for l in labels:
		files_l = open('svm_light/digits_%s_%d.dat' %(output,l),'w')
		for line_dat in D:
			line = "%d" %(2*((line_dat[d-1]==l)-0.5))
			for i in range(d-1):
				line = line + " %d:%d" %(i+1,line_dat[i])
			line = line + "\n"
			files_l.write(line)	
		files_l.close()

def svm_spambase():
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	k_folds = np.array_split(spambase,10)
	i = int(np.random.rand()*10)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
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
	#clf = svm.SVC(kernel='linear')
	clf = svm.SVC() #rbf kernal
	clf.fit(train_X,train_y)
	predicted = clf.predict(test_X)
	acc = 1-np.logical_xor(predicted,test_y).mean()
	print 'Testing accuracy: %f' %acc
	#to_svm_light(train,"train")
	#to_svm_light(test,"test")

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
			svms[(i,j)] = svm.SVC(kernel='linear')
			#svms[(i,j)] = svm.SVC()
			train_Xi,train_yi = trains[i]
			train_Xj,train_yj = trains[j]
			train_Xij = np.vstack((train_Xi,train_Xj))
			train_yij = np.append(train_yi,train_yj)
			svms[(i,j)].fit(train_Xij,train_yij)
	print "============================================="
	print "Testing..."
	m,d = test.shape
	predicted_matrix = np.zeros((m,len(svms)))
	svm_i = 0
	for i,j in svms:
		predicted_matrix[:,svm_i] = svms[(i,j)].predict(test_X)
		svm_i += 1
	predicted = stats.mode(predicted_matrix,axis=1)[0].T[0]
	print 'Testing accuracy: %f' %((predicted == test_y).mean())
	print "============================================="
	#multi_to_svm_light(train,"train")
	#multi_to_svm_light(test,"test")

if __name__ == '__main__':
	svm_spambase()
	svm_digits()