"""
feature analysis
"""
import numpy as np
import ada_boosting as ab

def feature_analysis(dataset,num_top_feat):
	k_folds = np.array_split(dataset,10)
	i = int(np.random.rand()*10)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	wwls = ab.ada_boosting(dataset)
	sum_margins_f = {}
	for alpha,feat,thresh in wwls:
		sum_margins_f[feat] = 0
	for x in dataset:
		sum_margins_f = margin_f(x,wwls,sum_margins_f)
	return sorted(sum_margins_f.keys(), key=sum_margins_f.get, reverse=True)[:num_top_feat]

def margin_f(x,wwls,sum_margins_f):
	numerator = {}
	for alpha,feat,thresh in wwls:
		if feat not in numerator:
			numerator[feat] = 0
		numerator[feat] += alpha*2*((x[feat] > thresh) - 0.5)
	for feature in sum_margins_f:
		sum_margins_f[feature] += 2*(x[-1]- 0.5)*numerator[feature]
	return sum_margins_f

def spambase_feature_analysis():
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	print "============================================="
	top_10 = feature_analysis(spambase,10)
	print "Top 10 features are:"
	print top_10

def bosting_bad_feautres():
	print "============================================="
	print "loading spambase polluted data..."
	train_X = np.loadtxt("../dataset/spam_polluted/train_feature.txt")
	train_y = np.loadtxt("../dataset/spam_polluted/train_label.txt")
	test_X = np.loadtxt("../dataset/spam_polluted/test_feature.txt")
	test_y = np.loadtxt("../dataset/spam_polluted/test_label.txt")
	print "============================================="
	print "Train with ada boosting..."
	train = np.array(np.hstack((train_X,np.matrix(train_y).T)))
	test = np.array(np.hstack((test_X,np.matrix(test_y).T)))
	wwls = ab.ada_boosting(train)
	accuracy = np.sum((ab.ada_predict(test_X,wwls)/2.0 + 0.5)==test_y)/float(len(test_y))
	print "Accuracy is %f" %accuracy

if __name__ == '__main__':
	spambase_feature_analysis()
	bosting_bad_feautres()