import json
import networkx as nx
from networkx.readwrite import json_graph
import time
import GraphLoader
import random
import numpy as np
import pprint

"""

Create simple probability graph
P[u -> v] = (degree of v) / (sum of degree of all neighbours of u + degree u)
P[exit] = (degree of u) / (sum of degree of all neighbours of u + degree u)

"""

tag = 'degree_only'

G = GraphLoader.load_page_subgraph()

degrees = nx.degree((G))
[d['attr_data'].update({'degree': degrees[n]}) for n, d in G.nodes(data=True)]

for current in G.nodes:
    edges = G.edges(current, data=True)
    edges = [(u, v, d) for (u, v, d) in edges if u != v]
    views = {current: G.nodes[current]['attr_data']['degree']}
    total = G.nodes[current]['attr_data']['degree'] + \
            sum([G.nodes[neighbour]['attr_data']['degree'] for (_, neighbour, _) in edges])

    [attributes.update({'p': G.nodes[neighbour]['attr_data']['degree'] / total})
     for (_, neighbour, attributes) in edges]
    G.nodes[current]['attr_data']['p_exit'] = G.nodes[current]['attr_data']['degree'] / total

GraphLoader.save_probability_graph(G, tag)
print("Created probability graph:")
print("Degree only")
