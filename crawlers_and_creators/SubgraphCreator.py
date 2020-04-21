import json
import networkx as nx
from networkx.readwrite import json_graph
import time
import GraphLoader
import matplotlib.pyplot as plt
import numpy as np

path = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/'
timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')

traffic_graph = GraphLoader.load_traffic_graph()

link_graph = GraphLoader.load_page_graph()

nodes = set([n for n in traffic_graph.nodes if n in link_graph])
[nodes.update(nx.shortest_path(link_graph, source=n1, target=n2))
 for n1 in traffic_graph.nodes for n2 in traffic_graph.nodes
 if n1 != n2
 and n1 in link_graph
 and n2 in link_graph
 and nx.has_path(link_graph, n1, n2)]
prev = 0
while len(nodes) != prev and len(nodes) < 1000:
    prev = len(nodes)
    [nodes.update(link_graph.neighbors(n)) for n in nodes.copy()]

subgraph = nx.DiGraph(link_graph.subgraph(nodes))

self_edges = [(u, v) for (u, v) in subgraph.edges if u == v]
subgraph.remove_edges_from(self_edges)

singular_nodes = [n for n, d in subgraph.degree() if d == 0]
subgraph.remove_nodes_from(singular_nodes)

with open(path + 'subgraph_' + timestamp + '.json', 'w', encoding='utf-8') as file:
    json.dump(json_graph.node_link_data(subgraph), file, indent=4)
with open(path + 'subgraph_latest.json', 'w', encoding='utf-8') as file:
    json.dump(json_graph.node_link_data(subgraph), file, indent=4)

print('----------------------------------------------------------------------------------------')
print('Created subgraph')
print('Nodes:\t' + str(len(subgraph.nodes)))
print('Edges:\t' + str(len(subgraph.edges)))
print('----------------------------------------------------------------------------------------')

fig, ax = plt.subplots(1, 1, figsize=(50, 50));
nx.draw(subgraph, ax=ax)
plt.savefig('/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final//figures/subgraph_latest.svg',
            format='svg')
plt.savefig(
    '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final//figures/subgraph_' + timestamp + '.svg',
    format='svg')
print("Plotted subgraph in figures/subgraph_latest.svg")
