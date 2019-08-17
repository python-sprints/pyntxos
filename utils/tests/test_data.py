import os
import utils.data


def test_scrape():
    utils.data.scrape(data_path='../../data/', dummy_flag=True)
    assert os.path.exists('../../data/data.json')


def test_load():
    data = utils.data.load(data_path='../../data/')
    assert data == utils.data.dummy
