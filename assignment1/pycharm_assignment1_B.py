import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os.path
import math

df = pd.read_excel('manufacturing_emails_temporal_network.xlsx')
number_of_nodes = 167
print(df)

try:
    infected_per_timestep = pickle.load(open("infected_per_timestamp.pickle", "rb"))
except Exception as e:
    print(e)
    print("Rebuilding data")

    infected_per_timestep = np.zeros([number_of_nodes, df['timestamp'][len(df) - 1]])

    for n in range(1, number_of_nodes + 1):
        infected = np.zeros(number_of_nodes + 1, dtype=bool)
        infected[n] = True
        infected_count = 1

        for index, transaction in df.iterrows():
            node1 = transaction['node1']
            node2 = transaction['node2']
            if infected[node1] and not infected[node2]:
                infected[node2] = True
                infected_count += 1

            infected_per_timestep[n - 1, transaction['timestamp'] - 1] = infected_count

        print("Infection of starting node " + str(n) + " finished")
    pickle.dump(infected_per_timestep, open("infected_per_timestamp.pickle", "wb"))

    print("Finished creating data")
print("infected_per_timestep initialized")
print(infected_per_timestep)

try:
    os.path.isfile('Infected_per_timestep.xlsx')
    print("Excelfile already there")
except Exception as e:
    print(e)
    print("Writing data to excel")
    df_infected_per_timestep = pd.DataFrame(infected_per_timestep.T)
    writer = pd.ExcelWriter('Infected_per_timestep.xlsx')
    df_infected_per_timestep.to_excel(writer, 'Sheet1', index=False)
    writer.save()
    print("Written infected per timestep to excel")

avg = [np.average(col) for col in infected_per_timestep.T]
std = [np.std(col) for col in infected_per_timestep.T]
print("Array length avg" + str(len(avg)) + ": " +str(avg[0:5]))
print("Array length std" + str(len(std)) + ": " +str(std[0:5]))

plt.figure()
plt.errorbar(np.arange(1,len(avg) + 1), avg, yerr=std, ecolor='grey')
plt.title("Average infected nodes over time")
plt.gca().set_xlim([0,57791])
plt.gca().set_ylim([0, 120])
plt.xlabel('Time')
plt.ylabel('Infected nodes')
plt.show()

threshold = math.ceil(0.8 * number_of_nodes)

threshold_reached = [np.min(np.where(row > threshold)[0])
         if np.where(row > threshold )[0].shape[0] > 0
         else len(infected_per_timestep.T)
         for row in infected_per_timestep]

print(threshold_reached[0:5])

node_timestamp_pair = np.stack(
    (np.arange(1,168),
    np.array(threshold_reached)), axis=-1  )
sorted_nodes = node_timestamp_pair[node_timestamp_pair[:,1].argsort()][:,0]


G = nx.from_pandas_edgelist(df, source='node1', target='node2')

degree_vector = np.array(G.degree())
sorted_degree_vector = degree_vector[degree_vector[:,1].argsort()][::-1][:,0]

cl_vector = np.array([[a, b] for (a,b) in nx.clustering(G).items()])
sorted_cl_vector = cl_vector[cl_vector[:,1].argsort()][::-1][:,0]

f_range = np.arange(0.05, 0.55, 0.05)
recognition_rate = np.zeros((2, len(f_range)))
for i in range(0, len(f_range)):
    f = f_range[i]
    selection_range = math.floor(f * number_of_nodes)

    d_intersection = [n for n
                      in sorted_nodes[0:selection_range]
                      if n in sorted_degree_vector[0:selection_range]]
    recognition_rate[0, i] = len(d_intersection) / selection_range

    c_intersection = [n for n
                      in sorted_nodes[0:selection_range]
                      if n in sorted_cl_vector[0:selection_range]]
    recognition_rate[1, i] = len(c_intersection) / selection_range
print(recognition_rate)
print("")
print(sorted_nodes[0:9])
print(sorted_degree_vector[0:9])
print(sorted_cl_vector[0:9])

plt.figure()
plt.plot(f_range, recognition_rate[0])
plt.plot(f_range, recognition_rate[1])
plt.title("Recognition rate of centrality metrics")
plt.gca().set_xlim([0.05,0.5])
plt.gca().set_ylim([0, 1])
plt.xlabel('Fraction of nodes in comparison set')
plt.ylabel('Recognition rate')
plt.legend(['Degree', 'Clustering Coefficient'])
plt.show()









