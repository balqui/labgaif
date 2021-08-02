#! /usr/bin/env python3

'''
Towards decomposing graphs and 2-structures on top of
pygraphviz's AGraph graphs; assumed to have been already
constructed with separate singletons by make_agraph in
labgaif/td2dot.py

ToDo: 
. proper init of OurAGraph class
. try iterator on nodes instead of storing the nm list

'''

from pygraphviz import AGraph
from td2dot import read_graph_in, make_agraph
from auxfun import delbl

VERSION = "0.1 alpha"

class OurAGraph(AGraph):
    
    def start_dec(self, nm):
        if len(nm) > 1:
            a, b, *rest = nm
            nmroot = 'cluster_' + a + '_' + b
            self.root = self.add_subgraph([a, b], name = nmroot)
            self.pend = rest
# ~ # double-checking with colored subgraph instead
            # ~ self.root = self.add_subgraph([a, b], name = nmroot, style = 'filled', color = 'yellow')
            # ~ print("a, b, rest:", a, b, rest, self.pend)
            # ~ ggg = self.get_subgraph(nmroot)
            # ~ ggg.draw("e13_" + nmroot + "_subgraph.png", prog = "dot")

    def add2tree(self, curr_root, curr_node):
        pass

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
    g = AGraph(name = delbl(filename), compound = "True")
    nm = make_agraph(gr, items, g)

# compound allows for edge clipping at clusters

# might use AGraph.iternodes instead of nm

# ~ # double-checking everything:
    # ~ print("Internal AGraph names:", nm)
    # ~ g2 = AGraph(name = delbl(filename))
    # ~ nm = make_agraph(gr, items, g2)
    # ~ g2.draw(filename + "_sgtons.png", prog = "dot")
    
    g = OurAGraph(g.handle)
    
# create root with two first nodes to start the decomposition, test
    g.start_dec(nm)
    g.draw(filename + "_started.png", prog = "dot")
    
# now should loop on g0.pend to insert all the pending nodes
    for n in g.pend:
        g.add2tree(g.root, n)

# or alternatively loop on an iterator over the nodes and dispose of nm

#    g.layout("dot") # unnecessary here, gets called from draw
    g.draw(filename + "_redecomp.png", prog = "dot")
    


    
    





