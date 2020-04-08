import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas
import pprint

import GraphLoader

print("Imports loaded")


def plot_traffic_graph():
    G = GraphLoader.load_traffic_graph()

    print("Data loaded")

    fig, ax = plt.subplots(figsize=(500, 500))
    nx.draw(G, ax=ax)
    plt.show()

    print("Done with traffic")


def page():
    G = GraphLoader.load_page_graph()

    fig, ax = plt.subplots(1, 1, figsize=(30, 30));
    nx.draw(G, ax=ax)

    print("Done with pages")


def find_paths_to_component(source, component, full_graph):
    paths = [nx.shortest_path(full_graph, source=n1, target=n2)
             for n2 in component
             for n1 in source
             if n1 in full_graph
                and n2 in full_graph
                and nx.has_path(full_graph, source=n1, target=n2)]
    min_length = min([len(path) for path in paths]) if len(paths) > 0 else -1
    return paths, min_length


def find_closest_component(source, component_list, full_graph):
    paths_to_all_components = [find_paths_to_component(source,component, full_graph) for component in component_list]
    min_dist = min([l for (p, l) in paths_to_all_components if l > 0])
    print(min_dist)


    # return [path for (path, len) in paths_to_all_components if len < search_size]


def add_all_paths_to_graph(t_graph, full_graph):
    nodes = set([n for n in t_graph.nodes if n in full_graph])
    [nodes.update(nx.shortest_path(full_graph, source=n1, target=n2))
        for n1 in t_graph.nodes for n2 in t_graph.nodes
        if n1 != n2
            and n1 in full_graph
            and n2 in full_graph
            and nx.has_path(full_graph, n1, n2)]
    prev = 0
    while len(nodes) != prev and len(nodes) < 1000:
        prev = len(nodes)
        [nodes.update(full_graph.neighbors(n)) for n in nodes.copy()]

    return full_graph.subgraph(nodes)


search_size = 10

traffic_graph = GraphLoader.load_traffic_graph()

link_graph = GraphLoader.load_page_graph()
link_graph_undirected = link_graph.to_undirected()

updated_graph = nx.Graph()

# sorted_components = [c for c in sorted(nx.connected_components(traffic_graph), key=len, reverse=True)]
# first_component = sorted_components.pop(0)
#
# paths = find_closest_component(first_component, sorted_components, link_graph)
# pprint.pprint(paths)

newgraph = add_all_paths_to_graph(traffic_graph, link_graph)
print(len(newgraph.nodes))
print(len(newgraph.edges))
