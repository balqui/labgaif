#! /usr/bin/env python3

'''
Towards decomposing graphs and 2-structures on top of
pygraphviz's AGraph graphs; assumed to have been already
constructed with separate singletons by make_agraph in
labgaif/td2dot.py

ToDo: 
. proper init of OurAGraph class
. try iterator on nodes instead of storing the nm list
. better yet, allow for an external iterator eg on decreasing edge weights

'''

from pygraphviz import AGraph
from td2dot import read_graph_in, make_agraph
from sgton import Sgton
from auxfun import delbl
from collections import defaultdict as ddict
from itertools import combinations

VERSION = "0.1 beta"

class DecompTree(AGraph):
    '''
    AGraph where we will be running the incremental decomposition algorithm.
    Has a dict self.typ mapping cluster names to types as follows:
        -1: primitive; N >= 0: complete and of "color" N; 
        as of today, just modules: 
        N == 0 for nonexistent edge, N == 1 for existing edge
    Has a specific clan which acts as root
    Currently has a list of nodes not yet added to the decomposition
    but this is likely to change.
    '''
    
    def setup(self, name):
        '''tried to do most of this upon __init__ but something ends up wrong'''
        self.graph_attr.name = name
        self.graph_attr.compound = "true"
        self.graph_attr.directed = "true"
        self.graph_attr.newrank = "true"
        self.typ = dict()

    def start_dec(self, gr, a, b):
        print("at start with:", a.dump_sgton(), b.dump_sgton())
        a.add_sgton(self)
        b.add_sgton(self)
        nmroot = 'cluster_' + a.nmr + '_' + b.nmr
        print(nmroot)
        self.root = self.add_subgraph([a.nmr, b.nmr], name = nmroot, rank = "same")
        if gr.has_edge(a.nmr, b.nmr):
            "only modules and no clans for now"
            self.add_edge(a.nmr, b.nmr)
            self.typ[nmroot] = 1
        else:
            self.typ[nmroot] = 0                


    def add2tree(self, gr, curr_root, node_to_add):
        '''
        case study according to -v and self.typ[curr_root]
        complete cases:
        1a: all visib with same color of clan, node is added
        1b: some but not all, separate them, recursively add to them
        1c: all visib with same color but not that of the clan: new size 2 clan
        1d: change it into primitive (more complicated case with splits)
        primitive cases:
        2a: same color pattern as one subclan: recursively add to it
        2b: like 1c
        2c: not all visible have same color: keep the node here and split as necessary
        '''
        node_to_add.add_sgton(self)
        sz = len(curr_root)
        print(sz, curr_root.name)
        vd = self.visib_dict(gr, curr_root, node_to_add.nmr)
        if len(vd[self.typ[curr_root.name]]) == sz:
            'case 1a'
            curr_root.add_node(node_to_add.nmr)
            if self.typ[curr_root.name] == 1:
                for n in curr_root:
                    if n != node_to_add.nmr:
                        print("add edge", n, node_to_add.nmr)
                        curr_root.add_edge(n, node_to_add.nmr)
        elif vd[self.typ[curr_root.name]]:
            'case 1b'
            to_sibling = list()
            for n in vd[1 - self.typ[curr_root.name]]:
                '''
                create sibling clan with the rest;
                this must become more sophisticate if we move beyond edges/nonedges
                '''
                to_sibling.append(n)
                curr_root.remove_node(n)
                # make clan with to_sibling nodes plus recursive call on curr_node
                # connect it with remaining curr_root
                # clarify whether/how curr_root gets updated
                print("Node", node_to_add.nmr, "not added, case 1b not completed yet")
        elif not vd[self.typ[curr_root.name]]:
            'case 1c'
            # aux_clan = curr_root
            nmnew = curr_root.name + '_' + node_to_add.nmr
            new_clan = self.subgraph([node_to_add], name = nmnew)
            for n in curr_root:
                new_clan.add_node(n)
            curr_root = new_clan
            print("Node", node_to_add.nmr, "not added, case 1c not completed yet")
        else:
            print("Node", node_to_add.nmr, "not added, case not covered so far")
    
    def visib_dict(self, gr, cl, nd):
        '''
        Visibility test, very slow and limited for the time being;
        all nodes inside clan/module cl are classified according to 
        which color, if any, are they seen from nd, class -1 if not seen;
        later must expand to treat adequately coarsest-quotient nodes.
        '''
        print("visib check for", cl.name, nd)
        d = ddict(list)
        for n in cl: 
            print("edge between", nd, "and", n, gr.has_edge(n, nd) or gr.has_edge(nd, n))
            c = 1 if gr.has_edge(n, nd) or gr.has_edge(nd, n) else 0
            d[c].append(n)
            print(n, "appended to color", c)
        return d

