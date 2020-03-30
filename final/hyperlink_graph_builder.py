import os

import requests
from requests.auth import HTTPBasicAuth

import networkx as nx
from networkx.readwrite import json_graph

import json
import re
import pprint

from tqdm import tqdm


# Global variables
G = nx.DiGraph()
pagedict = {}

pages_with_connection_error = {}


def init():
    pages = json.loads(open('pages.json','r').read())

    [pagedict.update({current_url['url']: current_url}) for current_url in pages]

    [G.add_node(key, attr_data=val) for key, val in pagedict.items()]


def find_urls_on_webpage(webpage):
    try:
        website = requests.get(webpage, headers={'Accept-Encoding': 'identity'})
        
    except Exception as e:
        print(str(e))
        pages_with_connection_error[webpage] = str(e)
        return []
    
    links = re.findall('"((http|ftp)s?://.*?)"', website.text)
    return [current_url for current_url, _ in links if current_url in pagedict]

    

            

def crawl_website():

    iterations = 0
    this_url = ""
    try:
        for current_url in tqdm(pagedict):
            this_url = current_url

            url_list = find_urls_on_webpage(current_url)

            [G.add_edge(current_url, new_url) for new_url in url_list]
            
            iterations += 1

    except Exception as e:
        error_message = str(e) + "\nIterations:" + str(iterations) + "\nCurrent page"+ str(this_url)
        with open('hyperlink_graph_builder_error_log.json', 'w', encoding='utf-8') as file:
            json.dump(error_message, file, indent=4)
        with open('hyperlink_graph_builder_error_pages.json', 'w', encoding='utf-8') as file:
            json.dump(pages_with_connection_error, file, indent=4)
        with open('hyperlink_graph_builder_error_output_graph.json', 'w', encoding='utf-8') as file:
            json.dump(json_graph.node_link_data(G), file, indent=4)
        
        print("Error occured:\n" + str(e))

init()

crawl_website()

# print("urls visited")
# print(urls_visited)
# print("Number of nodes")
# print(len(G.nodes))
# print("Number of edges")
# print(len(G.edges))

with open('hyperlink_graph_builder_output_graph.json', 'w', encoding='utf-8') as file:
    json.dump(json_graph.node_link_data(G), file, indent=4)
with open('hyperlink_graph_builder_faulty_pages.json', 'w', encoding='utf-8') as file:
            json.dump(pages_with_connection_error, file, indent=4)