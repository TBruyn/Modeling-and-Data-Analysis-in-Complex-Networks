import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collections
import netcomp as nc
import numpy as np
import netlsd 



"""""
Use these function to create a dataframe with the networking metrics 

"""""

def calculate_metrics_df(graph):

    df = pd.DataFrame()
    link_density = nx.density(graph)
    info = nx.info(graph)
    av = nx.average_clustering(graph)


    deg = graph.degree()
    deg_c = nx.degree_centrality(graph)
    between_c = nx.betweenness_centrality(graph, normalized=True, endpoints=False)
    pr = nx.pagerank(graph, alpha=0.8)
    close_centrality = nx.closeness_centrality(graph)


    df['Nodes'] = dict(deg).keys()
    df['Degree'] = dict(deg).values()
    df['Degree Centrality'] = deg_c.values()
    df['Betweeness Centrality'] = between_c.values()
    df['PageRank'] = pr.values()
    df['Closeness Centrality'] = close_centrality.values()


    print(info)
    print('The density of the graph is :{}'.format(link_density))
    print('The average clustering coefficient of the graph'.format(av))

    return df



"""""

Use this function to visualize the graph where the nodes size is 
based on the node betweeness value.

"""""
def plot_graph(graph):

    pos = nx.spring_layout(graph)
    betCent = nx.betweenness_centrality(graph, normalized=True, endpoints=True)
    node_color = [20000.0 * graph.degree(v) for v in graph ]
    node_size = [v * 10000 for v in betCent.values()]
    plt.figure(figsize=(20, 20))
    nx.draw_networkx(graph, pos=pos, with_labels=False,
                     node_color=node_color,
                     node_size=node_size)
    plt.axis('off')


def plot_distributions(data):

    plt.figure(figsize=(10, 5))
    sns.kdeplot(data["Closeness Centrality"], color="skyblue")
    sns.kdeplot(data["Degree Centrality"], color="olive")
    sns.kdeplot(data["Betweeness Centrality"], color="gold")
    sns.kdeplot(data["Eigenvector Centrality"], color="teal")
    plt.show()


def plot_degree_distribution(dd):
    degree_sequence = sorted(dd, reverse=True)
    degree_count = collections.Counter(degree_sequence)
    degree, count = zip(*degree_count.items())
    prob = [x / sum(count) for x in count]

    for i in range(139):
        if i not in degree:
            degree = list(degree)
            degree.append(i)
            prob = list(prob)
            prob.append(0)
            degree = tuple(degree)
            prob = tuple(prob)
    indexes = np.argsort(degree)
    sortedDegree = sorted(degree)
    sortedProb = []

    for index in indexes:
        sortedProb.append(prob[index])

    plt.plot(sortedDegree, sortedProb, 'b')
    plt.title("Degree Distribution")
    plt.ylabel("Pr[D = k]")
    plt.xlabel("Degree")
    plt.xlim(0, 75)
    plt.show()
    
def Comparison_metrics(G1, G2):
    
    A1 = nx.adjacency_matrix(G1)
    A2 = nx.adjacency_matrix(G2)
    
    a = nc.deltacon0(A1,A2)
    b = nc.lambda_dist(A1,A2)
    c = nc.lambda_dist(A1,A2,kind='laplacian_norm')
    
    av_cl1 = nx.average_clustering(G1)
    av_cl2 = nx.average_clustering(G1)
    
    desc0 = netlsd.heat(G1)
    desc1 = netlsd.heat(G2)
    net__lsd = netlsd.compare(desc0, desc1)
    
    print('The Average Glustering coeficient of G1:{}'.format(av_cl1))
    print('The Average Glustering coeficient of G2:{}'.format(av_cl2))
    
    print('The DeltaCon of G1 and G2:{}'.format(a))
    print('The differnce of the adjcency matrices of G1 and G2'.format(b))
    print('The differnce of the laplacian matrices of G1 and G2:{}'.format(c))
    print('The Netlsd of G1 and G2:{}'.format(net__lsd))

    
def plot_comp(d1,d2):
    f, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.kdeplot(d1['Degree Centrality'],color='b', ax=axes[0, 0])
    sns.kdeplot(d2['Degree Centrality'], color= 'r', ax=axes[0, 0])


    sns.kdeplot(d1["Betweeness Centrality"],color="b", ax=axes[0, 1])
    sns.kdeplot(d2["Betweeness Centrality"], color="r", ax=axes[0, 1]')
    plt.show()