import os
import utils.data


data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')


def test_scrape():
    data = utils.data.scrape(dummy_flag=True)
    assert data == utils.data.dummy
    # data = utils.data.scrape()


def test_dump():
    utils.data.dump(data=utils.data.scrape(dummy_flag=True), data_path=data_path)
    assert os.path.exists(os.path.join(data_path, utils.data.default_file_name))


def test_load():
    data = utils.data.load(data_path=data_path)
    assert data == utils.data.dummy
