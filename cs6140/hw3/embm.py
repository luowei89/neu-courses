"""
EM for Coin Flip (Bernoulli Mixture)
"""
import numpy as np
import copy

K = 10
M = 1000
COIN = [0,1]
MAX_ITER = 500
TOL = 1e-4

def flip_coin(num_coins,pi,probs):
	flips = np.zeros((M,K))
	print "fliping %d coins..." %num_coins
	for i in range(M):
		coin_head = pick_with_prob(probs,pi) # pick a coin
		for j in range(K):
			flips[i][j] = pick_with_prob(COIN,[1-coin_head,coin_head]) # flip the coin
	return flips

def pick_with_prob(array,probs):
	random = np.random.rand()
	for i in range(len(probs)):
		if random < probs[i]:
			break
		random -= probs[i]
	return array[i]

def embm(X,num_coins):
	print "recovering parameters..."
	params = random_init(X,num_coins)
	for i in range(MAX_ITER):
		old_p = copy.deepcopy(params)
		params = expectation(X,params)
		params = maximization(X,params)
		if converge(old_p,params):
			print "converged after %d iterations" %i
			break
	return params

def converge(old,new):
	conv_pi = np.sum(np.abs(old['pi'] - new['pi'])) < TOL
	conv_probs = np.sum(np.abs(old['probs'] - new['probs'])) < TOL
	conv_z = np.sum(np.abs(old['z'] - new['z'])) < TOL
	return conv_pi and conv_probs and conv_z

def random_init(X,k):
	m = len(X)
	params = {}
	params['z'] = np.zeros((m,k))	
	for i in range(m):
		index = int(np.random.rand()*k)
		params['z'][i][index] = 1
	params['pi'] = np.sum(params['z'],axis=0)/np.sum(params['z'])
	params['probs'] = np.random.random(k)
	return params

def expectation(X,params):
	pi = params['pi']
	probs = params['probs']
	m,d = X.shape
	n = len(pi)
	for i in range(m):
		for j in range(n):
			params['z'][i][j] = pi[j]*probability(X[i],probs[j])
		params['z'][i] = params['z'][i]/np.sum(params['z'][i])
	return params

def probability(x,p):
	return np.prod([p**xi*(1-p)**(1-xi) for xi in x])

def maximization(X,params):
	z = params['z']
	m,d = X.shape
	k = len(z[0])
	for i in range(k):
		prob = 0
		prob_base = 0
		count = 0
		for j in range(m):
			prob += z[j][i]*sum(X[j])
			prob_base += z[j][i]*d
			count += z[j][i]
		params['probs'][i] = prob/prob_base
		params['pi'][i] = count/m
	return params

def print_params(params):
	print "pi:"
	print params['pi']
	print "probablities:"
	print params['probs']

def random_parameters(num_coins):
	pi = np.random.rand(num_coins)
	pi = pi/np.sum(pi)
	probs = np.random.rand(num_coins)
	return pi,probs

if __name__ == "__main__":
	print "============================================="
	flips = flip_coin(2,[0.8,0.2],[0.75,0.4])
	recovered = embm(flips,2)
	print_params(recovered)
	print "============================================="
	flips = flip_coin(2,[0.4,0.6],[0.9,0.2])
	recovered = embm(flips,2)
	print_params(recovered)
	print "============================================="
	flips = flip_coin(2,[0.1,0.9],[0.45,0.51])
	recovered = embm(flips,2)
	print_params(recovered)
	print "============================================="
	flips = flip_coin(3,[0.2,0.3,0.5],[0.99,0.47,0.08])
	recovered = embm(flips,3)
	print_params(recovered)
	print "============================================="
	flips = flip_coin(5,[0.1,0.1,0.2,0.3,0.3],[0.98,0.69,0.38,0.21,0.03])
	recovered = embm(flips,5)
	print_params(recovered)
	print "============================================="