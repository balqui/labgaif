#! /usr/bin/env python3

'''
Tests of the various cases; this file: case 1c followed by 1a
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


filename = "titanic_"
fullfilename = filename + ".td"

g_raw, items = read_graph_in(fullfilename)
gr = AGraph(name = delbl(filename), directed = "false")
nm = make_agraph(g_raw, items, gr)
# ~ show_graph(gr, items, nm)

# Titanic nodes in appropriate order for this case:
# ~ ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 'Survived_Yes', 'Class_3rd', 'Sex_Female', 'Class_1st', 'Class_2nd', 'Age_Child']
ittit = ['Age_Adult', 'Class_Crew', 'Age_Child', 'Survived_Yes']

dtree = DecompTree(compound = True, newrank = True)
dtree.setup(delbl(filename))
# ~ print(dtree.graph_attr.compound)

dtree.start_dec(gr, Sgton(ittit[0]), Sgton(ittit[1])) 

szdraw = 4
for it in ittit[2:szdraw]:
    dtree.root = dtree.add2tree(gr, dtree.root, Sgton(it))
dtree.flatten_ranks()
dtree.layout("dot")
outfile = "dt1c1a0_" + str(szdraw) + "s2.png"
dtree.draw(outfile)
print("Wrote", outfile)


