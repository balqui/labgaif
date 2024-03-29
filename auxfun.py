'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary little functions.

In delbl we should keep alphabetic versions of digits

[Test of git issues, remove this line some day.]
'''

def delbl(lbl):
	'''reduce lbl to only alpha chars, capitalized'''
	return ''.join( c for c in lbl if c.isalnum() ).capitalize()

def q(s):
    'quote string s'
    return '"' + s + '"'

def grab_one(something):
	'''
	get some element from the something, that must be iterable and nonempty
	(probably there is some standard way to do this);
	if empty will return None
	'''
	for e in something:
		return e
