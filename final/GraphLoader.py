import json
from networkx.readwrite import json_graph


def load_graph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


def load_traffic_graph():
    filename = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/' \
               'traffic_graph_latest.json'
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


def load_page_graph():
    filename = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data' \
               '/hyperlink_graph_builder_output_graph.json'
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)
