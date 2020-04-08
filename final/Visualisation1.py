import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas

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


def find_closest_cluster(source, component_list, full_graph):
    min_d = 100000
    shortest_path = []
    for node1 in source:
        for node2 in component_list[0]:
            if node1 not in full_graph \
                    or node2 not in full_graph \
                    or not nx.has_path(full_graph, source=node1, target=node2): continue
            path = nx.shortest_path(full_graph, source=node1, target=node2)
            d = len(path)
            if d < min_d:
                min_d = d
                shortest_path = path
    return shortest_path

traffic_graph = GraphLoader.load_traffic_graph()

link_graph = GraphLoader.load_page_graph()

sorted_components = [c for c in sorted(nx.connected_components(traffic_graph), key=len, reverse=True)]
first_component = sorted_components.pop(0)
print(first_component)

d = find_closest_cluster(first_component, sorted_components, link_graph)
print(d)
