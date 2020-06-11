import math
from itertools import product


#This is our "Alphabet" data structure list, returns the list
class Alphabet(list):
	def __init__(self, val=[]):
		super(Alphabet, self).__init__(val)

	def is_empty(self):
		return not len(self)

	def nthString(alp, num):
		if num == 1: return String([])
		layer_size = 1
		tot_size = 1
		layer = 0
		
		while True:
			layer_size = tot_size
			tot_size += len(self) ** (layer + 1)
			if num <= tot_size:
				break
			layer += 1

		index = n - layer_size - 1

		return String(list(product(self, repeat=layer+1))[index])

	def __repr__(self):
		return 'Alphabet {}'.format(', '.join(map(str, self))) 


#This is our own string data type which will has an empty func in there and returns the string in a readable format
class String(list):
	def __init__(self, st):
		if isinstance(st,str):
			st = [Char(c) for c in list(st)]
		super(String, self).__init__(st)

	def empty(self):
		if self == [Char()]:
			return	True

	def __repr__(self):
		return 'String {}'.format(''.join(map(str,self)))


#Data type to hold a character
class Char():
	def __init__(self, ch=None):
		if ch:
			self.ch = ch
			self.empty = False
		else:
			self.ch = 'e'
			self.empty = True

	def isSheEmpty(self):
		return self.empty

	def __hash__(self):
		return hash(self.ch)

	def __eq__(self, other):
		return self.ch == other

	def __repr__(self):
		return self.ch

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
def union(d1, d2):
	return cross(d1,d2, bool.__or__)


#Task 16
def intersect(d1, d2):
	return cross(d1,d2, bool.__and__)


#Task 18
def subset(self, other):
	'''
		C := B intersect A^c
		A is a subset of B iff C does not have any acceptable strings
	'''
	new = self.intersect(~other)
	if new.get_accept():
		return False

	return True	


#Task 20	
def equality(d1, d2):
	'''
		if both sides are a subset of each other then they are equal
	'''
	return subset(d1,d2) and subset(d2,d1)

#Task 13
def compliment(d):
	return DFA(d.alpha, d.Q, d.iniQ, d.trans, d.Q - d.F)




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
			if i.isSheEmpty():continue
			qi = self.trans[qi][i]

		return qi in self.F 
		#Task 12



		'''
		Fixed get accept to return null if nothing is acceptable
		also return empty string if my initialq is accepting
		'''
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
				get_next = self.trans[qi][c]
				if accept(get_next):
					a.insert(0,c)#0 for null
					return True
			return False

		if accept(self.qi):
			return String(s)

		return False
		#Task 11
	def trace(self, s):
		state = []
		qi = self.iniQ
		for c in s:
			state.append(qi)
			qi = self.trans[qi][c]
		return state


