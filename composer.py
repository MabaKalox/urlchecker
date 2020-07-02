import json

with open('metric_res.json', 'r') as file:
    metric_res = json.loads(file.read())

with open('english_res.json', 'r') as file:
    english_res = json.loads(file.read())

metric_exist = set(metric_res['exist'])
metric_non_exist = set(metric_res['non-exist'])
english_exist = set(english_res['exist'])
english_non_exist = set(english_res['non-exist'])

metric_non_exist.intersection_update(english_non_exist)
print(len(metric_non_exist))
