'''
Trying it standalone.
Some strange error arose in te union/find str
but I cannot reproduce them anymore :(

if x.parent == x:
AttributeError: 'str' object has no attribute 'parent'
'''

from decomp import main

# JLB: to handle transactional file via github's labgaif/td2dot.py
from td2dot import read_graph_in #, dump_graph

# JLB: several functions follow to reformat graph as required by Ely's code

# JLB: from labeled graph to thresholded Gaifman graph 
def stdGgraph(graph, items, thr = 0):
	"list of lists of adjacency 0/1 booleans, optional lower threshold"
	MyGraph = []
	for r in items:
		"create each graph-matrix row"
		row = []
		for c in items:
			if graph[r][c] > thr:
				row.append([1]) # yes, a list of length 1, who knows why
			else:
				row.append([0])
		MyGraph.append(row)
	return MyGraph

# JLB: just recode the labeled graph as required by Ely's code
def labGgraph(graph, items):
	"list of lists of adjacency counts"
	MyGraph = []
	for r in items:
		"create each graph-matrix row"
		row = []
		for c in items:
			row.append([graph[r][c]]) # yes, a list of length 1, who knows why
		MyGraph.append(row)
	return MyGraph




datasetfile = 'titanic_'

# JLB: read labeled Gaifman graph, for now file hardwired
graph, items = read_graph_in(datasetfile + '.td')

# JLB: make items available as global variable, necessary for Ely's code to work
# JLB: there, replace '-' in names as disallowed by dot
TotalAttributesValues = [ item.replace('-', '_').replace('=', '_') for item in items ] 

# JLB: option 1 for original graph 
# MyGraph = labGgraph(graph, items)

# JLB: option 2 for standard Gaifman graph: thresholded graph with default 0 threshold
MyGraph = stdGgraph(graph, items)

# JLB: option 3 for thresholded graph with default 0 threshold
# MyGraph = stdGgraph(graph, items, 344) # OK 344 OR MORE, BUT WITH 343 OR LESS IT FAILS!	

# JLB: hardwire option for the time being
main(MyGraph, '2', datasetfile + '_decomp')

