import pygraphviz as pgv

g = pgv.AGraph(compound = "true", directed = "true", newrank = "true") 
# compound allows for edge clipping at clusters
# newrank allows for same rank in clusters separately from general rank

g.edge_attr.update(arrowhead = "none")
g.add_edges_from(zip(range(6), range(1,7)))
sg = g.subgraph(range(3), "cluster012", rank = "same")
g.add_edge(1, 8, ltail = "cluster012")
g.layout("dot")
g.draw('g.png')



