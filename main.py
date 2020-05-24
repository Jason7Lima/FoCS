import math
from itertools import product

class Alphabet(list):
	def __init__(self, val=[]):
		super(Alphabet, self).__init__(val)

	def __repr__(self):
		return 'Alphabet {}'.format(', '.join(map(str, self))) 


class String(list):
	def __init__(self, st, al):
		super(String, self).__init__(st)
		self.al = al

	def empty(self):
		return not len(self.st)

	def __repr__(self):
		return 'String {}'.format(''.join(map(str,self)))

class Char():
	def __init__(self, ch=''):
		self.ch = ch;

	def __repr__(self):
		return self.ch


def nthString(alp, num):
	if not num: return String([Char()], alp)
	layer = int(math.log(num + 1, len(alp))) 
	index =  num + 1 - len(alp) ** layer 
	return String(list(product(alp, repeat=layer))[index], alp)

