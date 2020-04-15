import GraphLoader
import json
import networkx as nx
import numpy as np
import pprint


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

        pagelist = [self.graph.nodes[entry_point]['attr_data']]
        pages_visited = 1

        current = entry_point
        while np.random.random(1)[0] < p_next_step(pages_visited):
            current = choose_next_point(current)
            if current == 'exit':
                return pagelist
            else:
                pagelist.append(self.graph.nodes[current]['attr_data'])
                pages_visited += 1

        return pagelist


def test():
    G = GraphLoader.load_graph('pipeline/probability_graphs/pgraph_random_graph_Wed_Apr_15_17:28:26_2020.json')

    model = UserModel(G)
    walk = model.random_walk_from_node('https://www.tudelft.nl/')

    list = [p['url'] for p in walk]

    pprint.pprint(list)


test()
