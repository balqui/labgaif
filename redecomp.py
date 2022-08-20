#! /usr/bin/env python3

'''
Towards decomposing graphs and 2-structures on top of
pygraphviz's AGraph graphs; assumed to have been already
constructed with separate singletons by make_agraph in
labgaif/td2dot.py

ToDo: 
. complete all cases, now just minimal to handle titanic plain
.. only two colors, edge and nonedte
.. 1a, 1b and 1c complete, 2b probably too
.. 1d advanced but 
... still lacks split of primitive clans and
... does not keep track of colors of split complete clans beyond one level 
. stay alert about proper init of DecompTree (see file CAREFUL.txt)
. try iterator on nodes instead of storing the nm list
. better yet, allow for an external iterator eg on decreasing edge weights
. right now undirected: 
.. directed requires handling with care the removal of edges upon 
   moving a node to a sibling
.. should it be directed even if arrows are removed from drawing?

'''

from pygraphviz import AGraph
from td2dot import read_graph_in, make_agraph
from sgton import Sgton
from auxfun import delbl, grab_one
from collections import defaultdict as ddict
from itertools import combinations
VERSION = "0.1 gamma"

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

    # ~ def __init__(self):
		# ~ "Early failing attempt"
        # ~ super().__init__(name = "test", compound = "true", directed = "true", newrank = "true")

    # ~ def setup(self, name):
        # ~ '''
        # ~ attempt at avoiding a specific __init__
        # ~ (see file CAREFUL.txt); 
        # ~ name and directed only seem to work upon constructing call, 
        # ~ not here at all; the others give the choice.
        # ~ '''
        # ~ self.typ = dict() # types of each of the subclans in the partition (I believe, check out)
        # ~ self.graph_attr["compound"] = "true" # this works here and also at constructing call
        # ~ self.graph_attr["newrank"] = "true" # this works here and also at constructing call
        # ~ self.graph_attr["directed"] = True # does not seem to have an effect
        # ~ self.graph_attr.name = name

    # ~ def __init__(self, **kwargs):
		# ~ "Ross Barnowsky's suggestion in the dialog at the GitHub PyGraphviz issue, rossbar@GitHub"
        # ~ super().__init__(name="test", compound="true", directed="true", newrank="true")

    def __init__(self, name = None, **kwargs):
        '''
        Clarify class of subgraphs: DecompTree or AGraph? 
        Dict typ's everywhere in the first case.
        '''
        argsdict = { **kwargs }
        # ~ print("INIT:", name, argsdict)
        if name is not None: 
            argsdict['name'] = name
        argsdict['directed'] = False
        argsdict['compound'] = True
        argsdict['newrank'] = True
        # ~ print("INIT mid:", name, argsdict)
        super().__init__(**argsdict)
        self.typ = dict() # types of all clans in the decomp (I believe, check out)

    def clus_from_repr(self, name):
        "from node name pointing to cluster PT_..., get the cluster name"
        if name.startswith("PT_cluster"):
            return self.get_subgraph(name[3:]) # causes a call to __init__ (!)

    def flatten_ranks(self, clus = None):
        "set rank at same for modules without edges or modules of size 2"
        if clus is None:
            clus = self.root
        # ~ print("flattening:", clus.name, '/' + clus.graph_attr["rank"] + '/' if "rank" in clus.graph_attr else "no rank")
        if len(clus) < 3 or self.typ[clus.name] == 0: 
            clus.graph_attr["rank"] = "same"
        # ~ if len(clus) < 5 and self.typ[clus.name] == -1):
            # ~ "path: reorder correctly and then:"
            # ~ clus.graph_attr["rank"] = "same"
            # ~ print("flattened:", clus.name)
        # ~ print("flattened:", clus.name, '/' + clus.graph_attr["rank"] + '/' if "rank" in clus.graph_attr else "no rank")
        for nm in clus:
            n = self.clus_from_repr(nm)
            if n is not None:
                self.flatten_ranks(n)

    # ~ def start_dec(self, gr, a, b):
        # ~ "early start from two nodes, now deprecated, please start with one and add the other"
        # ~ print("Start with nodes:", a.lbl, b.lbl)
        # ~ a.add_sgton(self)
        # ~ b.add_sgton(self)
        # ~ nmroot = 'cluster_' + a.nmr + '_' + b.nmr
        # ~ self.root = self.add_subgraph([a.nmr, b.nmr], name = nmroot) # , rank = "same")
        # ~ if gr.has_edge(a.nmr, b.nmr):
            # ~ "only modules and no clans for now"
            # ~ self.add_edge(a.nmr, b.nmr)
            # ~ self.typ[nmroot] = 1
        # ~ else:
            # ~ self.typ[nmroot] = 0                

    def start_dec(self, gr, v):
        "uses case sz == 1 of add2tree"
        print("Start with node", v.lbl)
        v.add_sgton(self)
        nmroot = 'cluster_' + v.nmr
        self.root = self.add_subgraph([v.nmr], name = nmroot) #, rank = "same") # not good for over 2 vertices

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
        sz = len(curr_root)
        oftype = ''
        if curr_root.name in self.typ:
            oftype = "of type " + str(self.typ[curr_root.name])
        print("Adding", node_to_add.lbl, "to module", curr_root.name, "of size", sz, oftype)
        node_to_add.add_sgton(self)

        if sz == 1:
            print("Adding it to a singleton.")
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
        if len(vd[t := self.typ[curr_root.name]]) == sz and t != -1:
            'case 1a'
            print("case is 1a: node to be added and clan still complete")
            curr_root.add_node(node_to_add.nmr)
            if self.typ[curr_root.name] == 1:
                for n in curr_root:
                    if n != node_to_add.nmr:
                        curr_root.add_edge(n, node_to_add.nmr)

        elif vd[t := self.typ[curr_root.name]] and t != -1:
            'case 1b - do we need to test for len(vd[-1]) == 0?'
            print("case is 1b: node to be added to sibling")
            to_sibling = list()
            nmsibling = 'cluster'
            for n in vd[1 - self.typ[curr_root.name]]:
                '''
                create sibling clan with the rest;
                here the other color, below the nonvisible;
                all this must become more sophisticate 
                if we move beyond edges/nonedges
                '''
                print("Sending to sibling:", n)
                to_sibling.append(n)
                nmsibling += "_" + n
            for n in vd[-1]:
                '''
                nonvisibles too!
                '''
                print("Sending to sibling:", n)
                to_sibling.append(n)
                nmsibling += "_" + n

            nmmedium = nmsibling + "_" + node_to_add.nmr
            if len(to_sibling) == 1:
                if to_sibling[0].startswith("PT_cluster"):
                    print("Single nonsingleton sibling", to_sibling[0]) # consider function clus_from_repr
                    sibl = self.get_subgraph(to_sibling[0][3:])
                    self.add2tree(gr, sibl, node_to_add) # what about the returning clan?
                else:
                    '''
                    only sibling is a singleton:
                    sibling clan unnecessary, just size-2 medium clan with new node and this one
                    complete but opposite to curr_root type (what happens with several colors?)
                    '''
                    print("Single singleton sibling", to_sibling[0])
                    n = to_sibling[0]
                    curr_root.remove_node(n)
                    if self.typ[curr_root.name] == 1:
                        "disconnect node n from rest of module"
                        for nn in curr_root.nodes():
                            # ~ print("removing", n, nn)
                            self.delete_edge(n, nn)
                    medium_clan = self.subgraph([node_to_add.nmr, to_sibling[0]], name = nmmedium) # , rank = "same")
                    self.typ[nmmedium] = 1 - self.typ[curr_root.name]
                    if self.typ[nmmedium] == 1:
                        self.add_edge(node_to_add.nmr, to_sibling[0])
                    self.add_node("PT_"+nmmedium, shape = "point") 
                    self.add_edge("PT_"+nmmedium, to_sibling[0], lhead = nmmedium)
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
                    '''now it is time for disconnecting once we know 
                    exactly who goes into to_sibling - but not sure
                    how this works for several colors!
                    '''
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
                    '''many places around would fail with several colors'''
                    for nn in curr_root.nodes(): 
                        self.add_edge(nmsiblingpt, nn)
                curr_root.add_node(nmsiblingpt)
                self.add_edge(nmsiblingpt, grab_one(sibling_clan), lhead = sibling_clan.name)

        elif not vd[self.typ[curr_root.name]] and not vd[-1]:
            '''case 1c and maybe we can use the same code for 2b,
            trying that out but careful with several colors
            '''
            print("case is 1c: node and complete clan go into higher size-2 clan")
            pt_curr_root_nm = "PT_" + curr_root.name
            self.add_node(pt_curr_root_nm, shape = "point")
            nmnew = curr_root.name + '_' + node_to_add.nmr
            new_clan = self.subgraph([pt_curr_root_nm, node_to_add.nmr], name = nmnew)
            self.add_edge(pt_curr_root_nm, grab_one(curr_root), lhead = curr_root.name) #conectar PT de cuirrent_root a current_root

            if self.typ[curr_root.name] == 0:
                'to work out with several colors'
                self.add_edge(pt_curr_root_nm, node_to_add.nmr)
                self.typ[nmnew] = 1  
            else:
                self.typ[nmnew] = 0         
            return new_clan

        elif self.typ[curr_root.name] != -1:
            '''case 1d: complete clan, all connections in a 
            different color or non-visible - warning, in vd
            we only have names, not nodes
            '''
            print("case is 1d")
            for n in curr_root:
                print("### Currently in root:", n.name)
            print("### Type of root:", self.typ[curr_root.name])
            to_split = set()
            for n in curr_root:
                if n.name in vd[1]:
                    self.add_edge(n, node_to_add.nmr)
                if n.name in vd[-1]:
                    curr_root.remove_node(n)
                    to_split.add(n)
            print("-----", to_split)
            if self.typ[curr_root.name] == 1:
                for n in to_split:
                    for nn in curr_root.nodes(): 
                        try:
                            self.remove_edge(n,nn)
                        except KeyError:
                            "should not happen anymore"
                            print("KE - Tried to remove nonexistent edge", n, nn)
            d = ddict(set) # color as seen from node_to_add after split
            for nn in to_split:
                print("Splitting:", nn, node_to_add.nmr)
                nnn = self.get_subgraph(nn[3:])
                dd = self.clan_split(gr, nnn, node_to_add.nmr)
                self.remove_node(nn) # removes also edge between nn and nnn
                self.remove_subgraph(nnn.name)
                for c in (0, 1):
                    d[c].update(dd[c]) # Are we not losing connections among the outcomes of the split?
            print("-------", d)
            for n in curr_root:
                print("### Currently in root:", n.name)
            to_add = set()
            for c in (0, 1):
                if len(d[c]) == 1:
                    m = d[c].pop()
                else:
                    nm = 'cluster_'
                    for e in d[c]:
                        nm += e.name
                    self.subgraph(d[c], name = nm)
                    self.typ[nm] = 1 - self.typ[curr_root.name] # WORKS ONLY WHILE NO SPLITTING OF PRIMITIVES - IF AT ALL
                    m = "PT_" + nm
                    self.add_node(m, shape = "point") 
                    self.add_edge(m, grab_one(d[c]), lhead = nm)
                if self.typ[curr_root.name] == 1:
                    for n in curr_root:
                        self.add_edge(n, m)
                        print("### Edge", n.name, m)
                if c == 1:
                    self.add_edge(m, node_to_add.nmr)
                    print("### Edge", node_to_add.nmr, m)
                to_add.add(m)
            for m in to_add:
                curr_root.add_node(m)
                print("### Adding to root:", m)
            curr_root.add_node(node_to_add.nmr)
            print("### Adding to root finally:", node_to_add.nmr)
            self.typ[curr_root.name] = -1

        else:
            print("Node", node_to_add.nmr, "not added to", curr_root.name)
            print("Case not covered so far. But trying split.")
            print(self.clan_split(gr, curr_root, node_to_add))
            
        return curr_root # unchanged in case no previous return was found

    def visib_dict(self, gr, cl, nd):
        '''
        Visibility test, very slow and limited for the time being;
        all nodes inside clan/module cl are classified according to 
        which color, if any, are they seen from nd, class -1 if not seen;
        later must expand to treat adequately coarsest-quotient nodes.
        Also, right now it is called over and over with the same cl and nd.
        '''
        # ~ print("Visib check for", cl.name, nd)
        d = ddict(list)
        for n in cl: 
            if n.name.startswith("PT_cluster"): 
                "not sure whether get_subgraph might be slow"
                # ~ print("-- recursive call in visib check for:", n.name)
                subcl = self.get_subgraph(n.name[3:]) # causes a call to __init__ (!)
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
        # ~ for e in d: print("  ", e, d[e])
        # ~ print("==")
        return d

    def clan_split(self, gr, cl, nd):
        '''
        Split clan cl and below from nd using visib_dict
        as auxiliary to access gr.
        DecompTree self needed to find out the subgraph 
        members as in visib_dict (sounds strange).
        Just "colors" 0: no edge and 1: edge for now.
        Some day the calls to visib_dict should become 
        unnecessary, right now a lot of repeated computations.
        BAD THING: WE ARE LOSING THE INFO OF THEIR TYPES
        AS WE GO DOWN THE RECURSIVE CALLS, THUS LOSING 
        THE EDGES AMONG ELEMENTS OF THE OUTCOME
        '''
        vd = self.visib_dict(gr, cl, nd)
        if self.typ[cl.name] == -1:
            'primitive clan cl, PENDING'
            print("SPLITTING OF PRIMITIVE CLANS LIKE", cl.name, cl, "NOT IMPLEMENTED")
            exit()
        else:
            'complete clan'
            outd = ddict(set)
            for c in (0, 1):
                outd[c].update(vd[c])
            for n in vd[-1]:
                if n.name.startswith("PT_cluster"): 
                    print("-- recursive call to split:", n.name)
                    subcl = self.get_subgraph(n.name[3:]) # causes a call to __init__ (!)
                    dd = self.clan_split(gr, subcl, nd)
                    for c in (0, 1):
                        outd[c].update(dd[c])
                else:
                    print("!! ERROR, CHECK:", n, "found nonvisible from", nd)
                    exit()
            return outd


