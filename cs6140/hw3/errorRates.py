import numpy as np

def error_rates(predicted,labels):
	tp,fp,tn,fn = confusion_matrix(predicted,labels)
	error = (fp+fn)/float(len(labels))
	fpr = fp/float(fp+tn)
	fnr = fn/float(tp+fn)
	return np.array([fpr,fnr,error])

def tp_fp_rates(predicted,labels):
	tp,fp,tn,fn = confusion_matrix(predicted,labels)
	tpr = tp/float(tp+fn)
	fpr = fp/float(fp+tn)
	return tpr,fpr

def confusion_matrix(predicted,labels):
	tp,fp,tn,fn = 0,0,0,0
	for i in range(len(labels)):
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
	return tp,fp,tn,fn