import GraphLoader
import os
import glob
import sys

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

graphs = []
for file in glob.glob(dname + 'pgraph*.json'):
    graphs.append((file, GraphLoader.load_probability_graph(file)))

for file, G in graphs:
    missing_edges = [(u,v) for u,v,d in G.edges(data=True) if 'p' not in d]
    missing_nodes = [n for n, d in G.nodes(data=True) if 'p_exit' not in d['attr_data']]

    if len(missing_edges) > 0 or len(missing_nodes) > 0:
        print("Malformed graph:")
        print(file)
        print("Malformed nodes:")
        print(missing_nodes)
        print("Malformed edges:")
        print(missing_edges)

