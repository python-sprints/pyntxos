import data.utils as data_utils
from .base import make_and_save_map


def test_make_and_save_map():
    data = data_utils.dummy_data
    make_and_save_map(data=data)
    print('bla')
