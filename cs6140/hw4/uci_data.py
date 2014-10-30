import numpy as np
import ada_boosting as ab
import matplotlib.pyplot as plt
K = 10

def data_path(data_set):
	return "../dataset/%s/%s.data" %(data_set,data_set),"../dataset/%s/%s.config" %(data_set,data_set)

def parse_data(data_file,config_file):
	D = np.loadtxt(data_file,dtype='str')
	D = D[np.array(['?' not in d for d in D])]
	con_file = open(config_file)
	lines = np.array([line.rstrip().split('\t') for line in con_file])
	con_file.close()
	for i in range(int(lines[0][1])+int(lines[0][2])+1):
		if lines[i+1][0] != '-1000':
			labels = lines[i+1][1:]
			np.random.shuffle(labels)
			label_dict = {}
			for l in range(len(labels)):
				label_dict[labels[l].strip()] = l
			D[:,i] = np.array([label_dict[d] for d in D[:,i]])
	return D.astype(float)

def k_folds_test(data_set):
	print "================================================================================"
	print "Boosting on %s dataset with %d folds cross-validation." %(data_set,K)
	data,config = data_path(data_set)
	D = parse_data(data,config)
	np.random.shuffle(D)
	k_folds = np.array_split(D,K)
	errors = np.zeros(K)
	for i in range(K):
		print "================================================================================"
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))
		wwls = ab.ada_boosting(train,test)
		d = test.shape[1]
		errors[i] = ab.error_rate(ab.ada_predict(test[:,:d-1],wwls),test[:,d-1])
		print "================================================================================"
		print "Fold %d, accuracy %f" %(i,1-errors[i])
	print "================================================================================"
	print "Average accuracy for %s, %f" %(data_set,1-np.mean(errors))
	print "================================================================================"

def train_with_sample(data_set):
	c_values = [5,10,15,20,30,50,80]
	data,config = data_path(data_set)
	D = parse_data(data,config)
	#np.random.shuffle(D)
	k_folds = np.array_split(D,10)
	i = int(np.random.rand()*10)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	d = test.shape[1]
	errs = []
	for c in c_values:
		print "================================================================================"
		print "Training on %s dataset with %d%% samples." %(data_set,c)
		train_c = train[np.random.randint(len(train),size=c*len(train)/90)]
		wwls = ab.ada_boosting(train_c,test)
		err = ab.error_rate(ab.ada_predict(test[:,:d-1],wwls),test[:,d-1])
		print "================================================================================"
		print "Accuracy with %d%% samples (%s) is %f." %(c,data_set,1-err)
		errs.append(err)
	plt.clf()
	plt.plot(c_values,errs)
	plt.savefig("p2_err.png")

if __name__ == '__main__':
	#binary_label_datasets = ["crx","vote","band","agr","monk","tic"]
	#for ds in binary_label_datasets:
	#	k_folds_test(ds)
	k_folds_test("crx")
	k_folds_test("vote")
	train_with_sample("crx")
	train_with_sample("vote")