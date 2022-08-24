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
    
    def __init__(self, name = None, typ = -2, **kwargs):
        '''
        As an AGraph, a clan consists of the corresponding 
        cluster subgraph, named, and the point that allows us
        to have it inside a larger clan; all this to be based
        on the now deprecated Sgton. Additionally it keeps
        its own type: -2 empty or singleton, -1 primitive, 
        n >= 0 color n; in case of modules n == 0 for nonedge
        and n == 1 for edge.
        Right now everything is still missing and we keep what
        we had for init in DecompTree.
        '''
        argsdict = { **kwargs }
        # ~ print("INIT args:", name, argsdict)
        # ~ if name is not None: 
            # ~ argsdict['name'] = name
        # ~ argsdict['directed'] = False
        # ~ argsdict['compound'] = True
        # ~ argsdict['newrank'] = True
        # ~ print("INIT new args:", name, argsdict)
        super().__init__(**argsdict)
        self.typ = typ

