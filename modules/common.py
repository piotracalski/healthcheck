import json


def get_data_from_json(path):
  with open(path) as f:
    data = json.load(f)
    return data


def save_data_to_json(path, data):
  with open(path, 'w') as outfile:
    json.dump(data, outfile)