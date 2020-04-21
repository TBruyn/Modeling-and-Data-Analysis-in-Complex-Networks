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

The betweenness is on the undirected graph and is calculated per component

P[u -> v] = (betweenness of v) / (sum of betweenness of all neighbours of u + betweenness u)
P[exit] = (betweenness of u) / (sum of betweenness of all neighbours of u + betweenness u)

"""

tag = 'betweenness_only'


def create_graph():
    G = GraphLoader.load_page_subgraph()
    undirected = G.to_undirected()

    components = [undirected.subgraph(c) for c in nx.connected_components(undirected)]
    betweenness = {}
    [[betweenness.update({k: v}) for k, v in nx.betweenness_centrality(c).items()] for c in components]

    min_b = min([betweenness[n] for n, d in G.nodes(data=True) if betweenness[n] > 0])
    [betweenness.update({n: betweenness[n] + min_b}) for n, d in G.nodes(data=True)]

    [d['attr_data'].update({'betweenness': betweenness[n]}) for n, d in G.nodes(data=True)]

    for current in G.nodes:
        edges = G.edges(current, data=True)
        edges = [(u, v, d) for (u, v, d) in edges if u != v]
        views = {current: G.nodes[current]['attr_data']['betweenness']}
        total = G.nodes[current]['attr_data']['betweenness'] + \
                sum([G.nodes[neighbour]['attr_data']['betweenness'] for (_, neighbour, _) in edges])
        [attributes.update({'p': G.nodes[neighbour]['attr_data']['betweenness'] / total})
         for (_, neighbour, attributes) in edges]
        G.nodes[current]['attr_data']['p_exit'] = G.nodes[current]['attr_data']['betweenness'] / total

    return G


def main():
    G = create_graph()

    GraphLoader.save_probability_graph(G, tag)
    print("Created probability graph:")
    print("Betweenness only")


if __name__ == "__main__":
    main()
