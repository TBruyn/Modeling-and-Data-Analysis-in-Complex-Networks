import json
import tqdm

from pipeline.UserModel import UserModel
import GraphLoader

number_visits = 1000


def influence_ranking(graph, user_model):
    influence_metrics = {}

    for node in tqdm.tqdm(graph.nodes):
        total_extra_views = 0
        average_distance = 0
        max_distance = 0
        for i in range(number_visits):
            traffic = model.random_walk_from_node(node)
            total_extra_views += traffic['page_views']
            average_distance += len(traffic['pagelist']) / number_visits
            if len(traffic['pagelist']) > max_distance:
                max_distance = len(traffic['pagelist'])
        influence_metrics[node] = {}
        influence_metrics[node]['Total extra views'] = total_extra_views
        influence_metrics[node]['Average distance'] = average_distance
        influence_metrics[node]['Max distance'] = max_distance
    return influence_metrics


G = GraphLoader.load_probability_graph('pgraph_inverted_degree_only_Sat_Apr_18_17:06:15_2020.json')

model = UserModel(G)

influence = influence_ranking(G, model)

with open('pipeline/infect/Influence_metrics.json', 'w', encoding='utf-8') as file:
    json.dump(influence, file, indent=4)
