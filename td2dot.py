#! /usr/bin/env python3

'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Construct labeled Gaifman graph of a transactional dataset.

Pending: smarter iterator on .td file to handle comments and such

Don't bother to import graphs from NetworkX, use case is easy enough.

Adjacency lists. 

Graph g is a dict of counters; g maps node u to g[u] which is a 
Counter of edges: g[u][v] gives how many occurrences we find of 
the pair (u, v) in a transaction.

Invariant: g[u][v] = g[v][u], careful with the redundancy at output time.

Filename used as dot graph name, hence no dots allowed in it.

'''

from collections import Counter, defaultdict
from itertools import combinations

VERSION = "0.0 alpha"


def q(s):
    'quote string s'
    return '"' + s + '"'

def read_graph_in(filename):
    '''
    filename must be a .td file containing only transactions:
    comments and other variations not supported yet
    '''
    gr = defaultdict(Counter)
    with open(filename) as f:
        for line in f:
            transaction = set(line.split())
            if transaction:
                for (u,v) in combinations(transaction, 2):
                    gr[u][v] += 1
                    gr[v][u] += 1
    return gr

def dump_graph(gr):
    for u in gr:
        for v in gr[u]:
            if u <= v:
                print(u, v, gr[u][v], gr[v][u])

def dot_output(gr, name):
    print("graph " + name + " {")
    for u in gr:
        for v in gr[u]:
            if gr[u][v] != gr[v][u]:
                print("Wrong count for items", u, "and", v)
                exit(-1)
            if u <= v:
                print(q(u), " -- ", q(v), "[ label = ", gr[u][v], "]")
    print("}")

if __name__ == "__main__":
    
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = ("Construct dot-coded labeled Gaifman graph" +
                       " from transactional dataset"),
        prog = "python[3] td2dot.py or just ./td2dot"
        )

    # ~ argp.add_argument('-v', '--verbose', action = 'store_true', 
                      # ~ help = "verbose report of current support at every closure")

    argp.add_argument('-V', '--version', action = 'version', 
                                         version = "td2dot " + VERSION,
                                         help = "print version and exit")

    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file (default: none, ask user)")
    
    args = argp.parse_args()

    # ~ if args.verbose:
        # ~ statics.verbose = True

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
    
    gr = read_graph_in(fullfilename)
    # ~ dump_graph(gr)
    dot_output(gr, filename)



