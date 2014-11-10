import random, time
import numpy as np
import ada_boosting as ab

TEST_OFFSET = 8
TRAIN_OFFSET = 16
IMAGE_SIZE = 28
COLOR_THRESHOLD = 255/2
TRAIN_SIZE = 60000
TEST_SIZE = 10000
NUM_RECTS = 100

def read_file():
	train_labels = np.fromfile("../dataset/digits/train-labels-idx1-ubyte",dtype=np.dtype('u1'))[TEST_OFFSET:]
	np.savetxt("digits/train_labels.txt",train_labels,fmt='%i')
	test_labels = np.fromfile("../dataset/digits/t10k-labels-idx1-ubyte",dtype=np.dtype('u1'))[TEST_OFFSET:]
	np.savetxt("digits/test_labels.txt",test_labels,fmt='%i')
	train_data = np.fromfile("../dataset/digits/train-images-idx3-ubyte",dtype=np.dtype('u1'))[TRAIN_OFFSET:]
	train_data = (train_data > COLOR_THRESHOLD).astype(int)
	train_data = np.split(train_data,TRAIN_SIZE)
	np.savetxt("digits/train_data.txt",train_data,fmt='%i')
	test_data = np.fromfile("../dataset/digits/t10k-images-idx3-ubyte",dtype=np.dtype('u1'))[TRAIN_OFFSET:]
	test_data = (test_data > COLOR_THRESHOLD).astype(int)
	test_data = np.split(test_data,TEST_SIZE)
	np.savetxt("digits/test_data.txt",test_data,fmt='%i')

def extract_features():
	rects = [random_rectangle() for i in range(NUM_RECTS)]
	while len(set(rects)) < NUM_RECTS:
		rects = [random_rectangle() for i in range(NUM_RECTS)]
	train_data = np.loadtxt("digits/train_data.txt")
	train_labels = np.loadtxt("digits/train_labels.txt")
	train = np.zeros((TRAIN_SIZE,2*NUM_RECTS+1))
	for i in range(TRAIN_SIZE):
		train[i,:2*NUM_RECTS] = get_features(train_data[i],rects)
		train[i,2*NUM_RECTS] = train_labels[i]
	np.savetxt("digits/train.txt",train,fmt='%i')
	test_data = np.loadtxt("digits/test_data.txt")
	test_labels = np.loadtxt("digits/test_labels.txt")
	test = np.zeros((TEST_SIZE,2*NUM_RECTS+1))
	for i in range(TEST_SIZE):
		test[i,:2*NUM_RECTS] = get_features(test_data[i],rects)
		test[i,2*NUM_RECTS] = test_labels[i]
	np.savetxt("digits/test.txt",test,fmt='%i')

def get_features(data,rects):
	blacks = {}
	blacks[(-1,-1)] = 0
	for i in range(IMAGE_SIZE):
		blacks[(-1,i)] = 0
		blacks[(i,-1)] = 0
	for i in range(IMAGE_SIZE):
		for j in range(IMAGE_SIZE):
			blacks[(i,j)] = blacks[(i,j-1)] + blacks[(i-1,j)] - blacks[(i-1,j-1)] + data[i*IMAGE_SIZE+j]
	features = np.zeros(2*NUM_RECTS)
	for i in range(NUM_RECTS):
		lt_x,lt_y,rb_x,rb_y = rects[i]
		mid_x = (lt_x+rb_x)/2
		mid_y = (lt_y+rb_y)/2
		left = lt_x,lt_y,rb_x,mid_y
		right = lt_x,mid_y+1,rb_x,rb_y
		top = lt_x,lt_y,mid_x,rb_y
		bottom = mid_x+1,lt_y,rb_x,rb_y
		features[i*2] = blacks_in_rect(left,blacks) - blacks_in_rect(right,blacks)
		features[i*2+1] = blacks_in_rect(top,blacks) - blacks_in_rect(bottom,blacks)
	return features

def blacks_in_rect(rect,blacks):
	lt_x,lt_y,rb_x,rb_y = rect
	return blacks[(rb_x,rb_y)] - blacks[(lt_x-1,rb_y)] - blacks[(rb_x,lt_y-1)] + blacks[(lt_x-1,lt_y-1)]

def random_rectangle():
	# return a random rectangle with 130-170 area, each side at least 5
	lt_x,lt_y,rb_x,rb_y = 0,0,0,0
	while (rb_x - lt_x) * (rb_y - lt_y) < 130 or (rb_x - lt_x) * (rb_y - lt_y) > 170:
		lt_x = np.random.randint(IMAGE_SIZE-5)
		lt_y = np.random.randint(IMAGE_SIZE-5)
		rb_x = lt_x + np.random.randint(IMAGE_SIZE-lt_x-5) + 5
		rb_y = lt_y + np.random.randint(IMAGE_SIZE-lt_y-5) + 5
	return (lt_x,lt_y,rb_x,rb_y)

def ecoc_image():
	print "============================================="
	print "loading image features..."
	train = np.loadtxt("digits/train.txt")
	test = np.loadtxt("digits/test.txt")
	print "============================================="
	ecoc(train,test,len(np.unique(test[:,test.shape[1]-1])))

def exhaustive_codes(num):
	funs = 2**(num-1)-1
	codes = np.zeros((num,funs))
	for i in range(funs):
		codes[:,i] = list(("{0:0%sb}" %num).format(2**num-i-2))
	return codes

def reduce_codes(codes,size):
	rand_idx = random.sample(range(codes.shape[1]),size)
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
	codes = reduce_codes(codes,50)
	funs = codes.shape[1]
	m,d = train.shape
	train_y = np.copy(train[:,d-1])
	test_y = np.copy(test[:,d-1])
	predictors = {}
	for i in range(funs):
		s = time.time()
		train[:,d-1] = [codes[y,i] for y in train_y]
		test[:,d-1] = [codes[y,i] for y in test_y]
		predictors[i] = ab.ada_boosting(train)
		print "function %d, time %fs" %(i,time.time()-s)
	correct = np.sum(ecoc_predict(test[:,:d-1],predictors,codes)==test_y)
	print "Accuracy is %f" %(correct/float(m))

if __name__ == '__main__':
	"step 1. read the file and store it as numpy txt"
	#read_file()
	"step 2. load the txt files and extract feature and save it as txt"
	#extract_features()
	"step 3. run ecoc with extracted features"
	ecoc_image()
