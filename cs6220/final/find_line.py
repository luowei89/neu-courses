TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"
TEST_FILE = "../dm_dataset/AP_train/AP_test_par.txt"
import database
import publication
import author


def load_data(data_file):
	fdata = open(data_file)
	pubs = set()
	auths = set()
	t_len = []
	v_len = []
	for line in fdata:
		if line.startswith("#index"):
			# new publication
			pub_id = line[len("#index")+1:].rstrip()
			pubs.add(pub_id)
		elif line.startswith("#@"):
			au_line = line[len("#@")+1:].rstrip()
			aus = au_line.split(";")
			for au in aus:
				auths.add(au)
		elif line.startswith("#*"):
			tt_line = line[len("#*")+1:].rstrip()
			t_len.append(len(tt_line))
		elif line.startswith("#c"):
			ve_line = line[len("#c")+1:].rstrip()
			v_len.append(len(ve_line))	
	fdata.close()
	print len(pubs)
	print len(auths)
	print max(t_len)
	print max(v_len)
"""
def load_data(data_file):
	fdata = open(data_file)
	db = database.Database()
	flag = False
	for line in fdata:
		if line.startswith("#index"):
			pub_id = line[len("#index")+1:].rstrip()
			pub = publication.Publication(pub_id)
			flag = pub.exists(db)
		if not flag:
			print line
	fdata.close()

def load_data(data_file):
	fdata = open(data_file)
	db = database.Database()
	flag = False
	for line in fdata:
		line = line.replace("\\","").replace("'","\\'").replace("\"","\\\"")
		if line.startswith("#@"):
			au_line = line[len("#@")+1:].rstrip()
			aus = au_line.split(";")
			for au in aus:
				auth= author.Author(au)
				if not auth.exists(db):
					print au
"""
if __name__ == '__main__':
	load_data(TEST_FILE)