# Know Your Data
import time
import numpy as np
import matplotlib.pyplot as plt

DTAT_FILE = "../dm_dataset/AP_train.txt"

id_head = "#index"	# publication id header
au_head = "#@"		# author header
rf_head = "#%"		# refreence header
vn_head = "#c"		# venue header

def readData(filename):
	# open the data file
	fdata = open(filename)
	# key: author_name, value: list of pub_ids
	authors = {}
	# key: pub_id, value: number of cites
	pubs = {}
	# a set of venues string
	venues = set()
	for line in fdata:
		if line.startswith(id_head):
			pub_id = line[len(id_head)+1:].rstrip()
			if not pub_id in pubs:
				pubs[pub_id] = 0
		elif line.startswith(au_head):
			au_line = line[len(au_head)+1:].rstrip()
			if au_line: # no author
				aus = au_line.split(";")
				for au in aus:
					if au in authors:
						authors[au].append(pub_id)
					else:
						authors[au] = [pub_id]
		elif line.startswith(rf_head):
			ref = line[len(rf_head)+1:].rstrip()
			if ref in pubs:
				pubs[ref] = pubs[ref]+1
			else:
				pubs[ref] = 1
		elif line.startswith(vn_head):
			venue = line[len(vn_head)+1:].rstrip()
			venues.add(venue)
	fdata.close()
	return authors,pubs,venues

def pubs_per_author(authors):
	return [len(authors[au]) for au in authors]

def cites_per_author(authors,pubs):
	return [sum(pubs[pub] for pub in authors[au]) for au in authors]

def plot_histogram(nums,xstep,title):
	x = ceil(max(nums)/xstep*1.0)*xstep
	plt.clf()
	plt.hist(nums,x/xstep,bottom=0.1)
	plt.yscale('log')
	plt.title(title)
	plt.savefig("%s.png" %title)

def plot_scatter(ppa,cpa):
	x = np.array(ppa)
	y = np.array(cpa)
	x5 = x[x[:]>5]
	y5 = y[x[:]>5]
	plt.clf()
	plt.scatter(x5,y5,s=5)
	plt.xlabel("number of publications")
	plt.ylabel("number of citations")
	plt.savefig("num_pubs_vs_num_cites.png")

def ceil(x):
	if x == int(x):
		return x
	else:
		return int(x)+1
# return min max q1 q3 median numbers of the list 
def stat_numbers(nums):
	n = len(nums)
	sorted_list = sorted(nums)
	return sorted_list[0],sorted_list[n-1],sorted_list[n/4],sorted_list[n*3/4],sorted_list[n/2],

if __name__ == '__main__':

	print "========================================"
	start_time = time.time()
	print "Loading data..."
	authors,pubs,venues = readData(DTAT_FILE)
	print "Number of authors: %d" %len(authors)
	print "Number of publications: %d" %len(pubs)
	print "Number of venues: %d" %len(venues)
	print "Time used: %f seconds" %(time.time() - start_time)
	print "========================================"
	start_time = time.time()
	print "Publications per author:"
	ppa = pubs_per_author(authors)
	print "min\tmax\tq1\tq3\tmedian"
	print "%d\t%d\t%d\t%d\t%d\t" %stat_numbers(ppa)
	print "Ploting histogram..."
	plot_histogram(ppa,100,"publications_per_author")
	print "Time used: %f seconds" %(time.time() - start_time)
	print "========================================"
	print "========================================"
	start_time = time.time()
	print "Citations per author:"
	cpa = cites_per_author(authors,pubs)
	print "min\tmax\tq1\tq3\tmedian"
	print "%d\t%d\t%d\t%d\t%d\t" %stat_numbers(cpa)
	print "Ploting histogram..."
	plot_histogram(cpa,1000,"citations_per_author")
	print "Time used: %f seconds" %(time.time() - start_time)
	print "========================================"
	print "Ploting scatter plot..."
	plot_scatter(ppa,cpa)
	print "========================================"