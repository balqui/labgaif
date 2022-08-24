#! /usr/bin/env python3

'''
Part of the refactoring of ../redecomp.py 0.1 gamma.

Try to isolate here everything that may depend on PyGraphviz
and the handling of the four related notions of a clan, a clan 
name, the vertex that represents the clan, and the name of the 
vertex, so that only the name of the vertex is needed outside
this class.
'''

from pygraphviz import AGraph
# ~ from td2dot import read_graph_in, make_agraph
# ~ from sgton import Sgton
# ~ from auxfun import delbl, grab_one
# ~ from collections import defaultdict as ddict
# ~ from itertools import combinations
VERSION = "0.2 alpha"

class Clan(AGraph):
    pass

