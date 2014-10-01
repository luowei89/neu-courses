import numpy as np

threshold = 0.5

# sigmoid function
def sigmoid(x):
    return 1/(1+np.exp(-x))
# derivative of the sigmoid function
def dsigmoid(y):
    return sigmoid(y)*(1-sigmoid(y))

class NeuralNetwork:

	def __init__(self, ni, nh, no):
		# number of input, hidden, and output nodes
		self.ni = ni
		self.nh = nh
		self.no = no

		# output for nodes
		self.oi = np.ones(self.ni + 1)
		self.oh = np.ones(self.nh + 1)
		self.oo = np.ones(self.no)

		# create random weights [0, 1]
		self.wi = np.random.rand(self.ni + 1, self.nh)
		self.wo = np.random.rand(self.nh + 1, self.no)

	def backPropagate(self,D,l,iterations=1000):
		for it in range(iterations):
			for d in D:
				inputs = d[0]
				targets = d[1]
				# propagate the inputs forward: 
				self.oi[1:] = inputs
				self.oh[1:] = np.array([sigmoid(x) for x in np.dot(self.oi,self.wi)])
				self.oo = np.array([sigmoid(x) for x in np.dot(self.oh,self.wo)])
				# caculate output error
				output_err = np.array([dsigmoid(x) for x in self.oo]) * (targets-self.oo)
				# caculate hidden error
				hidden_err = np.array([dsigmoid(x) for x in self.oh]) * np.dot(output_err.T,self.wo.T)

				# update output weights
				delta_wo = l * np.dot(np.matrix(self.oh).T,np.matrix(output_err))
				self.wo += delta_wo
				# update input weights
				delta_wi = l * np.dot(np.matrix(self.oi).T,np.matrix(hidden_err))
				self.wi += delta_wi[:,1:]

	def test(self, D):
		for d in D:
			print list(d[0]), "->", list(self.output(d[0]))

	def output(self,inputs):
		self.oi[1:] = inputs
		self.oh[1:] = np.array([sigmoid(x) for x in np.dot(self.oi,self.wi)])
		self.oo = np.array([sigmoid(x) for x in np.dot(self.oh,self.wo)])
		outputs = np.array([1 if x > threshold else 0 for x in self.oo])
		return outputs