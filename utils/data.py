import json
import os

default_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
default_file_name = "data.json"


def dump(data, data_path=None):

    if data_path is None:
        data_path = default_data_path

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    data_file_path = os.path.join(data_path, default_file_name)

    with open(data_file_path, "w") as file:
        json.dump(data, file)


def load(data_path=None):

    if data_path is None:
        data_path = default_data_path

    data_file_path = os.path.join(data_path, default_file_name)

    with open(data_file_path, "r") as file:
        data = json.load(file)

    data = [
        item
        for item in data
        if item['longitude'] is not None and item['latitude'] is not None
    ]

    return data
