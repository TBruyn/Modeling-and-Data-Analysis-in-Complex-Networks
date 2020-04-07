import json

path = '/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/'

allpages = json.loads(open(path + 'all_pages_formatted.json', 'r').read())
entry_point = json.loads(open(path + 'entry_points_formatted.json', 'r').read())
exit_point = json.loads(open(path + 'exit_points_formatted.json', 'r').read())

entry_point_ids = [page['id'] for page in entry_point]
exit_point_ids = [page['id'] for page in exit_point]

[page.update({'entry_point': True})
 if page['id'] in entry_point_ids
 else page.update({'entry_point': False})
 for page in allpages]

[page.update({'exit_point': True})
 if page['id'] in exit_point_ids
 else page.update({'exit_point': False})
 for page in allpages]

with open(path + 'all_pages_with_entry_exit_points.json', 'w', encoding='utf-8') as file:
    json.dump(allpages, file, indent=4)