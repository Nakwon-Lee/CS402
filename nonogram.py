import sys
import math
import random

N = 0
M = 0
rows = []
cols = []
varmapr = []
varmapc = []

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
	for k in range(len(rows[r])):
		for c in range(M):
			varmapr[r][c][k]->
			

def nonogram():
	
	#number of blanks for row is M, the length of colunm 
	for i in range(len(rows)):
		formula(i)

if __name__ == '__main__':

	read_file(sys.argv[1])

	nonogram()


