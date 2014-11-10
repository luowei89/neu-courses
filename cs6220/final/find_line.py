TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"
TEST_FILE = "../dm_dataset/AP_train/AP_test_par.txt"

def load_data(data_file):
	fdata = open(data_file)
	for line in fdata:
		if "gtilde" in line:
			print line
			break
	fdata.close()

if __name__ == '__main__':
	load_data(TRAIN_FILE)