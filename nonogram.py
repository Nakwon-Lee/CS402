import sys
import math
import random

N = 0
M = 0
rows = []
cols = []
varmapr = []
varmapc = []

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

def read_file(filename):
	lines = open(filename).readlines()

	N = int(lines[0])

	M = int(lines[1])

	for i in range(2,2+N):
		temp = []
		for j in range(len(lines[i])):
			if lines[i][j].isdigit():
				temp.append(int(lines[i][j]))
		rows.append(temp)

	for i in range(2+N,2+N+M):
		temp = []
		for j in range(len(lines[i])):
			if lines[i][j].isdigit():
				temp.append(int(lines[i][j]))
		cols.append(temp)

	varnum = 1

	for r in range(N):
		temprow = []
		for c in range(M):
			temp = []
			for i in range(len(rows[r]))
				temp.append(varnum)
				varnum = varnum + 1
			temprow.append(temp)
		varmapr.append()

	for r in range(N):
		temprow = []
		for c in range(M):
			temp = []
			for i in range(len(cols[c]))
				temp.append(varnum)
				varnum = varnum + 1
			temprow.append(temp)
		varmapc.append()


def formula(r):
	root1 = BinaryNode()
	for k in range(len(rows[r])):
		rootC = None
		for c in range(M-rows[r][k]):
			root = BinaryNode(4)
			root.left = TerminalNode(7)
			root.left.var = varmapr[r][c][k]
			root.right = None
			for i in range(0,c): # and negations
				if root.right is None:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapr[r][i][k] 
					root.right = tempNode
				else:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapr[r][i][k]
					temprightNode = BinaryNode(1)
					temprightNode.left = tempNode
					temprightNode.right = root.right
					root.right = temprightNode

			for i in range(c+1,c+rows[r][k]): # and filled squares
				if root.right is None:
					root.right = TerminalNode(7)
					root.right.var = varmapr[r][i][k]
				else:
					temprightNode = BinaryNode(1)
					temprightNode.left = TerminalNode(7)
					temprightNode.left.var = varmapr[r][i][k]
					temprightNode.right = root.right
					root.right = temprightNode

			for i in range(c+rows[r][k],M): # and negations
				if root.right is None:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapr[r][i][k] 
					root.right = tempNode
				else:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapr[r][i][k]
					temprightNode = BinaryNode(1)
					temprightNode.left = tempNode
					temprightNode.right = root.right
					root.right = temprightNode

			if rootC is None:
				rootC = root
			else:
				t_rootC = BinaryNode(2)

def nonogram():
	
	#number of blanks for row is M, the length of colunm 
	for i in range(len(rows)):
		formula(i)

if __name__ == '__main__':

	read_file(sys.argv[1])

	nonogram()


