import math
from itertools import product


#This is our "Alphabet" data structure list, returns the list
class Alphabet(list):
	def __init__(self, val=[]):
		super(Alphabet, self).__init__(val)

	def is_empty(self):
		return not len(self)

	def __repr__(self):
		return 'Alphabet {}'.format(', '.join(map(str, self))) 


#This is our own string data type which will has an empty func in there and returns the string in a readable format
class String(list):
	def __init__(self, st, al):
		if isinstance(st,str):
			st = [Char(c) for c in list(st)]
		super(String, self).__init__(st)
		self.al = al

	def empty(self):
		return not len(self)

	def __repr__(self):
		return 'String {}'.format(''.join(map(str,self)))


#Data type to hold a character
class Char():
	def __init__(self, ch=''):
		self.ch = ch;

	def __hash__(self):
		return hash(self.ch)

	def __eq__(self, other):
		return self.ch == other

	def __repr__(self):
		return self.ch


def nthString(alp, num):
	if not num: return String([Char()], alp)
	layer = int(math.log(num + 1, len(alp))) 
	index =  num + 1 - len(alp) ** layer 
	
	return String(list(product(alp, repeat=layer))[index], alp)

class DFA():
	def __init__(self, alpha, Q, iniQ, trans, F):
		self.Q = Q
		self.alpha = alpha
		self.iniQ = iniQ
		self.trans = trans
		self.F = F

	def accepts(self, w):

		if self.Q:
			if not w:
				return False
			elif w == [Char()]:
				return True
		else:
			if w.is_empty():
				return True
			return False

		qi = self.iniQ
		for i in w:
			qi = self.trans[qi][i]

		return qi in self.F 
		#Task 12
	def get_accept(self):
		v = set()
		a = []

		def accept(qi):
			if qi in self.F:
				return True
			elif qi in v:
				return False
			v.add(qi)

			for c in self.alpha:
				if accept(self.trans[qi][c]):
					a.append(c)
					return True
			return False

		accept(self.iniQ)

		return String(a[::-1], self.alpha)
		#Task 11
	def trace(self, s):
		state = []
		if self.accepts(s):
			qi = self.iniQ
			for c in s:
				state.append(qi)
				qi = self.trans[qi][c]
			return state
		return False

	def cross(self, other, cond):
		states = set()
		accepts = set()
		delta = dict()

		for qi1 in self.Q:
			for qi2 in other.Q:
				states.add((qi1, qi2))
				delta[(qi1, qi2)] = dict()
				for c in self.alpha:
					delta[(qi1, qi2)][c] = (self.trans[qi1][c], other.trans[qi2][c])

		for (qi1, qi2) in states:
			if cond(qi1 in self.F, qi2 in other.F):
				accepts.add((qi1, qi2))

		return DFA(self.alpha, states, (self.iniQ, other.iniQ), delta, accepts)

	#Task 14
	def union(self, other):
		return self.cross(other, bool.__or__)


	#Task 16
	def intersect(self, other):
		return self.cross(other, bool.__and__)

	def subset(self, other):
		'''
			C := B intersect A^c
			A is a subset of B iff C does not have any acceptable strings
		'''
		return not other.intersect(~self).get_accepted()

	def __contains__(self, other):
		return self.subset(other)

	def __eq__(self, other):
		'''
			if both sides are a subset of each other then they are equal
		'''
		return self in other and other in self

	def __invert__(self):
		'''
			returns the complement of the DFA with a new name
		'''
		return DFA(self.alpha, self.Q, self.iniQ, self.trans, self.Q - self.F)


	#Task 13
	def compliment(d):
		return DFA(d.alpha, d.Q, d.iniQ, d.trans, d.Q - d.F)










binary = Alphabet([Char('0'), Char('1')])
alpha = Alphabet([Char(letters) for letters in 'abcdefghijklmnopqrstuvwxyz'])


contains_001 = DFA(binary,
					   {'iniQ', 'q1', 'q2', 'q3'}, 'iniQ',
					   {
						   	'iniQ': {Char('0'): 'q1', Char('1'): 'iniQ'},
						    'q1': {Char('0'): 'q2', Char('1'): 'iniQ'},
						    'q2': {Char('1'): 'q3', Char('0'): 'q2'},
						    'q3': {Char('0'): 'q3', Char('1'): 'q3'}
					   },
					   {'q3'})

only_ones = DFA(binary,
					{'q0', 'q1', 'q2'}, 'q0',
					{
						'q0': {Char('0'): 'q2', Char('1'): 'q1'},
						'q1': {Char('0'): 'q2', Char('1'): 'q1'},
						'q2': {Char('0'): 'q2', Char('1'): 'q2'}
					},
					{'q1'})

RepetitiveOnes = DFA(binary,
						   {'q0', 'q1', 'q2'}, 'q0',
						   {
						   	'q0': {Char('1'): 'q1', Char('0'): 'q0'},
						    'q1': {Char('1'): 'q2', Char('0'): 'q0'},
						    'q2': {Char('1'): 'q2', Char('0'): 'q2'},
						   },
						   {'q2'})

even_length = DFA(binary,
					  {'q0', 'q1'}, 'q0',
					  {
						'q0': {Char('0'): 'q1', Char('1'): 'q1'},
						'q1': {Char('0'): 'q0', Char('1'): 'q0'}
					  },
					  {'q0'})

def dfaFailCase(d, s, expected):
	if d.accepts(s) != expected:
		print(f'A test has failed')
		return False
	return True

def dfaTestingDriver(d, tests):
	passed = 0 
	for test in tests:
		if dfaFailCase(d, String(test[0], d.alpha), test[1]):
			passed += 1
	print(f'{passed}/{len(tests)} tests PASSED')
	return passed

##########################################################################################################################################################################################################


										#Testing for Intersect for task 17


RepetitiveOnes_and_contains_001 = RepetitiveOnes.intersect(contains_001)
even_length_and_only_ones = even_length.intersect(only_ones)

# Test DFA that accepts strings accepted by either RepetitiveOnes and contains_001
test_cases = [([], False), ('0', False), ('01', False), ('11', False), ('111', False), ('110', False), ('0011', True), ('10011', True), ('00011', True), ('11001', True), ('111001', True), ('1001111', True)]
dfaTestingDriver(RepetitiveOnes_and_contains_001, test_cases)


##########################################################################################################################################################################################################

##########################################################################################################################################################################################################


										#Testing for Union for task 15


RepetitiveOnes_or_contains_001 = RepetitiveOnes.union(contains_001)
EvenLength_OnlyOnes = even_length.union(only_ones)

# Test DFA that accepts strings accepted by either RepetitiveOnes or contains_001
test_cases = [([], False), ('0', False), ('01', False), ('11', True), ('111', True), ('110', True), ('010', False), ('0011', True), ('0001', True), ('00011', True), ('0000', False), ('01000', False)]
dfaTestingDriver(RepetitiveOnes_or_contains_001, test_cases)

##########################################################################################################################################################################################################
