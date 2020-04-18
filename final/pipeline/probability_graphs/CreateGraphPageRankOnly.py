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
P[u -> v] = (pagerank of v) / (sum of pagerank of all neighbours of u + pagerank u)
P[exit] = (pagerank of u) / (sum of pagerank of all neighbours of u + pagerank u)

"""

tag = 'pagerank_only'

G = GraphLoader.load_page_subgraph()

pagerank = nx.pagerank(G)

[d['attr_data'].update({'pagerank': pagerank[n]}) for n, d in G.nodes(data=True)]

for current in G.nodes:
    edges = G.edges(current, data=True)
    edges = [(u, v, d) for (u, v, d) in edges if u != v]
    views = {current: G.nodes[current]['attr_data']['pagerank']}
    total = G.nodes[current]['attr_data']['pagerank'] + \
            sum([G.nodes[neighbour]['attr_data']['pagerank'] for (_, neighbour, _) in edges])

    [attributes.update({'p': G.nodes[neighbour]['attr_data']['pagerank'] / total})
     for (_, neighbour, attributes) in edges]
    G.nodes[current]['attr_data']['p_exit'] = G.nodes[current]['attr_data']['pagerank'] / total

GraphLoader.save_probability_graph(G, tag)
print("Created probability graph:")
print("Pagerank only")