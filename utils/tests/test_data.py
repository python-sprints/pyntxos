import os
import utils.data

test_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

dummy_data = [
    {'name': 'Argotia', 'latitude': 43.2590929, 'longitude': -2.9244257, 'address': 'Plaza Nueva, 48005 Bilbao, Vizcaya, Spain'},
    {'name': 'Sorginzulo', 'latitude': 43.259387, 'longitude': -2.9233905, 'address': 'Plaza Nueva, 12, 48005 Bilbao, BI, Spain'},
    ]


def test_dump():
    utils.data.dump(data=dummy_data, data_path=test_data_path)
    assert os.path.exists(os.path.join(test_data_path, utils.data.default_file_name))


def test_load():
    data = utils.data.load(data_path=test_data_path)
    assert data == dummy_data