if __name__ == "__main__":
    
    filename = "titanic_" # TO BE REPLACED BY ARGUMENT PARSING AS FOLLOWS

    # ~ from argparse import ArgumentParser
    # ~ argp = ArgumentParser(
        # ~ description = ("Construct dot-coded decomposition of a graph or 2-structure"),
        # ~ prog = "python[3] redecomp.py or just ./redecomp"
        # ~ )

    # ~ argp.add_argument('-V', '--version', action = 'version', 
                                         # ~ version = "redecomp " + VERSION,
                                         # ~ help = "print version and exit")

    # ~ argp.add_argument('dataset', nargs = '?', default = None, 
                      # ~ help = "name of optional dataset file (default: none, ask user)")
    
    # ~ args = argp.parse_args()

    # ~ if args.dataset:
        # ~ filename = args.dataset
    # ~ else:
        # ~ print("No dataset file specified.")
        # ~ filename = input("Dataset File Name? ")
    
    if '.' in filename:
        fullfilename = filename
        filename, ext = filename.split('.', maxsplit = 1)
        if ext != "td":
            print("Found extension", ext, "instead of td for file", filename)
    else:
        fullfilename = filename + ".td"

    g_raw, items = read_graph_in(fullfilename)
    gr = AGraph(name = delbl(filename), directed = False)
    nm = make_agraph(g_raw, items, gr)
    # ~ # show the graph data on console if convenient:
    # ~ print(items)
    # ~ for i, j in combinations(nm, 2):
        # ~ if gr.has_edge(i, j):
            # ~ print(i, j, gr.get_edge(i, j).attr["label"])
        # ~ else:
            # ~ print("no edge", i, j)

    dtree = DecompTree(name = delbl(filename), # directed = True, # makes current version fail
    compound = True, newrank = "true")