#Task 23
class NFA():
	def __init__(self, alpha, Q, iniQ, trans, F):
		self.alpha = alpha
		self.Q = Q
		self.iniQ = iniQ
		self.trans = trans
		self.F = F

	def toNFA(d):
		trans = dict()
		for state in d.trans:
			trans[state] = dict()
			for c in d.trans[state]:
				trans[state][c] = [d.trans[state][c]]

		return NFA(d.alpha, d.Q, d.iniQ, trans, d.F)

	def accepts(self, w):
		def closure(qi):
			stack = []
			v = set([qi])

			if self.trans[qi].get('e'):
				stack.extend(self.trans[qi]['e'])

			while stack:
				state = stack.pop()
				if state not in v:
					v.add(state)
					if self.trans[state].get('e'):
						stack.extend(self.trans[state]['e'])

			return v
			#task 32
		states = closure(self.iniQ)

		for c in w:
			if c.isSheEmpty():continue
			get_next = set()
			for qi in states:
				if self.trans[qi].get(c):
					for nexts in self.trans[qi][c]:
						get_next.update(closure(nexts))
			states = get_next

		return True if (states & self.F) else False

	def oracle(self, s, trace, exp):
		#no match
		if s != String(''.join(str(t[0]) for t in trace)):
			print(f'String<{s}> does no match the given trace')
			return False

		#
		qi = self.iniQ
		#litte search algo here for each t if it's in
		#the transition
		for t in trace:
			if t[1] in self.trans[qi].get(t[0]):
				qi = t[1]
			else:
				print(f'{trace} is not a valid one')
				return False
		#this is for testing oracle at a later task
		return self.accepts(s) == exp

	def cross(self, other, cond):
		states = set()
		accepts = set()
		delta = dict()

		for qi1 in self.Q:
			for qi2 in other.Q:
				states.add((qi1, qi2))
				delta[(qi1, qi2)] = dict()
				for c in self.alpha:
					delta[(qi1, qi2)][c] = list(product(self.trans[qi1][c], other.trans[qi2][c]))

		for (qi1, qi2) in states :
			if cond(qi1 in self.F, qi2 in other.F):
				accepts.add((qi1,qi2))

		return NFA(self.alpha, states, (self.iniQ, other.iniQ), delta, accepts)

	def union(self, other):
		return self.cross(other, bool.__or__)

	def concat(self, other):
		alpha = Alphabet(set(self.alpha).union(other.alpha))
		Q = self.Q.union(set([s for s in other.Q]))
		trans = self.trans.copy()
		iniQ = self.iniQ
		F = set([s for s in other.F])

		newTrans = {}
		for qi, transitions in other.trans.items():
			new_state = qi 
			newTrans[new_state] = dict()
			for c, states in transitions.items():
				newTrans[new_state][c] = [a for a in states]

		trans.update(newTrans)

		for qi in self.F:
			trans[qi]['e'] = [trans[qi].get('e') or []]

		return NFA(alpha, Q, iniQ, trans, F)

	def forking(self, d):
		d = list(d)

		def rec(qi, si):
			if len(d) - 1 < si:
				return 'works' if qi in self.F else 'doesnt'

			r = ''
			c = self.trnas[qi].get(d[si]) or []

			if self.trans[qi].get('e'):
				c.extend(self.trans[qi]['e'])

			if c:
				for t in c:
					r += f'({d[si]}/{t}[{rec(t,si+1)}])'
			return r

			return f'({self.iniQ}[{rec(self.iniQ, 0)}])'


def equalityDriver(d1, tests):
	def equalityFailCase(d1, d2, expected):
		if (d1 == d2) != expected :
			print(f'Test FAILED!')
			return False
		return True

	passed = 0
	for case in tests:
		if equalityFailCase(d1, case[0], case[1]):
			passed += 1
	print(f'{passed}/{len(tests)} equality tests PASSED!')
	return passed



class tt():
	def __init__(self):
		self.start = 0

class accep():
		def __bool__(self): return 'YES'
class branch():
	def __init__(self,c):
		self.c = c
		self.states= states
		

tracetree1 = '(A [(0/A [(1/A [(0/A [(0/A [NO])])])(1/B [(0/C [(0/D [YES])])])])])'
tt1 = tracetree1.tt()
if(tt1.accep == 'YES'):
	print('YES')
	tt1.brach()
else:
	print('NO')
#my trace tree is made manually from my NFA in the correct formatting the tt class will confirm and build
tracetree2 = '(A[(1/A[(0/A[(1/A[(0/A[(0/A[NO])])])(1/B[(0/C[(0/D[YES])])])])])(1/B[(0/C[(1/D[(0/E[(0/E[NO])])])])])])'
tt2 = tracetree2.tt()
if(tt2.accep == 'YES'):
	print(tt2.accept())
	tt2.branch()
	
else:
	print('NO')
