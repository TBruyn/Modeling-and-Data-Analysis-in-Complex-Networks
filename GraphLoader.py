import glob
import json
import os
import pprint
import time
from networkx.readwrite import json_graph

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

subgraph_filename = 'data/' \
                    'subgraph_latest.json'
traffic_graph_filename = 'data/' \
                         'traffic_graph_latest.json'
pages_graph_filename = 'data' \
                       '/hyperlink_graph_builder_output_graph.json'


def filenames():
    return [subgraph_filename, traffic_graph_filename, pages_graph_filename]


def load_graph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
        return json_graph.node_link_graph(js_graph)


def load_page_subgraph():
    return load_graph(subgraph_filename)


def load_traffic_graph():
    return load_graph(traffic_graph_filename)


def load_page_graph():
    return load_graph(pages_graph_filename)


def load_probability_graph(filename):
    return load_graph('pipeline/probability_graphs/' + filename)


def save_probability_graph(graph, filename, add_path=True, add_timestamp=False):
    if add_path:
        timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')
        filename = dname + '/pipeline/probability_graphs/pgraph_' \
                   + filename.replace('.json', '') + '_'
        if add_timestamp:
            filename += timestamp
        else:
            filename += 'latest'
        filename += '.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(json_graph.node_link_data(graph), file, indent=4)


def load_generated_traffic_graph(filename):
    return load_graph('pipeline/traffic_graphs/' + filename)


def load_all_generated_traffic_graphs():
    traffic_graphs = []
    for file in glob.glob('pipeline/traffic_graphs/*.json'):
        try:
            traffic_graphs.append(load_graph(file))
        except Exception as e:
            print('Something went wrong with file:')
            print(file)
            print(str(e))
    return traffic_graphs


def main():
    pprint.pprint(load_page_subgraph())


if __name__ == '__main__':
    main()
