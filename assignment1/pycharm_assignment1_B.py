import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os.path
import math


def create_temporal_graph_data(df, verbose=False):
    print("Creating temporal graph data")

    if verbose: print(df)

    infected_per_timestamp = np.zeros([number_of_nodes, df['timestamp'][len(df) - 1]])
    time_to_infection = np.full([number_of_nodes + 1, number_of_nodes + 1], -1)

    for n in range(1, number_of_nodes + 1):
        infected = np.zeros(number_of_nodes + 1, dtype=bool)
        infected[n] = True
        infected_count = 1

        time_to_infection[n, n] = 0

        for index, transaction in df.iterrows():
            node1 = transaction['node1']
            node2 = transaction['node2']
            if infected[node1] and not infected[node2]:
                infected[node2] = True
                infected_count += 1
                if infected_count / number_of_nodes <= 0.8:
                    time_to_infection[n, node2] = transaction['timestamp']

            infected_per_timestamp[n - 1, transaction['timestamp'] - 1] = infected_count

        print("Data created for starting node " + str(n))

    print("Finished creating data")

    return infected_per_timestamp, time_to_infection


def calculate_average_and_standard_deviation(infected_per_timestamp):
    avg = [np.average(col) for col in infected_per_timestamp.T]
    std = [np.std(col) for col in infected_per_timestamp.T]
    return avg, std


def plot_average_and_standard_deviation(average, standard_dev, wait_with_plotting=False):
    plt.figure()
    plt.errorbar(np.arange(1, len(average) + 1), average, yerr=standard_dev, ecolor='grey')
    plt.title("Average infected nodes over time")
    plt.gca().set_xlim([0, 57791])
    plt.gca().set_ylim([0, 120])
    plt.xlabel('Time')
    plt.ylabel('Infected nodes')
    if wait_with_plotting:
        plt.draw()
    else:
        plt.show()


def create_node_vector_sorted_on_time_to_reach_threshold(infected_per_timestamp):
    threshold = math.ceil(0.8 * number_of_nodes)

    threshold_reached = [np.min(np.where(row > threshold)[0])
                         if np.where(row > threshold)[0].shape[0] > 0
                         else len(infected_per_timestamp.T)
                         for row in infected_per_timestamp]

    node_timestamp_pair = np.stack(
        (np.arange(1, number_of_nodes + 1),
         np.array(threshold_reached)), axis=-1)
    return node_timestamp_pair[node_timestamp_pair[:, 1].argsort()][:, 0]


def create_node_vector_sorted_on_degree(graph):
    degree_vector = np.array(graph.degree())
    return degree_vector[degree_vector[:, 1].argsort()][::-1][:, 0]


def create_node_vector_sorted_on_clustering(graph):
    cl_vector = np.array([[a, b] for (a, b) in nx.clustering(graph).items()])
    return cl_vector[cl_vector[:, 1].argsort()][::-1][:, 0]


def calculate_recognition_rate(f_range, sorted_vector_1, sorted_vector_2):
    recognition_rate_vector = np.zeros(len(f_range))
    for i in range(0, len(f_range)):
        f = f_range[i]
        selection_range = math.floor(f * number_of_nodes)

        d_intersection = [n for n
                          in sorted_vector_1[0:selection_range]
                          if n in sorted_vector_2[0:selection_range]]
        recognition_rate_vector[i] = len(d_intersection) / selection_range

    return recognition_rate_vector


def plot_recognition_rate_metrics(f_range, recognition_rates, legend, wait_with_plotting=False):
    plt.figure()

    for recognition_rate in recognition_rates:
        print(recognition_rate)
        plt.plot(f_range, recognition_rate)

    plt.title("Recognition rate of centrality metrics")
    plt.gca().set_xlim([0.05, 0.5])
    plt.gca().set_ylim([0, 1])
    plt.xlabel('Fraction of nodes in comparison set')
    plt.ylabel('Recognition rate')
    plt.legend(legend)
    if wait_with_plotting:
        plt.draw()
    else:
        plt.show()


# Initialization
df = pd.read_excel('manufacturing_emails_temporal_network.xlsx')
number_of_nodes = 167

try:
    time_to_infection = np.loadtxt(open('time-to-infection.csv', "rb"), delimiter=",")
    infected_per_timestamp = np.loadtxt(open('infected-per-timestep-Gdata.csv', "rb"), delimiter=",")
except Exception as e:
    print(e)
    time_to_infection, infected_per_timestamp = create_temporal_graph_data(df)
    np.savetxt('time_to_infection.csv', time_to_infection, delimiter=',')
    np.savetxt('infected_per_timestep-Gdata.csv', infected_per_timestamp, delimiter=',')

# Q10
avg, std = calculate_average_and_standard_deviation(infected_per_timestamp)
plot_average_and_standard_deviation(avg, std, wait_with_plotting=True)

# Q11
sorted_infection_vector = create_node_vector_sorted_on_time_to_reach_threshold(infected_per_timestamp)
G = nx.from_pandas_edgelist(df, source='node1', target='node2')
sorted_degree_vector = create_node_vector_sorted_on_degree(G)
sorted_clustering_vector = create_node_vector_sorted_on_clustering(G)

f_range = np.arange(0.05, 0.55, 0.05)
recognition_rate_infection_degree = calculate_recognition_rate(f_range, sorted_infection_vector, sorted_degree_vector)
recognition_rate_infection_clustering = calculate_recognition_rate(f_range, sorted_infection_vector,
                                                                   sorted_clustering_vector)

plot_recognition_rate_metrics(f_range,
                              [recognition_rate_infection_degree, recognition_rate_infection_clustering],
                              ["Degree", "Clustering Coefficient"],
                              wait_with_plotting=True
                              )

# If you wait with plotting until the end, you need to call
plt.show()