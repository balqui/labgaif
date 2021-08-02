'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Class to test the dot code of singletons at the time of drawing 
graph or 2-structure decompositions.

'''

from auxfun import delbl

class Sgton:
	
	def __init__(self, lbl):
		self.lbl = delbl(lbl)
	
	def dotcode(self):
		s = "\nPT" + self.lbl + " [ shape = point ]\n"
		return s + "PT" + self.lbl + " -- " + self.lbl

if __name__ == "__main__":
	p = Sgton("3qp984hl")
	q = Sgton("3984hgf")
	print("graph g { " + p.dotcode() + q.dotcode())
	print("PT" + p.lbl + " -- " + "PT" + q.lbl + "[ style = dashed ] }")

