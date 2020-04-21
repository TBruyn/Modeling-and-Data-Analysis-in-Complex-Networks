import json
import os
import glob
import time
import pprint
import random
import math

path = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/'
timestamp = time.asctime(time.localtime(time.time())).replace(' ', '_')

os.chdir(path)
json_files = []
file_list = []
for file in glob.glob('traffic_pages*.json'):
    try:
        file_list.append(file)
        json_files.append(json.loads(open(path + file, 'r').read()))
    except Exception as e:
        print(e)
        print(file)

merged_traffic = {}

[merged_traffic.update(file) for file in json_files]

traffic_array = list(merged_traffic.values())

choice_1 = random.sample(traffic_array, k=math.floor(len(traffic_array)/2))
choice_2 = [page for page in traffic_array if page not in choice_1]

with open(path + 'merged_traffic_' + timestamp + '.json', 'w', encoding='utf-8') as file:
    json.dump(merged_traffic, file, indent=4)

with open(path + 'merged_traffic_array_latest.json', 'w', encoding='utf-8') as file:
    json.dump(traffic_array, file, indent=4)

with open(path + 'merged_traffic_array_half_1.json', 'w', encoding='utf-8') as file:
    json.dump(choice_1, file, indent=4)

with open(path + 'merged_traffic_array_half_2.json', 'w', encoding='utf-8') as file:
    json.dump(choice_2, file, indent=4)

print("Merged:")
pprint.pprint(file_list)
print("Number of visitors in traffic")
print(len(merged_traffic))
print("Output files:")
print(path + 'merged_traffic_array_latest.json')
print(path + 'merged_traffic_' + timestamp + '.json')
print(path + 'merged_traffic_array_half_1.json')
print(path + 'merged_traffic_array_half_2.json')
