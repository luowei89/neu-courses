"""
real_world_cluster.py
"""
import heapq
import numpy as np
import k_means as km
import cluster_analysis as ca

id_head = "#index"	# publication id header
tt_head = "#*"		# title header
au_head = "#@"		# author header
yr_head = "#t"		# year header
vn_head = "#c"		# venue header
rf_head = "#%"		# refreence header
ab_head = "#!"		# abstract header

TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"

conferences = ['IJCAI','AAAI','ICDE','VLDB','SIGMOD','SIGIR','ICML','NIPS','CIKM','KDD','WWW','PAKDD','PODS','ICDM','ECML','PKDD','EDBT','SDM','ECIR','WSDM']
kdd_i = 9
pakdd_i = 11
pkdd_i = 15
sdm_i = 17
wsdm_i = 19
ground_truth_label = np.array([3,3,1,1,1,4,3,3,4,2,4,2,1,2,3,2,1,2,4,4])

def load_data(data_file):
	fdata = open(data_file)
	pubs = {}
	for line in fdata:
		if line.startswith(id_head):
			# new publication
			pub_id = line[len(id_head)+1:].rstrip()
			pubs[pub_id] = {}
		elif line.startswith(au_head):
			au_line = line[len(au_head)+1:].rstrip()
			aus = au_line.split(";")
			pubs[pub_id]['authors'] = aus
		elif line.startswith(vn_head):
			venue = line[len(vn_head)+1:].rstrip()
			pubs[pub_id]['venue'] = venue
	fdata.close()
	return pubs

def top_authors(pubs):
	authors = {}
	for p in pubs:
		aus = pubs[p]['authors']
		venue = pubs[p]['venue']
		if useful_venue(venue):
			for au in aus:
				if au in authors:
					authors[au] = authors[au] + 1
				else :
					authors[au] = 1
	top_num = len(authors)/10
	return heapq.nlargest(top_num, authors)

def useful_venue(venue):
	for cfs in conferences:
		if cfs in venue:
			return True
	return False

def extract_features(pubs,authors):
	m = len(conferences)
	n = len(authors)
	X = np.zeros((m,n))
	for p in pubs:
		aus = pubs[p]['authors']
		venue = pubs[p]['venue']
		for i in range(m):
			if conferences[i] in venue:
				for j in range(n):
					if authors[j] in aus:
						X[i][j] = X[i][j] + 1
	# remove duplicate
	X[kdd_i] = X[kdd_i] - X[pakdd_i] - X[pkdd_i]
	X[sdm_i] = X[sdm_i] - X[wsdm_i]
	return X

def member_print(mem):
	for m in mem:
		for i in range(len(m)):
			if m[i] == 1:
				print i+1

if __name__ == '__main__':
	pubs = load_data(TRAIN_FILE)
	top_aus = top_authors(pubs)
	X = extract_features(pubs,top_aus)
	member = km.k_means(X,4)
	#member_print(member)
	print "Purity is %f" %ca.purity(ground_truth_label,member)
	print "NMI is %f" %ca.nmi(ground_truth_label,member)