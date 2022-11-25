import networkx as nx
import matplotlib.pyplot as plt
   
  
# Defining a Class
class GraphVisualization:
   
    def __init__(self):
        self.visual = dict()
          
    def addEdge(self, a, b, peso=1):
        temp = (a, b,peso)
        self.visual.setdefault(palavra,set(data_set[tweet].replace(palavra,'').split())).update(data_set[tweet].replace(palavra,'').split())
        print(peso)
          
    def visualize(self):
        G = nx.Graph()
        G.add_weighted_edges_from(self.visual)
        pos = nx.spring_layout(G, seed=7)
        nx.draw_networkx_nodes(G, pos, node_size=400)
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, "weight"))
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
  
G = GraphVisualization()
G.addEdge('sa', 'fd')
G.addEdge(1, 2)
G.addEdge(1, 3)
G.addEdge(5, 3)
G.addEdge(3, 4)
G.addEdge(1, 0)
G.addEdge(2,1)
G.visualize()