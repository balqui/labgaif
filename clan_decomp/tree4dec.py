#! /usr/bin/env python3

'''
Tree-like PyGraphviz AGraph supporting basic operations for
the modular/clan decomposition of graphs/2-structures.
To be extended into the decomposition tree proper in the
decomp_tree.py module.

Drawing correctly the path primitive modules requires a
directed graph; using edge_attr["dir"] = "none" to avoid
drawing the arrows.
'''

from pygraphviz import AGraph

class Tree4Dec(AGraph):
    '''
    Has a specific clan that acts as root
    '''

    def __init__(self, **kwargs):
        kwargs["directed"] = True # override potential alternative
        kwargs['compound'] = True # think about newrank too
        super().__init__(**kwargs)
        self.edge_attr["dir"] = "none" # draw edges as undirected
        self.namecount = 100
        self.root = None

    def new_name(self):
        self.namecount += 1
        return "s" + str(self.namecount)

    def first_vertex(self, lbl):
        assert self.root is None
        



