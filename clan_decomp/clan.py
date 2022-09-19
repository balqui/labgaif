#! /usr/bin/env python3

'''
Part of the refactoring of ../redecomp.py 0.1 gamma.

STALLED.

Try to isolate here everything that may depend on PyGraphviz
and the handling of the four related notions of a clan, a clan 
name, the vertex that represents the clan, and the name of the 
vertex, so that only the name of the vertex is needed outside
this class.

Mid September: CAREFUL. add_subgraph takes LINEAR time on the
WHOLE set of edges of the WHOLE graph as it traverses all the 
edges to see whether they are part of the subgraph. 
Also: the subgraph is a separate instance of AGraph.

MANY opportunities to slow down very much the algorithm. However,
current decision is to keep going for the time being and leave
these considerations for future refactoring.

EVEN THEN: GIVING UP. THE IDEA OF Clan subclass_of AGraph
IS AGAIN VERY DOUBTFUL.
'''

from pygraphviz import AGraph
# ~ from td2dot import read_graph_in, make_agraph
# ~ from sgton import Sgton
from auxfun import delbl #, grab_one
# ~ from collections import defaultdict as ddict
# ~ from itertools import combinations
VERSION = "0.2 alpha"

class Clan(AGraph):

    def __init__(self, grph, *inside, typ = -2, **kwargs):
        '''
        As an AGraph, a clan consists of either the corresponding  
        cluster subgraph, named, or a data vertex; plus the point  
        that allows us to have it inside a larger clan. 
        The data vertex case is based on the now deprecated Sgton. 
        Additionally it keeps its own type: -2 singleton, -1 primitive, 
        n >= 0 color n; in case of modules: n == 0 for nonedge
        and n == 1 for edge.
        Must clarify newrank.
        In case typ is primitive, maybe should store locally the
        colors of the edges within the clan. How slow would that be?
        For the time being, no provision is made to provide the clan
        name from outside.
        '''
        argsdict = { **kwargs }
        # ~ print("INIT args:", inside, argsdict)
        argsdict['directed'] = False # override whatever comes in
        argsdict['compound'] = True  # ditto
        # ~ argsdict['newrank'] = True # NOT SURE OF THE EFFECT
        # ~ print("INIT new args:", name, argsdict)
        super().__init__(**argsdict)
        if len(inside) == 1:
            "singleton"
            self.typ = typ # should be -2
            self.lbl = inside[0] # should be a string, vertex info
            self.nms = delbl(inside[0])
            self.nmr = "PT_" + self.nms
            self.add_node(self.nms, label = self.lbl)
            self.add_node(self.nmr, shape = "point")
            self.add_edge(self.nmr, self.nms)
            grph.add_subgraph(self)
            print(self)
            print(grph)
        else:
            "nonsingleton - to complete - unclear how edges are handled"
            self.typ = typ
            name = "cluster_"
            for v in inside:
                "recall that PyGraphviz nodes subclass str"
                name += v
            self.nmr = "PT_" + self.nms
            self.add_node(self.nmr, shape = "point")
            self.add_edge(self.nmr, self.nms)
            grph.add_subgraph(self.nodes(), name = name)
        # ~ return sgrph - can't do that!

    # ~ def make_clan_of(self, grph):
        # ~ "add clan as cluster subgraph of grph"
        # ~ grph.add_nodes_from(self.nodes())
        # ~ grph.add_edges_from(self.edges())
        # turns out all that is done within add_subgraph
        # ~ sgrph = grph.add_subgraph(self.nodes())
        # ~ return sgrph



if __name__ == "__main__":
    from itertools import combinations
    g = AGraph()
    nodenames = [ "aaw", "q3r", "aw4f", "awafww" ]
    clanlist = []
    for n in nodenames:
        clanlist.append(Clan(g, n))
    # ~ sglist = []
    # ~ for c in clanlist:
        # ~ sglist.append(c.make_clan_of(g))
    print(list(l.nms for l in clanlist))
    # ~ print(list(str(l) for l in sglist))
    print(g)
    # ~ for e in combinations(pnames, 2):
        # ~ g.add_edge(e, style = "dashed")
    # ~ g.layout("dot")
    # ~ g.draw("t.png")
