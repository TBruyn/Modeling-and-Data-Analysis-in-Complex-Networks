import json
import networkx as nx
from networkx.readwrite import json_graph
import time
import GraphLoader
import random
import numpy as np

G = GraphLoader.load_page_subgraph()

for n in G.nodes:
    edges = G.edges(n, data=True)
    edges = [(u,v,d) for (u,v,d) in edges if u != v]
    rands = np.random.rand(len(edges) + 1)
    probs = (rands / np.sum(rands)).tolist()
    [d.update({'p':probs.pop()}) for (u,v,d) in edges if u != v]
    G.nodes[n]['attr_data']['p_exit'] = probs.pop()


GraphLoader.save_probability_graph(G, 'random_graph')
print("Created probability graph:")
print("Random")