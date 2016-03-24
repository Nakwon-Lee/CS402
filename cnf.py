import sys
import math
import random

class Node:
	id = 0
	def __init__(self, symbol):
		self.id = Node.id
		self.symbol = symbol #zero mean not valid symbol
		Node.id = Node.id + 1
	def getSym(self):
		return self.symbol

class BinaryNode(Node):
	def __init__(self, symnum):
		self.left = None
		self.right = None
		Node.__init__(self, symnum)

class UnaryNode(Node):
	def __init__(self, symnum):
		self.child = None
		Node.__init__(self, symnum)

class TerminalNode(Node):
	def __init__(self, symnum):
		self.var = None
		Node.__init__(self, symnum)

def printTree(root):

	if isinstance(root, BinaryNode):
		print root.getSym(), " ",
		printTree(root.left)
		printTree(root.right)

	elif isinstance(root, UnaryNode):
		print root.getSym(), " ",
		printTree(root.child)

	elif isinstance(root, TerminalNode):
		print root.var, " ",
	
def parsePolishNotation(formula):

	token = None
	remainingFormula = ""

	if formula.find(' ') is -1:
		token = formula
	else:
		token, remainingFormula = formula.split(' ', 1)

	subTree = None

	if token is "&":  # symbol number 1
		subTree = BinaryNode(1)
		subTree.left, remainingFormula = parsePolishNotation(remainingFormula)
		subTree.right, remainingFormula = parsePolishNotation(remainingFormula)

	elif token is "|": # 2
		subTree = BinaryNode(2)
		subTree.left, remainingFormula = parsePolishNotation(remainingFormula)
		subTree.right, remainingFormula = parsePolishNotation(remainingFormula)

	elif token is "-": # 3
		subTree = UnaryNode(3)
		subTree.child, remainingFormula = parsePolishNotation(remainingFormula)

	elif token is ">": # 4
		subTree = BinaryNode(4)
		subTree.left, remainingFormula = parsePolishNotation(remainingFormula)
		subTree.right, remainingFormula = parsePolishNotation(remainingFormula)

	elif token is "<": # 5
		subTree = BinaryNode(5)
		subTree.left, remainingFormula = parsePolishNotation(remainingFormula)
		subTree.right, remainingFormula = parsePolishNotation(remainingFormula)

	elif token is "=": # 6
		subTree = BinaryNode(6)
		subTree.left, remainingFormula = parsePolishNotation(remainingFormula)
		subTree.right, remainingFormula = parsePolishNotation(remainingFormula)

	else: # 7; must be a variable! if not, it is not valid. need to check the validity of formula
		subTree = TerminalNode(7)
		subTree.var = token

	return subTree, remainingFormula

if __name__ == '__main__':

	root, RF = parsePolishNotation("> & - p q & p > r q")

	if RF is not "":
		print "Invaild formula! Bye Bye!"
		sys.exit()	

	printTree(root)
