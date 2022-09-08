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
from auxfun import delbl #, grab_one
# ~ from collections import defaultdict as ddict
# ~ from itertools import combinations
VERSION = "0.2 alpha"

class Clan(AGraph):
    
    def __init__(self, *inside, typ = -2, **kwargs):
        '''
        As an AGraph, a clan consists of the corresponding 
        cluster subgraph, named, and the point that allows us
        to have it inside a larger clan; all this to be based
        on the now deprecated Sgton. Additionally it keeps
        its own type: -2 singleton, -1 primitive, 
        n >= 0 color n; in case of modules n == 0 for nonedge
        and n == 1 for edge.
        Must clarify newrank.
        In case typ is primitive, maybe should store locally the
        colors of the edges within the clan.
        '''
        argsdict = { **kwargs }
        # ~ print("INIT args:", name, argsdict)
        argsdict['directed'] = False # override whatever comes in
        argsdict['compound'] = True  # ditto
        # ~ if name is not None: 
            # ~ 'else? / remember it must start with "cluster"'
            # ~ argsdict['name'] = name
        # ~ argsdict['newrank'] = True # NOT SURE OF THE EFFECT
        # ~ print("INIT new args:", name, argsdict)
        super().__init__(**argsdict)
        if len(inside) == 1:
            "singleton"
            self.typ = typ # should be -2
            self.lbl = inside[0] # should be a string, vertex info
            self.nms = delbl(inside[0])
            self.nmr = "PT_" + self.nms
            # ~ grph.add_node(self.nms, label = self.lbl) # WHO IS grph NOW?
            # ~ grph.add_node(self.nmr, shape = "point")
            # ~ grph.add_edge(self.nmr, self.nms)
        else:
            "nonsingleton"
            self.typ = typ

