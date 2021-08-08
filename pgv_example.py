from itertools import product
import pygraphviz as pgv

d = pgv.AGraph(compound = "True") # compound allows for edge clipping at clusters
d.add_edges_from(product('ABCD', 'FGH'))
d.add_subgraph(nbunch = 'BC', name = 'clusterBC', style = 'filled', color = 'yellow')
d.add_node('X')
d.add_edge('X', 'B', lhead = 'clusterBC') # lhead does the clipping if compound is true

# ~ d.layout() # unnecessary if "draw" is called next

d.draw('d.png', prog = "dot")

# ~ G = pgv.AGraph(directed=True)
# ~ G.add_node(1)
# ~ G.add_node(2)
# ~ G.add_node(3)
# ~ G.add_node(4)
# ~ G1 = G.subgraph(nbunch=[1,2],name="cluster1")
# ~ G2 = G.subgraph(nbunch=[3,4],name="cluster2")
# ~ G.add_edge(1, 3, ltail = "cluster1")
# ~ G.write("g0.dot")
# ~ G.layout()
# ~ G.write("g1.dot")
# ~ G.draw('g.png', prog = "dot")


