import os
import data.utils as data_utils


def test_scrape_data():
    data_utils.scrape_data(data_path='..')
    assert os.path.exists('../data.json')


def test_get_data():
    data = data_utils.get_data(data_path='..')
    assert data == data_utils.dummy_data
