import sys
import math
import random
import os

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

	global N
	N = int(lines[0])

	global M
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

	global varnum
	varnum = 1

	for r in range(N):
		temprow = []
		for c in range(M):
			temp = []
			for i in range(len(rows[r])):
				temp.append(varnum)
				varnum = varnum + 1
			temprow.append(temp)
		varmapr.append(temprow)

	for r in range(N):
		temprow = []
		for c in range(M):
			temp = []
			for i in range(len(cols[c])):
				temp.append(varnum)
				varnum = varnum + 1
			temprow.append(temp)
		varmapc.append(temprow)

def write_minisat_input(root):

	lines = []

	st = []

	lines.append(st)

	nAND = inorder(root,lines)

	if (nAND+1) != len(lines):
		print "nAND+1 is not same as length of lines! error! ByeBye!"
		sys.exit()

	data = "p cnf %d %d\n" % (varnum-1,nAND+1) # nAND+1 should be same as length of lines

	miniin = open("mini.in",'w')

	miniin.write(data)
	for line in lines:
		for ca in line:
			if ca is not '-':
				miniin.write(ca)
				miniin.write(' ')
				#print ca, ' ',
			else:
				miniin.write(ca)
				#print ca,
		miniin.write("0\n")
		#print "0\n"

	miniin.close()

def inorder(root,lines):
	
	nAND = 0

	if isinstance(root,BinaryNode):
		nAND = inorder(root.left,lines) + nAND
		if root.getSym() is 1: # and
			st = []
			lines.append(st)
			nAND = nAND + 1
		nAND = inorder(root.right,lines) + nAND
	
	elif isinstance(root,UnaryNode):
		lines[len(lines)-1].append('-')
		nAND = inorder(root.child,lines) + nAND

	elif isinstance(root,TerminalNode):
		lines[len(lines)-1].append(str(root.var))
	
	return nAND

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

	elif key is 1:
		root.left = ImpFree(root.left)
		root.right = ImpFree(root.right)

	elif key is 2:
		root.left = ImpFree(root.left)
		root.right = ImpFree(root.right)

	elif key is 3:
		root.child = ImpFree(root.child)

	elif key is 7:
		pass

	else:
		print "Invalid symbol of Node! Bye Bye!"+key
		sys.exit()

	return root

def NNF(root):
	leftC = None
	rightC = None
	key = None

	if isinstance(root, BinaryNode):
		root.left = NNF(root.left)
		root.right = NNF(root.right)
		
	elif isinstance(root, UnaryNode): # negation is only an UnaryNode
		key = root.child.getSym()
		if key is (1 or 2): # child is binary
			leftC = UnaryNode(3)
			rightC = UnaryNode(3)
			leftC.child = root.child.left
			rightC.child = root.child.right
			root.child.left = leftC
			root.child.right = rightC
			op = root.child.getSym()
			if op is 1: # and
				root.child.setSym(2)
			elif op is 2: # or
				root.child.setSym(1)
			root = root.child
			root.left = NNF(root.left)
			root.right = NNF(root.right)
		elif key is 3: # child is unary
			root = NNF(root.child.child)
		else:
			root.child = NNF(root.child)

	elif isinstance(root, TerminalNode):
		pass

	return root

def CNF(root):
	key = root.getSym()

	if key is 2: # root is "or"
		CNF(root.left)
		CNF(root.right)
		DISTR(root)
	elif key is 1: # root is "and"
		CNF(root.left)
		CNF(root.right)

	return root

def DISTR(root):

	if not isinstance(root, BinaryNode):
		return root

	leftkey = root.left.getSym()
	rightkey = root.right.getSym()

	if leftkey is 1: # left child is "and"
		f1 = root.left.left
		f2 = root.left.right
		f3 = root.right

		root.left.right = f3
		root.right = BinaryNode(2)

		root.right.left = f2
		root.right.right = CopyTree(f3)

		root.setSym(1)
		root.left.setSym(2)

		DISTR(root.left)
		DISTR(root.right)

	elif (leftkey is not 1) and rightkey is 1: # right child is "and"
		f1 = root.left
		f2 = root.right.left
		f3 = root.right.right

		root.left = BinaryNode(2)
		root.left.left = f1
		root.left.right = f2

		root.right.left = CopyTree(f1)

		root.setSym(1)
		root.right.setSym(2)

		DISTR(root.left)
		DISTR(root.right)	

	return root

