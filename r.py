
from pygraphviz import AGraph

dd = AGraph(name = "test", compound = "true", directed = "true", newrank = "true")
dd.add_node("a", shape = "point")
dd.add_node("b", shape = "point")
dd.add_subgraph(["a", "b"], name = 'cluster_a_b')

class D(AGraph):
    
    def __init__(self):
        super().__init__(name = "test", compound = "true", directed = "true", newrank = "true")
        self.add_node("a", shape = "point")
        self.add_node("b", shape = "point")
        self.add_subgraph(["a", "b"], name = 'cluster_a_b')

d = D()

    
