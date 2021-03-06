import GraphLoader
import json
import networkx as nx
import numpy as np
import random
import pprint
import os
import time

current_number_of_visitors = 991
entry_pages = json.loads(open('pipeline/entry_pages.json', 'r').read())





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

    def random_walk_from_node_list(self, nodelist=entry_pages):
        return [self.random_walk_from_node(node) for node in nodelist if node in self.graph.nodes]

    def random_walk_n_nodes(self, n=current_number_of_visitors):
        nlist = random.choices(list(self.graph.nodes), k=n)
        return self.random_walk_from_node_list(nlist)

    def save_traffic_data(self, traffic_data, nametag=""):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        print(dname)
        os.chdir(dname)

        timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')

        with open('generated_user_traffic/generated_traffic_' + nametag + '.json', 'w', encoding='utf-8') as file:
            json.dump(traffic_data, file, indent=4)

def test():
    pages = json.loads(
        open(
            '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/merged_traffic_array_latest.json',
            'r').read())

    visits = [[(visit['url'], visit['last_page_view']) for visit in p['pagelist']] for p in pages if 'pagelist' in p]
    entry_pages_with_timestamp = [sorted(visit, key=lambda x: x[1])[0] for visit in visits if len(visit) > 0]
    entry_pages = [p for p, t in entry_pages_with_timestamp]

    with open('pipeline/entry_pages.json', 'w', encoding='utf-8') as file:
        json.dump(entry_pages, file, indent=4)


test()
