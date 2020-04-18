import json
import networkx as nx
from networkx.readwrite import json_graph
import time
import GraphLoader
import random
import numpy as np
import pprint

from pipeline.probability_graphs import CreateGraphPageviewsOnly, CreateGraphPageRankOnly, CreateGraphBetweennessOnly, \
    CreateGraphDegreeOnly, CreateGraphInvertedDegreeOnly, CreateGraphInvertedBetweennessOnly



def add_attribute(graph, attribute_graph, attribute_name):
    if set(graph.nodes) != set(attribute_graph.nodes) or set(graph.edges) != set(attribute_graph.edges):
        raise ValueError('Node sets different when adding: ' + attribute_name)

    [d['attr_data'].update(
        {'p_exit_' + attribute_name: attribute_graph.nodes[n]['attr_data']['p_exit'],
         attribute_name: attribute_graph.nodes[n]['attr_data'][attribute_name]
                            }) for n, d in graph.nodes(data=True)]
    [d.update({'p_'+ attribute_name : attribute_graph.edges[(u,v)]['p']}) for u,v,d in graph.edges(data=True)]
    return graph


G = GraphLoader.load_page_subgraph()

pageview_graph = CreateGraphPageviewsOnly.create_graph()
pagerank_graph = CreateGraphPageRankOnly.create_graph()
betweenness_graph = CreateGraphBetweennessOnly.create_graph()
# inverted_betweenness_graph = CreateGraphInvertedBetweennessOnly.create_graph()
degree_graph = CreateGraphDegreeOnly.create_graph()
inverted_degree_graph = CreateGraphInvertedDegreeOnly.create_graph()

add_attribute(G, pageview_graph, 'page_views')
add_attribute(G, pagerank_graph, 'pagerank')
add_attribute(G, betweenness_graph, 'betweenness')
# add_attribute(G, inverted_betweenness_graph, 'inverted_betweenness')
add_attribute(G, degree_graph, 'degree')
add_attribute(G, inverted_degree_graph, 'inv_degree')

GraphLoader.save_probability_graph(G, 'all_attributes', add_timestamp=False)

pprint.pprint(list(G.nodes(data=True))[5])
pprint.pprint(list(G.edges(data=True))[5])


# add_betweenness(G)
# add_degree(G)
# add_inverted_degree(G)
# add_pagerank(G)

