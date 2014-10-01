import numpy as np
import gradientDescent as gd
import perceptron as pcpt

def problem2():
	print "============================================="
	print "loading perceptron data..."
	perceptron_data = np.loadtxt("../dataset/perceptronData.txt")

	X,y = gd.extractData(perceptron_data)

	w = pcpt.perceptron(X,y)

	print "Classifier weights: ", w
	print "Normalized with threshold: ", w[1:]/-w[0]
	print "============================================="

if __name__ == "__main__":
	problem2()