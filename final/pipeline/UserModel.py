import GraphLoader
import json
import networkx as nx
import numpy as np
import random
import pprint
import os
import time


def save_traffic_data(traffic_data, nametag=''):
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    print(dname)
    os.chdir(dname)

    timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')

    with open('generated_user_traffic/generated_traffic_' + nametag + '_' + timestamp + '.json', 'w', encoding='utf-8') as file:
        json.dump(traffic_data, file, indent=4)


class UserModel:

    def __init__(self, graph):
        self.graph = graph

    def random_walk_from_node(self, entry_point):
        def choose_next_point(current_point):
            p_exit = self.graph.nodes[current_point]['attr_data']['p_exit']

            edges = self.graph.edges(current_point, data=True)
            next_list = [v for u, v, d in edges if v != current_point]
            next_list.insert(0, 'exit')

            p_list = [d['p'] for u, v, d in edges if v != current_point]
            p_list.insert(0, p_exit)

            next_index = np.random.choice(list(range(0, len(p_list))), p=p_list)

            return next_list[next_index]

        # TODO implement more realistic probability function
        def p_next_step(steps):
            return 1

        virtual_user_traffic = {
            'pagelist': [self.graph.nodes[entry_point]['attr_data']],
            'page_views': 1
        }

        next_node = entry_point
        while np.random.random(1)[0] < p_next_step(virtual_user_traffic['page_views']):
            next_node = choose_next_point(next_node)
            if next_node == 'exit':
                return virtual_user_traffic
            else:
                virtual_user_traffic['pagelist'].append(self.graph.nodes[next_node]['attr_data'])
                virtual_user_traffic['page_views'] = len(virtual_user_traffic['pagelist'])

        return virtual_user_traffic

    def random_walk_from_node_list(self, nodelist):
        return [self.random_walk_from_node(node) for node in nodelist]

    def random_walk_n_nodes(self, n):
        nlist = random.choices(list(self.graph.nodes), k=n)
        return self.random_walk_from_node_list(nlist)


def test():
    G = GraphLoader.load_graph('pipeline/probability_graphs/pgraph_random_graph_Wed_Apr_15_17:28:26_2020.json')

    model = UserModel(G)
    walk = model.random_walk_from_node('https://www.tudelft.nl/')

    deg = list(G.degree())
    deg.sort(key=lambda x: x[1], reverse=True)
    nlist = [node for (node, degree) in deg[0:10]]

    walklist = model.random_walk_from_node_list(nlist)

    bla = model.random_walk_n_nodes(10)


