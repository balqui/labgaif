#! /usr/bin/env python3

from pygraphviz import AGraph
from td2dot import read_graph_in, make_agraph
from sgton import Sgton
from auxfun import delbl
from itertools import combinations
from redecomp import DecompTree

VERSION = "0.1 alpha"

def show_graph(gr):
    "show the graph data on console"
    for i, j in combinations(gr.nodes(), 2):
        if gr.has_edge(i, j):
            print(i, j, gr.get_edge(i, j).attr["label"])
        else:
            print("no edge", i, j)

gr = AGraph(name = "Small Test", directed = False)

for n in 'ABCDE':
	s = Sgton(n)
	s.add_sgton(gr)
for e in ['AB', 'AC', 'BC', 'DE']:
	gr.add_edge('PT'+e[0], 'PT'+e[1])
show_graph(gr)

dtree = DecompTree(compound = True, newrank = True)
dtree.setup("Small Test Decomp")
# ~ print(dtree.graph_attr.compound)

dtree.start_dec_1(gr, Sgton('a')) 

szdraw = 5
for it in 'bcde':
    dtree.root = dtree.add2tree(gr, dtree.root, Sgton(it))
dtree.flatten_ranks()
dtree.layout("dot")
outfile = "dt_small_test_s1.png"
dtree.draw(outfile)
print("Wrote", outfile)


