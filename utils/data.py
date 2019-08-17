import os
import json

default_data_path = './data'

dummy = [
    {'name': 'Argotia', 'latitude': 43.2590929, 'longitude': -2.9244257, 'address': 'Plaza Nueva, 48005 Bilbao, Vizcaya, Spain'},
    {'name': 'Sorginzulo', 'latitude': 43.259387, 'longitude': -2.9233905, 'address': 'Plaza Nueva, 12, 48005 Bilbao, BI, Spain'},
    ]


def scrape(data_path=None, dummy_flag=False):

    if data_path is None:
        data_path = default_data_path

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    data_file_path = os.path.join(data_path, 'data.json')

    if dummy_flag:
        data = dummy
    else:
        # TODO Need to change the following to have real data
        data = dummy

    with open(data_file_path, 'w') as file:
        json.dump(data, file)


def load(data_path=None):

    if data_path is None:
        data_path = default_data_path

    data_file_path = os.path.join(data_path, 'data.json')

    with open(data_file_path, 'r') as file:
        data = json.load(file)

    return data
