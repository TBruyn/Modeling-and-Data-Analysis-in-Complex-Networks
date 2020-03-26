import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

import json

url = 'https://api.siteimprove.com/v2'
site_id = '1348629560'
command = "/sites/" + site_id + "/analytics/content/all_pages"
credentials = json.loads(open('secret.json', 'r').read())

initial_request = requests.get(url + command, auth=HTTPBasicAuth(credentials['userName'], credentials['userPass']))


start_page_list = initial_request.json()
page_lists = [start_page_list]

next_page_address = start_page_list['links']['next']['href']
for i in tqdm(range(start_page_list['total_pages'])):
    try:
        new_request = requests.get(next_page_address, auth=HTTPBasicAuth(credentials['userName'], credentials['userPass']))
        new_page_list = new_request.json()
        page_lists.append(new_page_list)
        if i < start_page_list['total_pages'] - 1: next_page_address = new_page_list['links']['next']['href']
    except Exception as e:
        log = "Exception:\n" + str(e) + "\npage:\n" + str(i) + "\npagelink\n" + str(next_page_address)

        with open('error_output_list.json', 'w', encoding='utf-8') as file:
            json.dump(page_lists, file, indent=4)
        with open('error_log.txt', 'w', encoding='utf-8') as file:
            file.write(log)

with open('pagelists.json', 'w', encoding='utf-8') as file:
    json.dump(page_lists, file, indent=4)


# pages = [p for p in start_page_list['items']]