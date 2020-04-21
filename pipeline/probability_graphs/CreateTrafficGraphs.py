import pprint

import GraphLoader
from crawlers_and_creators import TrafficGraphMediator
from pipeline.UserModel import UserModel


probability_graph_filenames = {
    'betweenness_only':"pgraph_betweenness_only_Sat_Apr_18_20:41:20_2020.json",
    'degree_only':"pgraph_degree_only_Sat_Apr_18_16:43:36_2020.json",
    'inverted_betweenness_only':"pgraph_inverted_betweenness_only_Sat_Apr_18_23:01:02_2020.json",
    'inverted_degree_only':"pgraph_inverted_degree_only_Sat_Apr_18_17:06:15_2020.json",
    'pagerank_only':"pgraph_pagerank_only_Sat_Apr_18_11:40:38_2020.json",
    'pageviews_only':"pgraph_pageviews_only_Fri_Apr_17_16:51:30_2020.json",
    'random':"pgraph_random_graph_Wed_Apr_15_17:28:26_2020.json",
    'all_attributes_evenly' : 'pgraph_all_attributes_latest.json'
}



pgraphs = [(metric, GraphLoader.load_probability_graph(filename)) for metric, filename in probability_graph_filenames.items()]



traffic_files = []
for name, G in pgraphs:
    model = UserModel(G)
    traffic_1_entrypoints = model.random_walk_from_node_list()
    traffic_2_entrypoints = model.random_walk_from_node_list()
    traffic_2_entrypoints.extend(traffic_1_entrypoints)
    traffic_random = model.random_walk_n_nodes()


    tag1 = name + '_entrypoints_' + str(len(traffic_1_entrypoints))
    tag2 = name + '_entrypoints_' + str(len(traffic_2_entrypoints))
    tag_random = name + '_random_entry_' + str(len(traffic_random))

    model.save_traffic_data(traffic_1_entrypoints, tag1)
    model.save_traffic_data(traffic_2_entrypoints, tag2)
    model.save_traffic_data(traffic_random, tag_random)

    print("Created traffic:")
    print(tag1)
    print(tag2)
    print(tag_random)

    traffic_files.extend([tag1, tag2, tag_random])

for tag in traffic_files:

    inputfile = 'generated_user_traffic/generated_traffic_' + tag + '.json'
    outputfile = 'traffic_graphs/traffic_graph_' + tag + '.json'

    TrafficGraphMediator.create_graph(
        outputfile=outputfile,
        inputfile=inputfile
    )

    print("Created traffic graph " + tag)