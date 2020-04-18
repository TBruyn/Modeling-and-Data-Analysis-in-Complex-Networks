import json
import networkx as nx
from networkx.readwrite import json_graph
import time
import GraphLoader
import random
import numpy as np
import pprint

from pipeline.probability_graphs import CreateGraphPageviewsOnly, CreateGraphPageRankOnly, CreateGraphBetweennessOnly, \
    CreateGraphDegreeOnly, CreateGraphInvertedDegreeOnly


def add_betweenness(G):
    undirected = G.to_undirected()

    components = [undirected.subgraph(c) for c in nx.connected_components(undirected)]
    betweenness = {}
    [[betweenness.update({k: v}) for k, v in nx.betweenness_centrality(c).items()] for c in components]

    min_b = min([betweenness[n] for n, d in G.nodes(data=True) if betweenness[n] > 0])
    [betweenness.update({n: betweenness[n] + min_b}) for n, d in G.nodes(data=True)]

    [d['attr_data'].update({'betweenness': betweenness[n]}) for n, d in G.nodes(data=True)]


def add_degree(G):
    degrees = nx.degree((G))
    [d['attr_data'].update({'degree': degrees[n]}) for n, d in G.nodes(data=True)]


def add_inverted_degree(G):
    degrees = nx.degree((G))
    [d['attr_data'].update({'inv_degree': 1 / degrees[n]}) for n, d in G.nodes(data=True)]


def add_pagerank(G):
    pagerank = nx.pagerank(G)

    [d['attr_data'].update({'pagerank': pagerank[n]}) for n, d in G.nodes(data=True)]


def calculate_probabilities(attributelist):
    print()

G = GraphLoader.load_page_subgraph()
pageviewgraph = CreateGraphPageviewsOnly.create_graph()
pagerankgraph = CreateGraphPageRankOnly.create_graph()
betweennessgraph = CreateGraphBetweennessOnly.create_graph()
degreegraph = CreateGraphDegreeOnly.create_graph()
invdegreegraph = CreateGraphInvertedDegreeOnly.create_graph()
print(pageviewgraph.nodes(data=True))
print('bla')

# add_betweenness(G)
# add_degree(G)
# add_inverted_degree(G)
# add_pagerank(G)

