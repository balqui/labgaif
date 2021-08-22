'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary little functions.

In delbl we should keep alphabetic versions of digits
'''

def delbl(lbl):
	'''reduce lbl to only alpha chars, capitalized'''
	return ''.join( c for c in lbl if c.isalpha() ).capitalize()

def q(s):
    'quote string s'
    return '"' + s + '"'

