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

The inverted degree is calculated as 1 / degree

P[u -> v] = (inv_degree of v) / (sum of inv_degree of all neighbours of u + inv_degree u)
P[exit] = (inv_degree of u) / (sum of inv_degree of all neighbours of u + inv_degree u)

"""

tag = 'inverted_degree_only'

G = GraphLoader.load_page_subgraph()

degrees = nx.degree((G))
[d['attr_data'].update({'inv_degree': 1 / degrees[n]}) for n, d in G.nodes(data=True)]

for current in G.nodes:
    edges = G.edges(current, data=True)
    edges = [(u, v, d) for (u, v, d) in edges if u != v]
    views = {current: G.nodes[current]['attr_data']['inv_degree']}
    total = G.nodes[current]['attr_data']['inv_degree'] + \
            sum([G.nodes[neighbour]['attr_data']['inv_degree'] for (_, neighbour, _) in edges])

    [attributes.update({'p': G.nodes[neighbour]['attr_data']['inv_degree'] / total})
     for (_, neighbour, attributes) in edges]
    G.nodes[current]['attr_data']['p_exit'] = G.nodes[current]['attr_data']['inv_degree'] / total

GraphLoader.save_probability_graph(G, tag)
print("Created probability graph:")
print("Inverted degree only")
