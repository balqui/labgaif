#! /usr/bin/env python3

'''
Tests of the various cases; this file: only cases 1a (x2) and 1b (single nonsingleton sibling)
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


filename = "titanic_"
fullfilename = filename + ".td"

g_raw, items = read_graph_in(fullfilename)
gr = AGraph(name = delbl(filename), directed = False)
nm = make_agraph(g_raw, items, gr)
# ~ show_graph(gr, items, nm)

# Titanic nodes in order of edge weight, computed separately:
# ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 'Survived_Yes', 'Class_3rd', 'Sex_Female', 'Class_1st', 'Class_2nd', 'Age_Child']
# ittit = ['Sex_Male', 'Survived_No', 'Class_Crew', 'Class_3rd', 'Class_1st', 'Class_2nd', 'Age_Child']
ittit = ['Survived_No', 'Class_Crew', 'Survived_Yes', 'Class_3rd', 'Class_1st', 'Class_2nd', 'Age_Child']
# ittit = ['Class_Crew', 'Class_3rd', 'Class_1st', 'Class_2nd', 'Survived_Yes', 'Survived_No', 'Age_Child']


dtree = DecompTree(compound = True, newrank = True)
dtree.setup(delbl(filename))

# starting with one or two vertices
# ~ st = 1
st = 2

if st == 1:
    dtree.start_dec_1(gr, Sgton(ittit[0]))
else:
    dtree.start_dec(gr, Sgton(ittit[0]), Sgton(ittit[1])) 

szdraw = 7
for it in ittit[st:szdraw]:
    dtree.root = dtree.add2tree(gr, dtree.root, Sgton(it))
dtree.layout("dot")
outfile = "dt1abcd_" + str(szdraw) + "s" + str(st) + "_00.png"
dtree.draw(outfile)
print("Wrote", outfile)




