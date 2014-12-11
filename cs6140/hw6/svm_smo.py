import numpy as np
import time
C = 1

def svm_learn(D):
	m,n = D.shape
	X = D[:,:n-1]
	y = 2*(D[:,n-1]-0.5)

	alpha = np.zeros(m)
	b = 0.0
	updates = m
	while updates > 0:
		updates = 0
		old_b = b
		for i in range(m):
			fxi = f(X[i],alpha,X,y,b)
			yf = y[i]*fxi
			if (alpha[i] == 0 and yf < 1) or (alpha[i] == C and yf > 1):
				Ei = fxi - y[i]
				max_diffE = -1
				for j in range(m):
					Ej = f(X[j],alpha,X,y,b)-y[j]
					diffE = abs(Ei-Ej)
					if diffE > max_diffE:
						max_diffE = diffE
						max_index = j
						max_Ej = Ej
				j = max_index
				Ej = max_Ej
				Kii,Kjj,Kij = K(X[i],X[i]),K(X[j],X[j]),K(X[i],X[j])
				eta = Kii + Kjj - 2 * Kij
				alphai_old = alpha[i]
				alphaj_old = alpha[j]
				alpha[j] = alpha[j] + y[j]*(Ei-Ej)/eta
				alpha[j] = clip_alphaj(alpha[i],alpha[j],y[i],y[j])
				alpha[i] = alpha[i] + y[i]*y[j]*(alphaj_old-alpha[j])
				last_term = (alphai_old-alpha[i])*y[i]*Kii+(alphaj_old-alpha[i])*y[j]*Kij
				b = new_b(b,alpha[i],alpha[j],Ei,Ej,last_term)
				updates += 1
		print updates
		if old_b == b:
			break
	return X,y,alpha,b

def svm_predict(X,svm_X,svm_y,alpha,b):
	return np.array([f(x,alpha,svm_X,svm_y,b) > 0 for x in X])

def K(x1,x2):
	return np.dot(x1,x2)

def f(xi,alpha,X,y,b):
	return np.dot(alpha*y,K(X,xi)) + b

def clip_alphaj(alphai,alphaj,yi,yj):
	if yi == yj:
		L = max(0,alphaj-alphai)
		H = min(C,alphaj-alphai+C)
	else:
		L = max(0,alphai+alphaj-C)
		H = min(C,alphai+alphaj)

	if alphaj < L:
		return L
	elif alphaj > H:
		return H
	else:
		return alphaj

def new_b(b,ai,aj,Ei,Ej,last_term):
	bi = b - Ei + last_term
	bj = b - Ej + last_term
	if ai > 0 and ai < C:
		return bi
	elif aj > 0 and aj < C:
		return bj
	else:
		return (bi+bj)/2

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
	svm_X,svm_y,alpha,b = svm_learn(train)
	predicted = svm_predict(test_X,svm_X,svm_y,alpha,b)
	print np.mean((predicted - test_y)**2)
