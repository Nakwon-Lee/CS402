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

def onlyOneCond(r):
	rootK = None
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
				t_rootC.left = root
				t_rootC.right = rootC
				rootC = t_rootC

		if rootK is None:
			rootK = rootC
		else:
			t_rootK = BinaryNode(1)
			t_rootK.left = rootC
			t_rootK.right = rootK
			rootK = t_rootK

	return rootK

def orderCond(r):
	
	rootO = None
	for k is range(len(rows[r])-1):
		rootC = None
		for c is range(M-1):
			root = BinaryNode(4)
			root.left = TerminalNode(7)
			root.left.var = varmapr[r][c][k]
			root.right = BinaryNode(1)
			root.right.left = UnaryNode(3)
			root.right.left.child = TerminalNode(7)
			root.right.left.child.var = varmapr[r][c+1][k+1]
			root.right.right = None
			
			for i is range(c+2,M):
				if root.right.right is None:
					root.right.right = TerminalNode(7)
					root.right.right.var = varmapr[r][i][k+1]
				else:
					t_rrright = BinaryNode(2)
					t_rrright.right = root.right.right
					t_rrright.left = TerminalNode(7)
					t_rrright.left.var = varmapr[r][i][k+1]
					root.right.right = t_rrright

			if rootC is None:
				rootC = root
			else:
				t_rootC = BinaryNode(2)
				t_rootC.left = rootC
				t_rootC.right = root
				rootC = t_rootC
				


def nonogram():
	
	#number of blanks for row is M, the length of colunm 
	for i in range(len(rows)):
		rootK = onlyOneCond(i)
		rootO = orderCond(i)

if __name__ == '__main__':

	read_file(sys.argv[1])

	nonogram()


