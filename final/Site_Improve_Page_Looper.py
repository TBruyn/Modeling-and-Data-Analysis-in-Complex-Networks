import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
import json
import time


class Site_Improve_Page_Looper:

    def __init__(self, credentials_file='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/secret.json'):
        self.credentials = json.loads(open(credentials_file, 'r').read())

    def collect_pages(self,
                      command,
                      output_file="logs/Site_Improve_Page_Looper_" + time.asctime(time.localtime(time.time())).replace(
                          ' ', '_') + "_output.json",
                      error_output_file="logs/Site_Improve_Page_Looper_" + time.asctime(
                          time.localtime(time.time())).replace(' ', '_') + "_error_output.json",
                      error_log_file="logs/Site_Improve_Page_Looper_" + time.asctime(
                          time.localtime(time.time())).replace(' ', '_') + "_error_log.txt",
                      should_return=False,
                      should_save=True):
        initial_request = requests.get(command,
                                       auth=HTTPBasicAuth(self.credentials['userName'], self.credentials['userPass']))

        start_page_list = initial_request.json()
        page_lists = [start_page_list]

        if 'links' in start_page_list and 'next' in start_page_list['links'] and 'href' in start_page_list['links'][
            'next']:
            next_page_address = start_page_list['links']['next']['href']
        else:
            if should_return:
                return page_lists
            else:
                return
        try:
            for i in tqdm(range(start_page_list['total_pages'])):
                new_request = requests.get(next_page_address,
                                           auth=HTTPBasicAuth(self.credentials['userName'],
                                                              self.credentials['userPass']))
                new_page_list = new_request.json()
                page_lists.append(new_page_list)

                if 'links' in new_page_list and 'next' in new_page_list['links'] and 'href' in new_page_list['links'][
                    'next']:
                    next_page_address = new_page_list['links']['next']['href']
        except Exception as e:
            log = "Exception:\n" + str(e) + "\npage:\n" + str(i) + "\npagelink\n" + str(next_page_address)
            print(log)

            if should_save:
                with open(error_output_file, 'w', encoding='utf-8') as file:
                    json.dump(page_lists, file, indent=4)
                with open(error_log_file, 'w', encoding='utf-8') as file:
                    file.write(log)
            print("Error: ending execution of " + command)

            if should_return:
                return page_lists

            return

        if should_save:
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(page_lists, file, indent=4)
        if should_return:
            return page_lists
