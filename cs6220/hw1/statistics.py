# Know Your Data
import time
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
	print ct
	return authors,pubs,venues

def pubs_per_author(authors):
	return {au:len(authors[au]) for au in authors}

def cites_per_author(authors,pubs):
	return {au:sum(pubs[pub] for pub in authors[au]) for au in authors}

def plot_histogram(dict_nums,filename):

	fig = plt.figure()
	x = dict_nums.keys()
	y = dict_nums.values()
	
	plt.savefig(filename)

# return min max q1 q3 median numbers of the list 
def stat_numbers(dict_nums):
	list_nums = [dict_nums[num] for num in dict_nums]
	n = len(list_nums)
	sorted_list = sorted(list_nums)
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
	#plot_histogram(ppa,"publications_per_author.png")
	print "Time used: %f seconds" %(time.time() - start_time)
	print "========================================"
	print "========================================"
	start_time = time.time()
	print "Citations per author:"
	cpa = cites_per_author(authors,pubs)
	print "min\tmax\tq1\tq3\tmedian"
	print "%d\t%d\t%d\t%d\t%d\t" %stat_numbers(cpa)
	# print "Ploting histogram..."
	# plot_histogram
	print "Time used: %f seconds" %(time.time() - start_time)
	print "========================================"
