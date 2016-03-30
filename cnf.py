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

	def setSym(self, sym):
		self.symbol = sym

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

def CopyTree(root): # copy all subtree

	clonedRoot = None
	
	if isinstance(root, BinaryNode):
		clonedRoot = BinaryNode(root.getSym())
		clonedRoot.left = CopyTree(root.left)
		clonedRoot.right = CopyTree(root.right)

	elif isinstance(root, UnaryNode):
		clonedRoot = UnaryNode(root.getSym())
		clonedRoot.child = CopyTree(root.child)

	elif isinstance(root, TerminalNode):
		clonedRoot = TerminalNode(root.getSym())
		clonedRoot.var = root.var

	return clonedRoot

def ImpFree(root):
	
	key = root.getSym()

	if key is 4:
		tempNode = UnaryNode(3)
		tempNode.child = ImpFree(root.left)
		root.left = tempNode
		root.right = ImpFree(root.right)
		root.setSym(2)

	elif key is 5:
		tempNode = UnaryNode(3)
		tempNode.child = ImpFree(root.right)
		root.right = tempNode
		root.left = ImpFree(root.left)
		root.setSym(2)

	elif key is 6:
		tempNode = BinaryNode(1)
		clonedRoot = CopyTree(root)
		root.setSym(4)
		clonedRoot.setSym(5)
		tempNode.left = ImpFree(root)
		tempNode.right = ImpFree(clonedRoot)
		root = tempNode

	elif key is (1 or 2):
		root.left = ImpFree(root.left)
		root.right = ImpFree(root.right)

	elif key is 3:
		root.child = ImpFree(root.child)

	elif key is 7:
		pass

	else:
		print "Invaild symbol of Node! Bye Bye!"
		sys.exit()

	return root

def NNF(root):
	
	leftC = None
	rightC = None
	child = None
	key = None

	if isinstance(root, BinaryNode):
		leftC, key = NNF(root.left)
		rightC, key = NNF(root.right)
		key = 2
		
	elif isinstance(root, UnaryNode): # negation is only an UnaryNode
		child, key = NNF(root.child)
		if key is 2: # child is binary
			leftC = UnaryNode(3)
			rightC = UnaryNode(3)

	elif isinstance(root, TerminalNode):
		pass

	return root, key

if __name__ == '__main__':

	root, RF = parsePolishNotation("= & - p q & p > r q")

	if RF is not "":
		print "Invaild formula! Bye Bye!"
		sys.exit()

	printTree(root)
	print ""

	root = ImpFree(root)	

	printTree(root)
