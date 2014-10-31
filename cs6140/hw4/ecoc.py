import numpy as np
import ada_boosting as ab
import time

def load_data(data_name):
	config_file = "../dataset/8newsgroup/%s.trec/config.txt" %data_name
	data_file = "../dataset/8newsgroup/%s.trec/feature_matrix.txt" %data_name

	config = read_config(config_file)
	m,d = config['numDataPoints'],config['numFeatures']
	return read_data(data_file,m,d)

def read_config(config_file):
	config = {}
	f = open(config_file)
	for line in f:
		if not line.startswith('#'):
			key,value = line.rstrip().split('=')
			config[key] = int(value)
	return config

def read_data(data_file,m,d):
	D = np.zeros((m,d+1))
	f = open(data_file)
	data_id = 0
	for line in f:
		data_i = read_data_line(line,d)
		for fid in data_i:
			D[data_id][fid] = data_i[fid]
		data_id += 1
	return D

def read_data_line(line,d):
	data = {}
	values = line.rstrip().split(' ')
	data[d] = int(values[0])
	for s in values[1:]:
		key,value = s.split(':')
		data[int(key)] = float(value)
	return data

def exhaustive_codes(num):
	funs = 2**(num-1)-1
	codes = np.zeros((num,funs))
	for i in range(funs):
		codes[:,i] = list(("{0:0%sb}" %num).format(2**num-i-2))
	return codes

def reduce_codes(codes,size):
	n,f = codes.shape
	rand_idx = np.random.randint(f,size=size)
	return codes[:,rand_idx]

def ecoc_predict(test_X,predictors,codes):
	nc = len(predictors)
	m,d = test_X.shape
	output_matrix = np.zeros((m,nc))
	for i in range(nc):
		output_matrix[:,i] = ab.ada_predict(test_X,predictors[i])
	output_matrix = output_matrix/2.0 + 0.5
	return np.array([min_distance(codes,om) for om in output_matrix])

def min_distance(a,item):
	dist = np.inf
	min_i = -1
	for i in range(len(a)):
		dist_i = np.sum(abs(a[i] - item))
		if dist_i < dist:
			dist = dist_i
			min_i = i
	return min_i

def ecoc(train,test,num_classes):
	codes = exhaustive_codes(num_classes)
	codes = reduce_codes(codes,20)
	funs = codes.shape[1]
	m,d = train.shape
	train_y = np.copy(train[:,d-1])
	test_y = np.copy(test[:,d-1])
	predictors = {}
	threads = []
	for i in range(funs):
		s = time.time()
		train[:,d-1] = [codes[y,i] for y in train_y]
		test[:,d-1] = [codes[y,i] for y in test_y]
		predictors[i] = ab.ada_boosting(train,test)
		print "function %d, time %fs" %(i,time.time()-s)
	print ecoc_accuracy(ecoc_predict(test[:,:d-1],predictors,codes),test_y)

def ecoc_accuracy(predicted,y):
	return np.sum(predicted==y)/float(len(y))

if __name__ == '__main__':
	
	train = load_data("train")
	test = load_data("test")
	ecoc(train,test,8)
	"""
	codes = exhaustive_codes(8)
	print codes
	codes = reduce_codes(codes,20)
	for i in range(len(codes)):
		for j in range(i+1,len(codes)):
			print np.sum(abs(codes[i]-codes[j]))
	"""