import json
import networkx as nx
import numpy as np
import random
import pprint
import os
import time
import GraphLoader
import matplotlib.pyplot as plt
import UserModel


G = GraphLoader.load_graph('pgraph_random.json') #Graph
model = UserModel.UserModel(G)
my_list = list(G.nodes())
walkList = model.random_walk_n_nodes(len(my_list))

for n in walkList:
    sum = 0
    for l in n['pagelist']:
        sum = sum + l['visits']
    print(sum)
