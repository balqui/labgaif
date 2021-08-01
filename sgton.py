'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Class to handle the addition of singletons to pygraphviz Agraph 
objects in order to compute graph or 2-structure decompositions.

Adds both the separate, labeled singleton node and its unlabeled
big dot representative for use within the decomposing clusters.

Does not take into account potential duplicate names or even
names that become empty upon removing nonalpha chars.

'''

from itertools import combinations
from scaff import delbl
from pygraphviz import AGraph

class Sgton:
	
	def __init__(self, lbl):
		self.lbl = lbl
		self.nms = delbl(lbl)
		self.nmr = "PT" + delbl(lbl)

	def add_sgton(self, grph):
		grph.add_node(self.nms, label = self.lbl)
		grph.add_node(self.nmr, shape = "point")
		grph.add_edge(self.nmr, self.nms)

if __name__ == "__main__":
	g = AGraph()
	nodes = [ "aaw", "q3r", "aw4f", "awafww" ]
	pnames = []
	for n in nodes:
		s = Sgton(n)
		pnames.append(s.nmr)
		s.add_sgton(g)
	for e in combinations(pnames, 2):
		g.add_edge(e, style = "dashed")
	g.layout("dot")
	g.draw("t.png")

