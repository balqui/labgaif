'''
Handle transactional file via github's labgaif/td2dot.py

Similar to integration tests inside maindecomposition but
trying them "from outside file".

Yesterday I got some strange error in the union/find str
but I cannot reproduce it anymore :(

It read:

if x.parent == x:
AttributeError: 'str' object has no attribute 'parent'
'''

from maindecomposition import decompose, stdGgraph, labGgraph, hack_items_in, hack_graph_in

from td2dot import read_graph_in 
# ~ from td2dot import dump_graph # might become necessary to track read in graph

datasetfile = 'titanic_'

graph, items = read_graph_in(datasetfile + '.td')

# make items available as global variable, necessary for Ely's code to work
# there, replace '-' and '=' in names as disallowed by dot
# means currently:
#      TotalAttributesValues = [ item.replace('-', '_').replace('=', '_') for item in items ] 
hack_items_in(items)

# option 1 for original labeled Gaifman graph
# ~ my_graph = labGgraph(graph, items)

# option 2 for standard Gaifman graph
my_graph = stdGgraph(graph, items)

# make my_graph available as global variable, necessary for Ely's code to work
hack_graph_in(my_graph)

#decompose it
decompose(my_graph, '2', datasetfile + '_std_decomp')

