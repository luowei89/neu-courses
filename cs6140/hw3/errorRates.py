import numpy as np

def error_rates(predicted,labels):
	total = len(labels)
	tp,fp,tn,fn = 0,0,0,0
	for i in range(total):
		if predicted[i] == 1:
			if labels[i] == 1:
				tp += 1
			else:
				fp += 1
		else:
			if labels[i] == 1:
				fn += 1
			else:
				tn += 1
	error = (fp+fn)/float(total)
	fpr = fp/float(fp+tn)
	fnr = fn/float(tp+fn)
	return np.array([fpr,fnr,error])
