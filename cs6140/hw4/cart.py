"""
cart.py from HW1
"""
import node
import numpy

from scipy.stats import mode

def fitTree(tree_node,D,depth,regression,max_depth):
	n = D.shape[1]
	if regression:
		tree_node.prediction = numpy.mean(D[:,n-1])
	else:
		tree_node.prediction = mode(D[:,n-1])[0][0]

	j,t,D_l,D_r = split(D,regression)

	if worthSpliting(depth,D_l,D_r,regression,max_depth):
		tree_node.test = lambda(x): x[j] < t
		tree_node.left = fitTree(node.Node(),D_l,depth+1,regression,max_depth)
		tree_node.right = fitTree(node.Node(),D_r,depth+1,regression,max_depth)
		return tree_node
	else:
		return tree_node

def split(D,regression):
	n = D.shape[1]
	labels = D[:,n-1]
	j,t,min_cost=None,None,float("inf")

	for i in range(n-1):
		threshold,cost = split_by_feature(D[:,i],labels,regression)
		if cost < min_cost:
			j = i
			t = threshold
			min_cost = cost
	x = D[:,j]
	D_l = D[x < t]
	D_r = D[~(x < t)]

	return j,t,D_l,D_r

def split_by_feature(x,y,regression):
	t = numpy.unique(x)
	min_t,min_cost = None,float("inf")

	for i in range(len(t)):
		y_l = y[x < t[i]]
		y_r = y[~(x < t[i])]
		if regression:
			cost = mse_two_parts(y_l,y_r)
		else:
			cost = (len(y_l)*entropy(y_l)+len(y_r)*entropy(y_r))/float(len(y))
		if cost < min_cost:
			min_t = t[i]
			min_cost = cost

	return min_t,min_cost

def mse_two_parts(y_l,y_r):

	sse_l,sse_r = 0,0

	if len(y_l) != 0:
		mean_l = numpy.mean(y_l)
		sse_l = sum([(y-mean_l)**2 for y in y_l])
	if len(y_r) != 0:
		mean_r = numpy.mean(y_r)
		sse_r = sum([(y-mean_r)**2 for y in y_r])

	return (sse_l+sse_r)/(len(y_l)+len(y_r))

def entropy(y):

	if len(y) == 0:
		return 0

	prediction = mode(y)[0][0]
	p = len(y[y==prediction])/float(len(y))

	if p == 0 or p == 1:
		return 0

	entropy = -0.5*p*numpy.log2(p) - 0.5*(1-p)*numpy.log2(1-p)
	return entropy

def worthSpliting(depth,D_l,D_r,regression,max_depth):
	return depth < max_depth and len(D_l) > 0 and len(D_r) > 0

def predict(X,tree):
	return numpy.apply_along_axis(predict_per_row,1,X,tree)

def predict_per_row(x,tree_node):
	if tree_node.test == None:
		return tree_node.prediction
	else:
		if tree_node.test(x):
			return predict_per_row(x,tree_node.left)
		else:
			return predict_per_row(x,tree_node.right)
