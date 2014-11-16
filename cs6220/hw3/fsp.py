"""
find frequent squential patterns.
"""
import fim,codecs
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def get_transactions(file_name):
	file_2001 = codecs.open(file_name,'r',encoding='utf8')
	transactions = []
	for line in file_2001:
		line = line.lower()
		line = line.replace('-',' ')
		line = line.replace('/',' ')
		line = line.replace('"',' ')
		transactions.append([w for w in word_tokenize(line) if valid_word(w)])
	return transactions

def valid_word(w):
	return w not in stopwords.words('english') and len(w) > 1 and not w.isdigit()

def print_top_n(d,n):
	top_n = sorted(d.iteritems(), key=lambda(k,v):(-v,k))[:n]
	for words in top_n:
		print '<' + ' '.join([w for w in words[0]]) + '>' + (' :%d' %words[1])
	
def find_by_year(years):
	print 'For year %s:' %years
	t_years = get_transactions('%s.csv' %years)
	report_years = fim.apriori(t_years,supp=8,conf=0,zmax=4)
	result_years = {}
	for i in range(1,5):
		result_years[i] = {}
	for words,counts in report_years:
		result_years[len(words)][words] = counts[0]
	for i in result_years:
		print 'Top 20 most frequent patterns with length %d' %i
		print_top_n(result_years[i],20)	

if __name__ == '__main__':
	find_by_year('2001-2005')
	print ''
	find_by_year('2008-2012')