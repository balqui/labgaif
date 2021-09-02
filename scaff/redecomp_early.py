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
from auxfun import delbl
from collections import defaultdict as ddict

VERSION = "0.1 alpha"

class OurAGraph(AGraph):
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
    
    def start_dec(self, nm):
        self.typ = dict()
        if len(nm) > 1:
            a, b, *rest = nm
            nmroot = 'cluster_' + a + '_' + b
            self.root = self.add_subgraph([a, b], name = nmroot)
            if self.has_edge(a, b):
                self.typ[nmroot] = 1
                # ~ self.typ[nmroot] = self.get_edge(a, b).attr["label"]
            else:
                self.typ[nmroot] = 0                
            self.pend = rest
# ~ # double-checking with colored subgraph instead
            # ~ self.root = self.add_subgraph([a, b], name = nmroot, style = 'filled', color = 'yellow')
            # ~ print("a, b, rest:", a, b, rest, self.pend)
            # ~ ggg = self.get_subgraph(nmroot)
            # ~ ggg.draw("e13_" + nmroot + "_subgraph.png", prog = "dot")

    def add2tree(self, curr_root, curr_node):
        '''
        case study according to v and self.typ[curr_root]
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
        sz = len(curr_root)
        print(sz, curr_root.name)
        vd = self.visib_dict(curr_root, curr_node)
        if len(vd[self.typ[curr_root.name]]) == sz:
            'case 1a'
            curr_root.add_node(curr_node)
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
                print("Node", curr_node, "not added, case not completed yet")
        elif not vd[self.typ[curr_root.name]]:
            'case 1c'
            # aux_clan = curr_root
            nmnew = curr_root.name + '_' + curr_node
            new_clan = self.subgraph([curr_node], name = nmnew)
            for n in curr_root:
                new_clan.add_node(n)
            curr_root = new_clan
            print("Node", curr_node, "not added, case not completed yet")
        else:
            print("Node", curr_node, "not added, case not covered so far")
    
    def visib_dict(self, cl, nd):
        '''
        Visibility test, very slow and limited for the time being;
        all nodes inside clan/module cl are classified according to 
        which color, if any, are they seen from nd, class -1 if not seen;
        later must expand to treat adequately coarsest-quotient nodes.
        '''
        d = ddict(list)
        for n in cl: 
            c = 1 if self.has_edge(n, nd) else 0
            d[c].append(n)
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
    
    gr, items = read_graph_in(fullfilename)
    g = AGraph(name = delbl(filename), compound = "true", directed = "true", newrank = "true")
    nm = make_agraph(gr, items, g)

# might use AGraph.iternodes instead of nm

# ~ # double-checking everything:
    # ~ print("Internal AGraph names:", nm)
    # ~ g2 = AGraph(name = delbl(filename))
    # ~ nm = make_agraph(gr, items, g2)
    # ~ g2.draw(filename + "_sgtons.png", prog = "dot")
    
    g = OurAGraph(g.handle) # maybe it should not have the singletons from the start but acquire them in steps
    
# create root with two first nodes to start the decomposition, test
    g.start_dec(nm)
    g.draw(filename + "_started.png", prog = "dot")
    # ~ for nd in g.pend:
        # ~ print(nd, g.visib_dict(g.root, nd))
# now should loop on g0.pend to insert all the pending nodes
    for n in g.pend:
        g.add2tree(g.root, n)

#    g.layout("dot") # unnecessary here, gets called from draw
    g.draw(filename + "_redecomp.png", prog = "dot")

# Nejada's project may require nm to be sorted according to the edge labels
# We must leave room for OurAGraph to sort in various ways the pend list

    


    
    





