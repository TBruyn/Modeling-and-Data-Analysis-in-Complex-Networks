import json
import networkx as nx
import numpy as np
import random
import pprint
import os
import time
import GraphLoader
import matplotlib.pyplot as plt


G = GraphLoader.load_graph('pgraph_random.json') #Graph
N = 1000 #Number of agents
k = 10 #Number of iterations

for n in G.nodes:
    if G.nodes[n]['attr_data']['p_exit'] < 1:
        print(G.nodes[n]['attr_data']['p_exit'])
