#! /usr/bin/env python3

'''
Tests of the various cases; this file: lenses
'''

from pygraphviz import AGraph
from td2dot import read_graph_in, make_agraph
from sgton import Sgton
from auxfun import delbl
from itertools import combinations
from redecomp import DecompTree

VERSION = "0.1 alpha"

def show_graph(gr, items, nm):
    "show the graph data on console"
    print(items)
    for i, j in combinations(nm, 2):
        if gr.has_edge(i, j):
            print(i, j, gr.get_edge(i, j).attr["label"])
        else:
            print("no edge", i, j)
        if gr.has_edge(j, i):
            print(j, i, gr.get_edge(j, i).attr["label"])
        else:
            print("no edge", j, i)


filename = "lenses"
fullfilename = filename + ".td"

g_raw, items = read_graph_in(fullfilename)
gr = AGraph(name = delbl(filename), directed = False)
nm = make_agraph(g_raw, items, gr)
show_graph(gr, items, nm)

dtree = DecompTree(compound = True, newrank = True)
dtree.setup(delbl(filename))

dtree.start_dec_1(gr, Sgton(items[0]))

szdraw = 12
for it in items[1:szdraw]:
	if it not in ("soft", "hard"):
		"case 1d each"
		dtree.root = dtree.add2tree(gr, dtree.root, Sgton(it))
dtree.flatten_ranks()
dtree.layout("dot")
outfile = "dt_lenses_" + str(szdraw) + "_00.png"
dtree.draw(outfile)
print("Wrote", outfile)