def printTree(root):

	key = root.getSym()

	if isinstance(root, BinaryNode):
		print root.getSym(), " ",
		printTree(root.left)
		printTree(root.right)

	elif isinstance(root, UnaryNode):
		print root.getSym(), " ",
		printTree(root.child)

	elif isinstance(root, TerminalNode):
		print '(', root.var, ')', " ",

def onlyOneCond(r):
	rootK = None
	for k in range(len(rows[r])):
		rootC = None
		for c in range(M-rows[r][k]+1):
			root = BinaryNode(1)
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
	for k in range(len(rows[r])-1):
		rootC = None
		for c in range(M-1):
			root = BinaryNode(4)
			root.left = TerminalNode(7)
			root.left.var = varmapr[r][c][k]
			root.right = BinaryNode(1)
			root.right.left = UnaryNode(3)
			root.right.left.child = TerminalNode(7)
			root.right.left.child.var = varmapr[r][c+1][k+1]
			root.right.right = None

			for i in range(0,c):
				t_rrleft = BinaryNode(1)
				t_rrleft.left = root.right.left
				t_rrleft.right = UnaryNode(3)
				t_rrleft.right.child = TerminalNode(7)
				t_rrleft.right.child.var = varmapr[r][i][k+1]
				root.right.left = t_rrleft
			
			for i in range(c+2,M):
				if root.right.right is None:
					root.right.right = TerminalNode(7)
					root.right.right.var = varmapr[r][i][k+1]
				else:
					t_rrright = BinaryNode(2)
					t_rrright.right = root.right.right
					t_rrright.left = TerminalNode(7)
					t_rrright.left.var = varmapr[r][i][k+1]
					root.right.right = t_rrright

			if root.right.right is None:
				root.right = root.right.left

			if rootC is None:
				rootC = root
			else:
				t_rootC = BinaryNode(1)
				t_rootC.left = rootC
				t_rootC.right = root
				rootC = t_rootC

		if rootO is None:
			rootO = rootC
		else:
			t_rootO = BinaryNode(1)
			t_rootO.left = rootO
			t_rootO.right = rootC
			rootO = t_rootO

	return rootO				

def onlyOneCond2(c):
	rootK = None
	for k in range(len(cols[c])):
		rootC = None
		for r in range(N-cols[c][k]+1):
			root = BinaryNode(1)
			root.left = TerminalNode(7)
			root.left.var = varmapc[r][c][k]
			root.right = None
			for i in range(0,r): # and negations
				if root.right is None:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapc[i][c][k] 
					root.right = tempNode
				else:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapc[i][c][k]
					temprightNode = BinaryNode(1)
					temprightNode.left = tempNode
					temprightNode.right = root.right
					root.right = temprightNode

			for i in range(r+1,r+cols[c][k]): # and filled squares
				if root.right is None:
					root.right = TerminalNode(7)
					root.right.var = varmapc[i][c][k]
				else:
					temprightNode = BinaryNode(1)
					temprightNode.left = TerminalNode(7)
					temprightNode.left.var = varmapc[i][c][k]
					temprightNode.right = root.right
					root.right = temprightNode

			for i in range(r+cols[c][k],N): # and negations
				if root.right is None:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapc[i][c][k] 
					root.right = tempNode
				else:
					tempNode = UnaryNode(3)
					tempNode.child = TerminalNode(7)
					tempNode.child.var = varmapc[i][c][k]
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

def orderCond2(c):
	
	rootO = None
	for k in range(len(cols[c])-1):
		rootC = None
		for r in range(N-1):
			root = BinaryNode(4)
			root.left = TerminalNode(7)
			root.left.var = varmapc[r][c][k]
			root.right = BinaryNode(1)
			root.right.left = UnaryNode(3)
			root.right.left.child = TerminalNode(7)
			root.right.left.child.var = varmapc[r+1][c][k+1]
			root.right.right = None
			
			for i in range(0,r):
				t_rrleft = BinaryNode(1)
				t_rrleft.left = root.right.left
				t_rrleft.right = UnaryNode(3)
				t_rrleft.right.child = TerminalNode(7)
				t_rrleft.right.child.var = varmapc[i][c][k+1]
				root.right.left = t_rrleft

			for i in range(r+2,N):
				if root.right.right is None:
					root.right.right = TerminalNode(7)
					root.right.right.var = varmapc[i][c][k+1]
				else:
					t_rrright = BinaryNode(2)
					t_rrright.right = root.right.right
					t_rrright.left = TerminalNode(7)
					t_rrright.left.var = varmapc[i][c][k+1]
					root.right.right = t_rrright

			if root.right.right is None:
				root.right = root.right.left

			if rootC is None:
				rootC = root
			else:
				t_rootC = BinaryNode(1)
				t_rootC.left = rootC
				t_rootC.right = root
				rootC = t_rootC

		if rootO is None:
			rootO = rootC
		else:
			t_rootO = BinaryNode(1)
			t_rootO.left = rootO
			t_rootO.right = rootC
			rootO = t_rootO

	return rootO

