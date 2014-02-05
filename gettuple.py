#!/usr/bin/env python
def gettuple(n):
	a = []
	for item in n:
		for thing in item:
			a.append(thing)
	n=a
	return n	

def getlist(n):
	a = []
	b = 0
	for line in n:
		b = list(line)
		a.append(b)
	n = a
	return n
