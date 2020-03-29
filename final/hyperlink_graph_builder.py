import os

import requests
from requests.auth import HTTPBasicAuth

import networkx as nx
from networkx.readwrite import json_graph

import json
import re
import pprint


# Global variables
G = nx.DiGraph()
pagedict = {}
urls_to_visit = []
urls_visited = []

def init():
    pages = json.loads(open('pages.json','r').read())
    [pagedict.update({current_url['url']: current_url}) for current_url in pages]


def find_urls_on_webpage(webpage):
    website = requests.get(webpage, headers={'Accept-Encoding': 'identity'})
    links = re.findall('"((http|ftp)s?://.*?)"', website.text)
    return [current_url for current_url, _ in links]


def add_url_list_to_graph(page_url, url_list):
    if not page_url in G and page_url in pagedict:
        G.add_node(page_url, attr_dict=pagedict[page_url])
    for url in url_list:
        if url in pagedict:
            G.add_node(url, attr_dict=pagedict[url])
            G.add_edge(page_url, url)
            

def crawl_website(start_url):
    urls_to_visit.append(start_url)

    try:
        while urls_to_visit:
            current_url = urls_to_visit.pop()
            urls_visited.append(current_url)

            urls_on_webpage = find_urls_on_webpage(current_url)
            add_url_list_to_graph(current_url, urls_on_webpage)

            [urls_to_visit.append(url) for url in urls_on_webpage if url in pagedict and not url in urls_visited]

    except Exception as e:
        error_lists = { 'urls_to_visit' : urls_to_visit,
                        'urls_visited' : urls_visited       }
        with open('hyperlink_graph_builder_error_log.json', 'w', encoding='utf-8') as file:
            json.dump(str(e), file, indent=4)
        with open('hyperlink_graph_builder_error_lists.json', 'w', encoding='utf-8') as file:
            json.dump(error_lists, file, indent=4)
        with open('hyperlink_graph_builder_error_output_graph.json', 'w', encoding='utf-8') as file:
            json.dump(json_graph.node_link_data(G), file, indent=4)
        


        print("Catch")

init()


start_url = "https://www.tudelft.nl/"

crawl_website(start_url)

print("urls visited")
print(urls_visited)
print("Number of nodes")
print(len(G.nodes))
print("Number of edges")
print(len(G.edges))

with open('hyperlink_graph_builder_output_graph.json', 'w', encoding='utf-8') as file:
    json.dump(json_graph.node_link_data(G), file, indent=4)