def rowcolMatch():

	rootM = None
	for r in range(N):
		for c in range(M):
			root = BinaryNode(6)
			
			rootR = None
			for k in range(len(rows[r])):
				if rootR is None:
					rootR = TerminalNode(7)
					rootR.var = varmapr[r][c][k]
				else:
					t_rootR = BinaryNode(2)
					t_rootR.left = rootR
					t_rootR.right = TerminalNode(7)
					t_rootR.right.var = varmapr[r][c][k]
					rootR = t_rootR

			rootC = None
			for k in range(len(cols[c])):
				if rootC is None:
					rootC = TerminalNode(7)
					rootC.var = varmapc[r][c][k]
				else:
					t_rootC = BinaryNode(2)
					t_rootC.left = rootC
					t_rootC.right = TerminalNode(7)
					t_rootC.right.var = varmapc[r][c][k]
					rootC = t_rootC

			if (rootR is not None) and (rootC is not None):
				root.left = rootR
				root.right = rootC

			elif (rootR is None) and (rootC is not None):
				root = UnaryNode(3)
				root.child = rootC

			elif (rootR is not None) and (rootC is None):
				root = UnaryNode(3)
				root.child = rootR
			else:
				root = None

			if root is not None:
				if rootM is None:
					rootM = root
				else:
					t_rootM = BinaryNode(1)
					t_rootM.left = rootM
					t_rootM.right = root
					rootM = t_rootM
	
	return rootM

def nonogram():
	
	# number of blanks for row is M, the length of colunm
	rootR = None

	for i in range(len(rows)):

		rootK = onlyOneCond(i)
		rootO = orderCond(i)

		t_rootR = None

		if (rootO is not None) and (rootK is not None):
			t_rootR = BinaryNode(1)
			t_rootR.left = rootK
			t_rootR.right = rootO
		elif (rootO is not None) and (rootK is None): 
			t_rootR = rootO
		elif (rootO is None) and (rootK is not None): 
			t_rootR = rootK

		if t_rootR is not None:
			if rootR is None:
				rootR = t_rootR
			else:
				tt_rootR = BinaryNode(1)
				tt_rootR.left = rootR
				tt_rootR.right = t_rootR
				rootR = tt_rootR

	# assume that rootR is not None because there is at least one row that have conditions		

	# number of blanks for col is N, the length of row
	rootC = None

	for i in range(len(cols)):
		rootK = onlyOneCond2(i)
		rootO = orderCond2(i)

		t_rootC = None

		if (rootO is not None) and (rootK is not None):
			t_rootC = BinaryNode(1)
			t_rootC.left = rootK
			t_rootC.right = rootO
		elif (rootO is not None) and (rootK is None): 
			t_rootC = rootO
		elif (rootO is None) and (rootK is not None): 
			t_rootC = rootK

		if t_rootC is not None:
			if rootC is None:
				rootC = t_rootC
			else:
				tt_rootC = BinaryNode(1)
				tt_rootC.left = rootC
				tt_rootC.right = t_rootC
				rootC = tt_rootC

	# assume that rootC is not None because there is at least one col that have conditions

	# row-based nonogram and column-based nonogram must be equivalant	
	rootM = rowcolMatch()

	t_root = BinaryNode(1)
	t_root.left = rootR
	t_root.right = rootC

	root = BinaryNode(1)
	root.left = t_root
	root.right = rootM
	
	return root

def read_show_result():
	lines = open("mini.out").readlines()

	if lines[0][0] is 'S':
		pass
	else:
		print "Not valid nonogram Bye!"
		sys.exit()

	variables = lines[1].split()

	varsint = []

	for var in variables:
		if int(var) > 0:
			varsint.append(int(var))

	# print varsint

	for r in range(N):
		for c in range(M):
			filled = 0
			for k in range(len(rows[r])):
				for var in varsint:
					if var == varmapr[r][c][k]:
						filled = 1
						break
			if filled == 1:
				print "#",
			else:
				print ".",
		print ""

if __name__ == '__main__':

	read_file(sys.argv[1])

	root = nonogram()

	root = CNF(NNF(ImpFree(root)))

	write_minisat_input(root)

	os.system("minisat mini.in mini.out")

	read_show_result()	

