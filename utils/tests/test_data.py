import os
import utils


def test_scrape():
    utils.data.scrape()
    assert os.path.exists('./data/data.json')


def test_load():
    data = utils.data.load()
    assert data == utils.data.dummy
