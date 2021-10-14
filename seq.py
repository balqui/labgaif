'''
Dot files for sequence of decomposition
'''

from maindecomposition import decompose, stdGgraph, hack_items_in, hack_graph_in

from td2dot import read_graph_in 
# ~ from td2dot import dump_graph # might become necessary to track read in graph

datasetfile = 'e13'


go_on = True
count = 0

while go_on and count < 5:
    "please don't try to go beyond 7 for the time being"
    
    count += 1

    graph, items, go_on = read_graph_in(datasetfile + '.td', count)
    
    # ~ print(len(items))

    # make items available as global variable, necessary for Ely's code to work
    # there, replace '-' and '=' in names as disallowed by dot
    # means currently:
    #      TotalAttributesValues = [ item.replace('-', '_').replace('=', '_') for item in items ] 
    hack_items_in(items)

    my_graph = stdGgraph(graph, items)
    
    # make my_graph available as global variable, necessary for Ely's code to work
    hack_graph_in(my_graph)
    
    # decompose it and write dot file
    decompose(my_graph, '2', datasetfile + '_decomp_' + str(count))
    
    # then read that file into a pgv AGraph and call layout with dot and draw with pygame
    
