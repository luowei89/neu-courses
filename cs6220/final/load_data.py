"""
load_data.py
"""

id_head = "#index"	# publication id header
tt_head = "#*"		# title header
au_head = "#@"		# author header
yr_head = "#t"		# year header
vn_head = "#c"		# venue header
rf_head = "#%"		# refreence header
ab_head = "#!"		# abstract header

TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"
TEST_FILE = "../dm_dataset/AP_train/AP_test_par.txt"

SAMPLE_SIZE = 3000

def feature_extraction(pubs,links):
	D = []
	rand_idx1 = np.random.randint(len(pubs),size=SAMPLE_SIZE)
	froms = np.array(pubs.keys())[rand_idx1]
	rand_idx2 = np.random.randint(len(pubs),size=SAMPLE_SIZE)
	tos = np.array(pubs.keys())[rand_idx2]
	for i in range(SAMPLE_SIZE):
		if froms[i] != tos[i]:
			label = ((froms[i],tos[i]) in links)*1.0
			D.append(get_features(pubs[froms[i]],pubs[tos[i]],label))
	rand_idx3 = np.random.randint(len(links),size=SAMPLE_SIZE)
	links_sample = np.array(links)[rand_idx3]
	for pub,ref in links_sample:
		if pub in pubs and ref in pubs:
			D.append(get_features(pubs[pub],pubs[ref],1.0))
	return np.array(D)

def test_features(test_pub,pubs):
	if test_pub.year == 0:
		test_pub.year = 2013
	D = []
	for p in pubs:
		D.append(get_features(test_pub,pubs[p],1))
	return np.array(D)

def get_features(from_pub,to_pub,label):
	year_diff = to_pub.year - from_pub.year
	if from_pub.year == 0 or to_pub.year == 0:
		year_diff = -5
	if year_diff > 0:
		return get_features(to_pub,from_pub,label)
	coauthor = coauthor_ratio(from_pub.authors,to_pub.authors)
	same_venue = cs.cosine_similarity(from_pub.venue,to_pub.venue)
	from_content = from_pub.title + " " + from_pub.abstract
	to_content = to_pub.title + " " + to_pub.abstract
	cos_similar = cs.cosine_similarity(from_content,to_content)
	return [year_diff,coauthor,same_venue,to_pub.cited,cos_similar,label]

def coauthor_ratio(aus1,aus2):
	if len(aus1) + len(aus2) == 0:
		return 0.0
	count = 0
	for au in aus1:
		if au in aus2:
			count += 1
	return float(count)/(len(aus1)+len(aus2)-count)

def load_data(data_file):
	fdata = open(data_file)
	pubs = {}
	pub_id = -1
	links = []
	for line in fdata:
		if line.startswith(id_head):
			# new publication
			if pub_id != -1:
				pubs[pub_id] = publication
			pub_id = line[len(id_head)+1:].rstrip()
			publication = Publication(pub_id)
		elif line.startswith(tt_head):
			tt_line = line[len(tt_head)+1:].rstrip()
			publication.title = tt_line
		elif line.startswith(au_head):
			au_line = line[len(au_head)+1:].rstrip()
			aus = au_line.split(";")
			publication.authors = aus
		elif line.startswith(yr_head):
			yr_line = line[len(yr_head)+1:].rstrip()
			if yr_line:
				publication.year = int(yr_line)
		elif line.startswith(vn_head):
			venue = line[len(vn_head)+1:].rstrip()
			publication.venue = venue
		elif line.startswith(rf_head):
			ref = line[len(rf_head)+1:].rstrip()
			links.append((pub_id,ref))
		elif line.startswith(ab_head):
			abstract = line[len(ab_head)+1:].rstrip()
			publication.abstract = abstract
	fdata.close()
	if len(links) != 0:
		for pub,ref in links:
			if pub in pubs and ref in pubs:
				pubs[ref].add_cites()
		# assume that the uncited publication won't be cited
		zero_cites = []
		for p in pubs:
			if pubs[p].cited < 10:
				zero_cites.append(p)
		for key in zero_cites:
			del pubs[key]
	return pubs,links

if __name__ == '__main__':
	pubs,links = load_data(TRAIN_FILE)
	print len(pubs)
	D = feature_extraction(pubs,links)
	np.savetxt("data.txt",D)