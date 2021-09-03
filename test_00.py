#! /usr/bin/env python3

'''
Tests of the various cases; this file: graph of a single node
'''

from pygraphviz import AGraph
from redecomp import DecompTree
from sgton import Sgton

VERSION = "0.1 alpha"

gname = "Single-node graph"
gr = AGraph(name = gname, directed = "false")
gr.add_node("Single node")

dtree = DecompTree()
dtree.setup(gname)

dtree.start_dec_1(gr, Sgton("Single node"))
dtree.layout("dot")
outfile = "dt_00.png"
dtree.draw(outfile)
print("Wrote", outfile)




