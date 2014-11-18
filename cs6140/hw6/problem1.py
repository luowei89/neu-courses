import numpy as np

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
				line = line + " %d:%f" %(i+1,line_dat[i])
			line = line + "\n"
			files_l.write(line)	
		files_l.close()

def load_data_spambase():
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)
	k_folds = np.array_split(spambase,10)
	i = int(np.random.rand()*10)
	test = k_folds[i]
	train = np.vstack(np.delete(k_folds, i, axis=0))
	to_svm_light(train,"train")
	to_svm_light(test,"test")

def load_data_digits():
	train = np.loadtxt("../hw5/digits/train_20.txt")
	test = np.loadtxt("../hw5/digits/test.txt")
	multi_to_svm_light(train,"train")
	multi_to_svm_light(test,"test")

if __name__ == '__main__':
	#load_data_spambase()
	load_data_digits()