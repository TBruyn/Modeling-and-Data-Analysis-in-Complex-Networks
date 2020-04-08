import requests
from requests.auth import HTTPBasicAuth

from tqdm import tqdm
import json
import time

from Site_Improve_Page_Looper import Site_Improve_Page_Looper

path = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/'

site_id = "1348629560"
url_sites = "https://api.siteimprove.com/v2/sites/"
command = url_sites + site_id + "/analytics/overview/online_visitors"
credentials = json.loads(open(path + 'secret.json', 'r').read())
timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')

looper = Site_Improve_Page_Looper()
pagelist_raw = looper.collect_pages(command=command,
                                    output_file=path + 'additional_output/traffic_pages_' + timestamp + '.json',
                                    error_output_file=path + 'additional_output/traffic_pages_error_' + timestamp + '.json',
                                    error_log_file=path + 'logs/traffic_pages_error_' + timestamp + '.json',
                                    should_return=True)

pagelist = []
[[pagelist.append(item) for item in page['items']] for page in pagelist_raw]

visitor_data = {}

for item in tqdm(pagelist):
    visitor_data[item['id']] = item

    if '_links' in item and 'pages' in item['_links'] and 'href' in item['_links']['pages']:
        pages_url = item['_links']['pages']['href']
        try:
            pages_for_visitor = requests.get(pages_url, auth=HTTPBasicAuth(credentials['userName'],credentials['userPass'])).json()

            visitor_data[item['id']]['pagelist'] = pages_for_visitor['items']

            while 'links' in pages_for_visitor and 'next' in pages_for_visitor['links'] and 'href' in pages_for_visitor['links']['next']:
                pages_for_visitor = requests.get(pages_for_visitor['links']['next']['href']).json()
                [visitor_data[item['id']]['pagelist'].append(page) for page in pages_for_visitor['items']]

        except Exception as e:
            with open(path + 'additional_output/traffic_collector_error_output_' + timestamp + '.json', 'w', encoding='utf-8') as file:
                    json.dump(visitor_data, file, indent=4)
            with open(path + 'additional_output/traffic_collector_error_log_' + timestamp + '.txt', 'w', encoding='utf-8') as file:
                    file.write(str(e))

with open(path + 'data/traffic_pages_' + timestamp + '.json', 'w', encoding='utf-8') as file:
    json.dump(visitor_data, file, indent=4)