# ~ # Titanic nodes in order of edge weight, computed separately, cases 1a and 1b until Age_Child 1d:
    ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 'Survived_Yes', 
    'Class_3rd', 'Sex_Female', 'Class_1st', 'Class_2nd', 'Age_Child']
# ~ # Ordering demonstrating cases 1a, 1b, 1c until Sex_Female:
    # ~ ittit = ['Class_1st', 'Class_2nd', 'Class_3rd', 'Sex_Male', 
    # ~ 'Sex_Female', 'Age_Child', 'Class_Crew',  'Age_Adult', 'Survived_No','Survived_Yes']
# Other test orderings:
    # ~ ittit = ['Sex_Male', 'Survived_No', 'Survived_Yes', 
    # ~ 'Class_3rd', 'Sex_Female', 'Class_1st', 'Class_2nd', 'Age_Child', 'Class_Crew', 'Age_Adult']
    # ~ ittit = ['Sex_Male', 'Class_3rd', 'Age_Child', 'Class_Crew', 'Age_Adult']
    # ~ ittit = ['Sex_Male', 'Age_Adult', 'Class_3rd', 'Age_Child', 'Class_Crew']
    # ~ ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 'Survived_Yes', 
    # ~ 'Class_3rd', 'Sex_Female', 'Age_Child'] # 'Class_1st', 'Class_2nd', 

# starting with one or two vertices deprecated, please start with a single one
    # ~ st = 1
    # ~ # st = 2
    
    # ~ if st == 1:
        # ~ dtree.start_dec_1(gr, Sgton(ittit[0]))
    # ~ else:
        # ~ dtree.start_dec(gr, Sgton(ittit[0]), Sgton(ittit[1])) 

    dtree.start_dec(gr, Sgton(ittit[0]))
    szdraw = 10
    mark = "s2"
    for it in ittit[1:szdraw]:
        "careful, add2tree returns a possibly new root"
        dtree.root = dtree.add2tree(gr, dtree.root, Sgton(it))
    dtree.flatten_ranks()
    dtree.layout("dot")
    outfile = "dt" + str(szdraw) + "_" + str(mark) + ".png"
    dtree.draw(outfile)
    print("Wrote", outfile)


# Alternative test using start decomp with a single node and calling add2tree with singleton module
    # ~ dtree.start_dec_1(gr, Sgton(ittit[0]))
    # ~ dtree.add2tree(gr, dtree.root, Sgton(ittit[1])) 
    # ~ dtree.add2tree(gr, dtree.root, Sgton(ittit[2])) 
    # ~ dtree.layout("dot")
    # ~ dtree.draw("dt_1_1.png")
