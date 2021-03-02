import json


def get_data_from_json(path):
  with open(path) as f:
    data = json.load(f)
    return data