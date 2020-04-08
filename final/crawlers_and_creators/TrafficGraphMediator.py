import json
import networkx as nx
import time
from networkx.readwrite import json_graph
from tqdm import tqdm


def create_graph(
        outputfile='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/traffic_graph_latest.json',
        inputfile='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/merged_traffic_array_latest.json'):

    def add_node_to_graph(page):
        if 'url' in page and not G.has_node(page['url']):
            G.add_node(page['url'], attr_dict=page)

    def add_edge_to_graph(page1, page2):
        add_node_to_graph(page1)
        add_node_to_graph(page2)

        url1 = page1['url']
        url2 = page2['url']
        if not G.has_edge(url1, url2):
            G.add_edge(url1, url2, visited_together=1)
        else:
            G[url1][url2]['visited_together'] += 1

    def add_list_to_graph(pagelist):
        pages_to_add = pagelist.copy()
        while pages_to_add:
            current = pages_to_add.pop()
            for page in pages_to_add:
                add_edge_to_graph(current, page)

    def normalize_edges():
        max_count = max([d['visited_together'] for u, v, d in G.edges(data=True)])
        [G.add_edge(u, v, weight=d['visited_together'] / max_count) for u, v, d in G.edges(data=True)]

    path = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/'
    timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')

    traffic = json.loads(open(inputfile, 'r').read())

    G = nx.Graph()

    pages_to_add = []
    for visitor in tqdm(traffic):
        if 'pagelist' in visitor and len(visitor['pagelist']) > 1:
            add_list_to_graph(visitor['pagelist'])

    normalize_edges()

    with open(path + 'traffic_graph_' + timestamp + '.json', 'w', encoding='utf-8') as file:
        json.dump(json_graph.node_link_data(G), file, indent=4)
    with open(outputfile, 'w', encoding='utf-8') as file:
        json.dump(json_graph.node_link_data(G), file, indent=4)

    print("Created graph from traffic data")
    print("Output file")
    print(path + 'traffic_graph_' + timestamp + '.json')
    print(path + 'traffic_graph_latest.json')


def load_graph(filename='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/traffic_graph_latest.json'):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)