tracetree3 = '(A[(0/A[(0/A[(0/A[(0/A[NO])])])])])'
tt3 = tracetree3.tt()
if (tt3.accep == 'YES):
    print 'YES'
    tt3.branch()
else:
    print('NO')
tracetree4 = '(A[(0/A[(0/A[(0/A[(0/A[NO])])])])])'
    #This is testing make sure this works I used my original tt data-type as sort of a testing
tt4 = tracetree4.tt()
if (tt4.accep == 'YES')
    print('YES')
    tt4.brach()
else:
    print('NO')


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
#NFA that includes an Epsilon
nfa0 = NFA(alpha,
			{'q1', 'q2', 'q3', 'q4'}, 'q1',
			{
				'q1': {Char('a'): ['q4'], Char('b'): ['q2'], 'e': ['q3']},
				'q2': {Char('a'): ['q2', 'q3'], Char('b'): ['q3']},
				'q3': {Char('a'): ['q1'], Char('b'): ['q4']},
				'q4': {Char('a'): ['q4'], Char('b'): ['q4']}
			},
			{'q1'})

nfa1 = NFA(binary,
			{'q1', 'q2', 'q3', 'q4', 'q5'}, 'q1',
			{
				'q1': {Char('0'): ['q1'], Char('1'): ['q1', 'q2']},
				'q2': {Char('0'): ['q3'], Char('1'): ['q5'], 'ε': ['q3']},
				'q3': {Char('0'): ['q5'], Char('1'): ['q4']},
				'q4': {Char('0'): ['q4'], Char('1'): ['q4']},
				'q5': {Char('0'): ['q5'], Char('1'): ['q5']}
			},
			{'q4'})

nfa2 = NFA(binary,
			{'q1', 'q2', 'q3', 'q4', 'q5'}, 'q1',
			{
				'q1': {Char('0'): ['q1'], Char('1'): ['q1', 'q2']},
				'q2': {Char('0'): ['q3'], Char('1'): ['q3']},
				'q3': {Char('0'): ['q4'], Char('1'): ['q4']},
				'q4': {Char('0'): ['q5'], Char('1'): ['q5']},
				'q5': {Char('0'): ['q5'], Char('1'): ['q5']}
			},
			{'q4'})

nfafork = NFA(binary,
				{'A', 'B', 'C', 'D'}, 'A',
				{
					'A': {Char('0'): ['A'], Char('1'): ['A', 'B']},
					'B': {Char('0'): ['C'], Char('1'): ['C']},
					'C': {Char('0'): ['D'], Char('1'): ['D']},
					'D': {},
				}, {'D'})

def dfaFailCase(d, s, expected):
	if d.accepts(s) != expected:
		print(f'A test has failed')
		return False
	return True

def dfaTestingDriver(d, tests):
	passed = 0 
	for test in tests:
		if dfaFailCase(d, String(test[0]), test[1]):
			passed += 1
	print(f'{passed}/{len(tests)} tests PASSED')
	return passed

##########################################################################################################################################################################################################


										#Testing for Intersect for task 17


RepetitiveOnes_and_contains_001 = intersect(RepetitiveOnes,contains_001)
even_length_and_only_ones = intersect(even_length,only_ones)

# Test DFA that accepts strings accepted by either RepetitiveOnes and contains_001
test_cases = [([], False), ('0', False), ('01', False), ('11', False), ('111', False), ('110', False), ('0011', True), ('10011', True), ('00011', True), ('11001', True), ('111001', True), ('1001111', True)]
dfaTestingDriver(RepetitiveOnes_and_contains_001, test_cases)


##########################################################################################################################################################################################################

##########################################################################################################################################################################################################


										#Testing for Union for task 15


RepetitiveOnes_or_contains_001 = union(RepetitiveOnes,contains_001)
EvenLength_OnlyOnes = union(even_length,only_ones)

# Test DFA that accepts strings accepted by either RepetitiveOnes or contains_001
test_cases = [([], False), ('0', False), ('01', False), ('11', True), ('111', True), ('110', True), ('010', False), ('0011', True), ('0001', True), ('00011', True), ('0000', False), ('01000', False)]
dfaTestingDriver(RepetitiveOnes_or_contains_001, test_cases)

##########################################################################################################################################################################################################


###############################################
#Task21######################
'''
Union, if we call union on two DFA we should have all elements from one
dfa and another dfa in one. We test to make sure all elements consist in
both DFA's

'''

# Test if RepetitiveOnes_or_contains_001 is equal to each test DFA
#Just realized that this works for task 22
test_cases = [(RepetitiveOnes_or_contains_001, True), (only_ones, False), (compliment(RepetitiveOnes_or_contains_001), False), (compliment(compliment(RepetitiveOnes_or_contains_001)), False)]
equalityDriver(RepetitiveOnes_or_contains_001, test_cases)

test_cases = [(RepetitiveOnes_and_contains_001, True), (only_ones, False), (compliment(RepetitiveOnes_and_contains_001), False), (RepetitiveOnes_and_contains_001, True)]
equalityDriver(RepetitiveOnes_and_contains_001, test_cases)

new_nfa = NFA.toNFA(even_length)

print(nfa1.accepts(String('')))

t = nfa1.union(nfa2)

print(t.accepts(String('111'))) #True

new = nfa2.concat(nfa1)

print(new.accepts(String('0baa')))	#false

print(nfafork.forking(String('0101')))