if __name__ == "__main__":
    
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = ("Construct dot-coded decomposition of a graph or 2-structure"),
        prog = "python[3] redecomp.py or just ./redecomp"
        )

    argp.add_argument('-V', '--version', action = 'version', 
                                         version = "redecomp " + VERSION,
                                         help = "print version and exit")

    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file (default: none, ask user)")
    
    args = argp.parse_args()

    if args.dataset:
        filename = args.dataset
    else:
        print("No dataset file specified.")
        filename = input("Dataset File Name? ")
    
    if '.' in filename:
        fullfilename = filename
        filename, ext = filename.split('.', maxsplit = 1)
        if ext != "td":
            print("Found extension", ext, "instead of td for file", filename)
    else:
        fullfilename = filename + ".td"


    g_raw, items = read_graph_in(fullfilename)

    gr = AGraph(name = delbl(filename), directed = "false")
    nm = make_agraph(g_raw, items, gr)
    print(items)
    for i, j in combinations(nm, 2):
        if gr.has_edge(i, j):
            print(i, j, gr.get_edge(i, j).attr["label"])
        else:
            print("no edge", i, j)

    dtree = DecompTree()
    dtree.setup(delbl(filename))
    
# following test requires at least 3 items
    # ~ dtree.start_dec(gr, Sgton(items[0]), Sgton(items[1])) 
    # ~ dtree.add2tree(gr, dtree.root, Sgton(items[2]))
    # ~ dtree.layout("dot")
    # ~ dtree.draw("dte.png")

# following tests only valid for Titanic
    # ~ if len(nm) > 8:
        # ~ dtree.start_dec(gr, Sgton(items[0]), Sgton(items[7])) 
        # ~ print(dtree.typ)
        # ~ print("next:", nm[4])
        # ~ dtree.add2tree(gr, dtree.root, Sgton(items[4]))
        # ~ dtree.layout("dot")
        # ~ dtree.draw("dt.png")

# Titanic nodes in order of edge weight, computed separately:
    ittit = ['PTAgeadult', 'PTSexmale', 'PTSurvivedno', 'PTClasscrew', 'PTSurvivedyes', 'PTClassrd', 'PTSexfemale', 'PTClassst', 'PTClassnd', 'PTAgechild']    
# Next goal not yet available: getting all the Titanic nodes in this order into the decomposition:
    dtree.start_dec(gr, Sgton(ittit[0]), Sgton(ittit[1])) 
    # ~ for it in ittit[2:]:
        # ~ dtree.add2tree(gr, dtree.root, Sgton(it))
    for it in ittit[2:3]:
        # one more node
        dtree.add2tree(gr, dtree.root, Sgton(it))
    dtree.layout("dot")
    dtree.draw("dt.png")

    

    





# might use AGraph.iternodes instead of nm

# ~ # double-checking everything:
    # ~ print("Internal AGraph names:", nm)
    # ~ g2 = AGraph(name = delbl(filename))
    # ~ nm = make_agraph(gr, items, g2)
    # ~ g2.draw(filename + "_sgtons.png", prog = "dot")
    
    # ~ g = OurAGraph(g.handle) # maybe it should not have the singletons from the start but acquire them in steps
    
# create root with two first nodes to start the decomposition, test
    # ~ g.start_dec(nm)
    # ~ g.draw(filename + "_started.png", prog = "dot")
    # ~ for nd in g.pend:
        # ~ print(nd, g.visib_dict(g.root, nd))
# now should loop on g0.pend to insert all the pending nodes
    # ~ for n in g.pend:
        # ~ g.add2tree(g.root, n)

#    g.layout("dot") # unnecessary here, gets called from draw
    # ~ g.draw(filename + "_redecomp.png", prog = "dot")

# Nejada's project may require nm to be sorted according to the edge labels


    
    





