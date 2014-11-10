"""
Load the AP_train data and save it to DB
"""
import database,publication,author,author_pub,citation

id_head = "#index"	# publication id header
tt_head = "#*"		# title header
au_head = "#@"		# author header
yr_head = "#t"		# year header
vn_head = "#c"		# venue header
rf_head = "#%"		# refreence header
ab_head = "#!"		# abstract header

TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"
TEST_FILE = "../dm_dataset/AP_train/AP_test_par.txt"

def load_data(data_file):
	fdata = open(data_file)
	db = database.Database()
	pub_id = -1
	for line in fdata:
		if line.startswith(id_head):
			# new publication
			if pub_id != -1:
				pub.save(db)
			pub_id = line[len(id_head)+1:].rstrip()
			pub = publication.Publication(pub_id)
		elif line.startswith(tt_head):
			tt_line = line[len(tt_head)+1:].rstrip()
			pub.title = tt_line
		elif line.startswith(au_head):
			au_line = line[len(au_head)+1:].rstrip()
			aus = au_line.split(";")
			for au in aus:
				au_id = author.Author(au).save(db)
				author_pub.AuthorPub(au_id,pub_id).save(db)
		elif line.startswith(yr_head):
			yr_line = line[len(yr_head)+1:].rstrip()
			if yr_line:
				pub.year = int(yr_line)
		elif line.startswith(vn_head):
			venue = line[len(vn_head)+1:].rstrip()
			pub.venue = venue
		elif line.startswith(rf_head):
			ref = line[len(rf_head)+1:].rstrip()
			citation.Citation(pub_id,ref).save(db)
		elif line.startswith(ab_head):
			abstract = line[len(ab_head)+1:].rstrip()
			pub.abstract = abstract
	fdata.close()

if __name__ == '__main__':
	load_data(TRAIN_FILE)