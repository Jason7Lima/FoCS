import math
from itertools import product


#This is our "Alphabet" data structure list, returns the list
class Alphabet(list):
	def __init__(self, val=[]):
		super(Alphabet, self).__init__(val)

	def __repr__(self):
		return 'Alphabet {}'.format(', '.join(map(str, self))) 


#This is our own string data type which will has an empty func in there and returns the string in a readable format
class String(list):
	def __init__(self, st, al):
		super(String, self).__init__(st)
		self.al = al

	def empty(self):
		return not len(self.st)

	def __repr__(self):
		return 'String {}'.format(''.join(map(str,self)))


#Data type to hold a character
class Char():
	def __init__(self, ch=''):
		self.ch = ch;

	def __eq__(self, other):
		return self.ch == other


def nthString(alp, num):
	layer = int(math.log(num + 1, len(alp))) 
	index =  num + 1 - len(alp) ** layer 
	
	return String(list(product(alp, repeat=layer))[index], alp)

class DFA():
	def __init__(self, Q, alpha, iniQ, trans, F):
		self.Q = Q
		self.alpha = alpha
		self.iniQ = iniQ
		self.trans = trans
		self.F = F

	def accepts(self, w):
		qi = self.iniQ
		i = 0
		for i in range(len(w)):
			qi = self.trans(qi, w[i])

		return self.F(qi) 


binary = Alphabet([Char('0'), Char('1')])
alpha = Alphabet([Char(letters) for letters in 'abcdefghijklmnopqrstuvwxyz'])

dfaNoString = DFA(binary,
					 (lambda qi: False), 0,
					 (lambda qi, c: False),
					 (lambda qi: False)) 

dfaEmpty = DFA(binary,
					   (lambda qi: qi == 0 or qi == 1), 0,
					   (lambda qi, c: 1 if c else 0),
					   (lambda qi: qi == 0)) 

dfaSingleChar = DFA(binary,
						(lambda qi: qi == 0 or qi == 1 or qi == 2), 0,
						(lambda qi, c: 1 if qi == 0 and c else 2),
						(lambda qi: qi == 1)) 

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

#contains 0
Zeros = DFA(binary,
	(lambda qi: qi == 0 or qi == 1 or qi == 2), 0,
	(lambda qi, c: 1 if qi == 0 and c == '0' else 2 if qi == 1 and c == '0' else 2 if qi == 2 else 0),
	(lambda qi: qi == 2))
#contains one
Ones = DFA(binary,
	(lambda qi: qi == 0 or qi == 1 or qi == 2), 0,
	(lambda qi, c: 1 if qi == 0 and c == '1' else 2 if qi == 1 and c == '1' else 2 if qi == 2 else 0),
	(lambda qi: qi == 2))

#even amount of elements
dfaEven = DFA(binary,
	(lambda qi: qi == 0 or qi == 1), 0,
	(lambda qi, c: 1 if qi == 0 and c else 0),
	(lambda qi: qi == 0))
#odd amount of element
dfaOdd = DFA(binary,
    (lambda qi: qi == 0 or qi == 1), 0,
    (lambda qi, c: 1 if qi == 0 and c else 0),
    (lambda qi: qi == 1))
#bin value even
dfaBinEven = DFA(binary,
    (lambda qi: qi == 0 or qi == 1), 0,
    (lambda qi, c: 1 if c == '0' else 0),
    (lambda qi: qi == 1))
#bin value is odd
dfaBinOdd = DFA(binary,
   (lambda qi: qi == 0 or qi == 1), 0,
   (lambda qi, c: 0 if c == '0' else 1),
   (lambda qi: qi == 1))

#random test cast to see if the first element is a *
dfaStrCase = DFA(alpha,
	(lambda qi: qi == 0 or qi == 1 or qi == 2), 0,
	(lambda qi, c: 1 if qi == 0 and c == '*' else 1 if qi == 1 else 2),
	(lambda qi: qi == 1))



tests = [('0', False), ('1', False), ('0000', True), ('0100', True), ('010010', True)]
dfaTestingDriver(Zeros, tests)

tests = [('0', False), ('1', False), ('1111', True), ('1011', True), ('101101', True)]
dfaTestingDriver(Ones, tests)

tests = [('0', False), ('1', False), ('000', True), ('011', False), ('0000', True)]
dfaTestingDriver(dfaEven, tests)

tests = [('0', True), ('1', True), ('010', True), ('011', True), ('0000', False)]
dfaTestingDriver(dfaOdd, tests)

tests = [('0', True), ('1', False), ('010', True), ('011', False), ('1110', True)]
dfaTestingDriver(dfaBinEven, tests)

tests = [('0', False), ('1', True), ('010', False), ('011', True), ('1011', True)]
dfaTestingDriver(dfaBinOdd, tests)

tests = [('*', True), ('*123', True), ('123*', False), ('trade***', False), ('', False)]
dfaTestingDriver(dfaStrCase, tests)
