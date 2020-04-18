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

The inverted betweenness is (1 - B) where B is the betweenness on the undirected graph and is calculated per component

P[u -> v] = (inverted betweenness of v) / (sum of inverted betweenness of all neighbours of u + inverted betweenness u)
P[exit] = (inverted betweenness of u) / (sum of inverted betweenness of all neighbours of u + inverted betweenness u)

"""

tag = 'inverted_betweenness_only'

G = GraphLoader.load_page_subgraph()
undirected = G.to_undirected()

components = [undirected.subgraph(c) for c in nx.connected_components(undirected)]
betweenness = {}
[[betweenness.update({k: v}) for k, v in nx.betweenness_centrality(c).items()] for c in components]

min_b = min([betweenness[n] for n, d in G.nodes(data=True) if betweenness[n] > 0])
[betweenness.update({n: betweenness[n] + min_b}) for n, d in G.nodes(data=True)]

[d['attr_data'].update({'inverted_betweenness': 1 - betweenness[n]}) for n, d in G.nodes(data=True)]

for current in G.nodes:
    edges = G.edges(current, data=True)
    edges = [(u, v, d) for (u, v, d) in edges if u != v]
    views = {current: G.nodes[current]['attr_data']['inverted_betweenness']}
    total = G.nodes[current]['attr_data']['inverted_betweenness'] + \
            sum([G.nodes[neighbour]['attr_data']['inverted_betweenness'] for (_, neighbour, _) in edges])
    [attributes.update({'p': G.nodes[neighbour]['attr_data']['inverted_betweenness'] / total})
     for (_, neighbour, attributes) in edges]
    G.nodes[current]['attr_data']['p_exit'] = G.nodes[current]['attr_data']['inverted_betweenness'] / total

GraphLoader.save_probability_graph(G, tag)
print("Created probability graph:")
print("Inverted betweenness only")