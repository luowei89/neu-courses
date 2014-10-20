import numpy as np
id_head = "#index"	# publication id header

TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"
TEST_FILE = "../dm_dataset/AP_train/AP_test_par.txt"

def get_pubs(file_name):
	pubs = []
	fdata = open(file_name)
	for line in fdata:
		if line.startswith(id_head):
			pub_id = line[len(id_head)+1:].rstrip()
			pubs.append(pub_id)
	fdata.close()
	return np.array(pubs)

def guess(file_name,pubs):
	print "Id,References"
	fdata = open(file_name)
	for line in fdata:
		if line.startswith(id_head):
			print_str = ""
			pub_id = line[len(id_head)+1:].rstrip()
			print_str += "%s," %pub_id
			rand_inx = np.random.randint(len(pubs),size=10)
			rand_pubs = pubs[rand_inx]
			for p in rand_pubs:
				print_str += " %s" %p
			print print_str
	fdata.close()

if __name__ == '__main__':
	pubs = get_pubs(TRAIN_FILE)
	guess(TEST_FILE,pubs)