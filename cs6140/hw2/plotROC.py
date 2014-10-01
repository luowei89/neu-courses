import numpy as np
import matplotlib.pyplot as plt
import confusionMatrix as cm

# rtype is one of "Linear", "Logistic"
def plotROC(X,y,w,rtype):
	
	y_predict = np.dot(X,w)
	t = np.unique(y_predict)
	t = np.append(t,np.max(y_predict)+1)

	tprs,fprs = np.zeros(len(t)),np.zeros(len(t))

	for i in range(len(t)):
		y1 = predictBoolean(y_predict,t[i])
		conf_m = cm.confusionMatrix(y1,y)
		tprs[i],fprs[i] = tp_fp_rates(conf_m)

	a = auc(fprs, tprs)

	plt.clf()
	plt.plot(fprs, tprs)
	plt.axis([0, 1, 0, 1])
	plt.title("ROC curve for %s Regression, AUC: %-2f" %(rtype,a))
	plt.ylabel("True Positive Rate")
	plt.xlabel("False Positive Rate")
	plt.savefig("ROC_%s_Regression.png" %rtype)

def predictBoolean(y,threshold):
	y_predict = np.zeros(len(y))
	for i in range(len(y)):
		y_predict[i] = 0 if y[i] < threshold else 1
	return y_predict

def auc(xs,ys):
	X = np.vstack((xs,ys))
	X_sort = X[:,np.argsort(X[0])]

	area = 0.0
	for i in range(len(X_sort[0])-1):
		x1,y1 = X_sort[:,i]
		x2,y2 = X_sort[:,i+1]
		area += (x2-x1)*(y1+y2)*0.5

	return area

def tp_fp_rates(confusion_matrix):
	tp,fp,tn,fn = confusion_matrix
	tpr = tp/float(tp+fn)
	fpr = fp/float(fp+tn)
	return tpr,fpr