"""
node.py from HW1
"""
class Node:
	def __init__(self):
		self.prediction = None
		self.left = None
		self.right = None
		self.test = None

	def printNode(self):
		print "=========================="
		print self.prediction
		if self.left != None:
			self.left.printNode()
		if self.right != None:
			self.right.printNode()