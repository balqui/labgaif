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
        '''
        tried to do most of this upon __init__ but something ends up wrong
        '''
        self.graph_attr.name = name
        self.graph_attr.compound = "true"
        self.graph_attr.directed = "true"
        self.graph_attr.newrank = "true"
        self.typ = dict()

    def start_dec(self, gr, a, b):
        print("Started with nodes:", a.lbl, b.lbl)
        a.add_sgton(self)
        b.add_sgton(self)
        nmroot = 'cluster_' + a.nmr + '_' + b.nmr
        self.root = self.add_subgraph([a.nmr, b.nmr], name = nmroot, rank = "same")
        print(nmroot, "--- just tried to get rank same")
        if gr.has_edge(a.nmr, b.nmr):
            "only modules and no clans for now"
            self.add_edge(a.nmr, b.nmr)
            self.typ[nmroot] = 1
        else:
            self.typ[nmroot] = 0                

    def start_dec_1(self, gr, v):
        "to test the new case sz == 1 of add2tree"
        v.add_sgton(self)
        nmroot = 'cluster_' + v.nmr
        self.root = self.add_subgraph([v.nmr], name = nmroot, rank = "same")
        print("Started with node", v.lbl)

    def add2tree(self, gr, curr_root, node_to_add):
        '''
        formerly, curr_root assumed to have two nodes at least,
        now attempt at making it work with curr_root of size just
        one vertex and, as it seems to work, we can simplify start_dec
        and case 1c;
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
        oftype = ''
        if curr_root.name in self.typ:
            oftype = "of type " + str(self.typ[curr_root.name])
        print("Adding", node_to_add.lbl, "to module", curr_root.name, "of size", sz, oftype)

        if sz == 1:
            for n in curr_root:
                "loop will run only once for the single vertex"
                # ~ print("Checking for edge", n, node_to_add.nmr)
                if gr.has_edge(n, node_to_add.nmr):
                    "only modules and no clans for now"
                    # ~ print("-- edge found")
                    self.add_edge(n, node_to_add.nmr)
                    self.typ[curr_root.name] = 1
                else:
                    # ~ print("-- edge not found")
                    self.typ[curr_root.name] = 0
            curr_root.add_node(node_to_add.nmr)
            return curr_root
# else, sz > 1:
        vd = self.visib_dict(gr, curr_root, node_to_add.nmr)   # PENDING: control for presence of -1
        print(vd)
        if len(vd[1 - self.typ[curr_root.name]]) == 0 and len(vd[-1]) == 0:
            'case 1a'
            print("case is 1a: node to be added and clan still complete")
            curr_root.add_node(node_to_add.nmr)
            if self.typ[curr_root.name] == 1:
                for n in curr_root:
                    if n != node_to_add.nmr:
                        curr_root.add_edge(n, node_to_add.nmr)

        elif vd[self.typ[curr_root.name]] and len(vd[-1]) == 0:
            'case 1b'
            print("case is 1b: node to be added to sibling")
            to_sibling = list()
            nmsibling = 'cluster'
            for n in vd[1 - self.typ[curr_root.name]]:
                '''
                create sibling clan with the rest;
                this must become more sophisticate if we move beyond edges/nonedges
                '''
                # ~ print("Sending to sibling:", n)
                to_sibling.append(n)
                nmsibling += "_" + n

            nmmedium = nmsibling + "_" + node_to_add.nmr
            if len(to_sibling) == 1:
                if to_sibling[0].startswith("PT_cluster"):
                    print("Single nonsingleton sibling", to_sibling[0])
                    sibl = self.get_subgraph(to_sibling[0][3:])
                    self.add2tree(gr, sibl, node_to_add) # what about the returning clan?
                else:
                    '''
                    only sibling is a singleton:
                    sibling clan unnecessary, just size-2 medium clan with new node and this one
                    complete but opposite to curr_root type
                    '''
                    print("Single singleton sibling", to_sibling[0])
                    n = to_sibling[0]
                    curr_root.remove_node(n)
                    if self.typ[curr_root.name] == 1:
                        "disconnect node n from rest of module"
                        for nn in curr_root.nodes(): 
                            self.delete_edge(n, nn)
                    medium_clan = self.subgraph([node_to_add.nmr, to_sibling[0]], name = nmmedium, rank = "same")
                    self.typ[nmmedium] = 1 - self.typ[curr_root.name]
                    if self.typ[nmmedium] == 1:
                        self.add_edge(node_to_add.nmr, to_sibling[0])
                    self.add_node("PT_"+nmmedium, shape = "point") 
                    self.add_edge("PT_"+nmmedium, to_sibling[0], lhead = nmmedium) # LOGICAL HEAD FAILS, WHY?
                    curr_root.add_node("PT_"+nmmedium)
                    if self.typ[curr_root.name] == 1:
                        for n in curr_root.nodes():
                            if n != "PT_"+nmmedium:
                                self.add_edge("PT_"+nmmedium,n)
            else:
                print("Size > 1 in to_sibling", nmsibling)
                for n in to_sibling:
                    curr_root.remove_node(n)
                    # ~ # wrong loop, it may disconnect things that go together later into to_sibling
                    # ~ if self.typ[curr_root.name] == 1:
                        # ~ "disconnect node n from rest of module"
                        # ~ for nn in curr_root.nodes(): 
                            # ~ self.delete_edge(n,nn)
                if self.typ[curr_root.name] == 1:
                    "now it is time for disconnecting once we know exactly who goes into to_sibling"
                    for n in to_sibling:
                        for nn in curr_root.nodes(): 
                            self.remove_edge(n,nn)
                sibling_clan = self.subgraph(to_sibling, name = nmsibling)
                self.typ[nmsibling] = self.typ[curr_root.name] # recursive call may change this
                sibling_clan = self.add2tree(gr, sibling_clan, node_to_add)
                nmsiblingpt = "PT_" + sibling_clan.name
                self.add_node(nmsiblingpt, shape = "point") 
                # ~ print("self.typ", curr_root.name, self.typ[curr_root.name])
                if self.typ[curr_root.name] == 1:
                    for nn in curr_root.nodes(): 
                        self.add_edge(nmsiblingpt,nn)
                curr_root.add_node(nmsiblingpt)
                self.add_edge(nmsiblingpt, grab_one(sibling_clan))

                # ~ sibling_clan = self.subgraph(to_sibling, name = nmsibling)
                # ~ self.typ[nmsibling] = self.typ[curr_root.name]
                # ~ # rest should be handled as a recursive call
                # ~ self.add_node("PT_"+nmsibling, shape = "point") 
                # ~ # medium_clan.add_node("PT_"+nmsibling)
                # ~ for nn in sibling_clan.iternodes():
                    # ~ # obtain a node nn in the clan, any node
                    # ~ break          
                # ~ self.add_edge("PT_"+nmsibling, nn)
            
            # ~ nmmedium = nmsibling+ "_"+node_to_add.nmr    
            # ~ medium_clan = self.subgraph([node_to_add.nmr,"PT_"+nmsibling], name = nmmedium)  
            # ~ medium_clan.graph_attr["rank"] = "same"

            # ~ if self.typ[curr_root.name] == 0:
                # ~ self.add_edge("PT_"+nmsibling , node_to_add.nmr)
                # ~ self.typ[nmmedium] = 1
            # ~ else:
                # ~ self.typ[nmmedium] = 0
            # ~ curr_root.add_node("PT_"+nmmedium, shape = "point")
            # ~ if self.typ[curr_root.name] == 1:
                # ~ for n in curr_root.nodes():
                    # ~ if n != "PT_"+nmmedium:
                        # ~ self.add_edge("PT_"+nmmedium,n)
            # ~ #self.add_edge("PT_"+nmmedium, "PT_"+nmsibling)
            # ~ for nn in medium_clan.iternodes():
                # ~ break            
            # ~ self.add_edge("PT_"+nmmedium, nn) #arrowhead = "none"
                
        elif not vd[self.typ[curr_root.name]] and len(vd[-1]) == 0:
            'case 1c'
            print("case is 1c: node and complete clan go into higher size-2 clan")
            pt_curr_root_nm = "PT_" + curr_root.name
            self.add_node(pt_curr_root_nm, shape = "point")
            # ~ trying to understand why lhead is not working 
            # ~ t = grab_one(curr_root)
            # ~ print("compound?", self.graph_attr.compound, t, pt_curr_root_nm, curr_root.name, t in curr_root)
            # ~ for n in curr_root: print(n)
            self.add_edge(pt_curr_root_nm, grab_one(curr_root), lhead = curr_root.name) #conectar PT de cuirrent_root a current_root
            nmnew = curr_root.name + '_' + node_to_add.nmr
            new_clan = self.subgraph([pt_curr_root_nm, node_to_add.nmr], name = nmnew)
            
            if self.typ[curr_root.name] == 0:
                self.add_edge(pt_curr_root_nm, node_to_add.nmr)
                self.typ[nmnew] = 1  
            else:
                self.typ[nmnew] = 0         
            return new_clan
          
        else:
            print("Node", node_to_add.nmr, "not added, case not covered so far")
        return curr_root # unchanged in case no previous return was found

    def visib_dict(self, gr, cl, nd):
        '''
        Visibility test, very slow and limited for the time being;
        all nodes inside clan/module cl are classified according to 
        which color, if any, are they seen from nd, class -1 if not seen;
        later must expand to treat adequately coarsest-quotient nodes.
        '''
        # ~ print("Visib check for", cl.name, nd)
        d = ddict(list)
        for n in cl: 
            if n.name.startswith("PT_cluster"): 
                "not sure whether get_subgraph might be slow"
                # ~ print("-- recursive call in visib check for:", n.name)
                subcl = self.get_subgraph(n.name[3:])
                dd = self.visib_dict(gr, subcl, nd)
                for c in dd:
                    if len(dd[c]) == len(subcl):
                        d[c].append(n)
                        break
                else:
                    d[-1].append(n)
            else:
                # ~ print("-- edge between", nd, "and", n, gr.has_edge(n, nd) or gr.has_edge(nd, n))
                c = 1 if gr.has_edge(n, nd) or gr.has_edge(nd, n) else 0
                d[c].append(n)
                # ~ print("--", n, "appended to color", c)
        # ~ print(d)
        return d

def grab_one(something):
	'''
	get some element from the something, that must be iterable and nonempty
	(probably there is some standard way to do this)
	'''
	for e in something:
		return e


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
    # ~ # show the graph data on console if convenient:
    # ~ print(items)
    # ~ for i, j in combinations(nm, 2):
        # ~ if gr.has_edge(i, j):
            # ~ print(i, j, gr.get_edge(i, j).attr["label"])
        # ~ else:
            # ~ print("no edge", i, j)

    dtree = DecompTree()
    dtree.setup(delbl(filename))

# Titanic nodes in order of edge weight, computed separately:
    ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 'Survived_Yes', 'Class_3rd', 'Sex_Female', 'Class_1st', 'Class_2nd', 'Age_Child']

# starting with one or two vertices
    st = 1
    # ~ st = 2
    
    if st == 1:
        dtree.start_dec_1(gr, Sgton(ittit[0]))
    else:
        dtree.start_dec(gr, Sgton(ittit[0]), Sgton(ittit[1])) 

# Next goal not yet available: getting all the Titanic nodes in this order into the decomposition:
    szdraw = 9
    for it in ittit[st:szdraw]:
        "careful, this has changed and now add2tree returns a possibly new root"
        dtree.root = dtree.add2tree(gr, dtree.root, Sgton(it))
    dtree.layout("dot")
    outfile = "dt" + str(szdraw) + "s" + str(st) + ".png"
    dtree.draw(outfile)
    print("Wrote", outfile)


# Alternative test using start decomp with a single node and calling add2tree with singleton module
    # ~ dtree.start_dec_1(gr, Sgton(ittit[0]))
    # ~ dtree.add2tree(gr, dtree.root, Sgton(ittit[1])) 
    # ~ dtree.add2tree(gr, dtree.root, Sgton(ittit[2])) 
    # ~ dtree.layout("dot")
    # ~ dtree.draw("dt_1_1.png")
