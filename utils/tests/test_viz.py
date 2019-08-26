import pytest

import utils.viz
import utils.scrape


@pytest.mark.parametrize("num_restaurants", [(1), (2)])
def test_select_num_restaurants(num_restaurants):
    data = utils.scrape.scrape(dummy_flag=True)
    map_ = utils.viz.get_map(data, num_restaurants)
    assert (
        len([i for i in map_.to_dict()["children"] if "marker" in i]) == num_restaurants
    )


def test_select_num_restaurants_zero():
    data = utils.scrape.scrape(dummy_flag=True)
    with pytest.raises(ValueError, match="`num_restaurants` must be at least 1!"):
        utils.viz.get_map(data, 0)


def test_select_num_restaurants_pizza():
    data = utils.scrape.scrape(dummy_flag=True)
    with pytest.raises(ValueError, match="`num_restaurants` must be integer or None!"):
        utils.viz.get_map(data, "pizza")


def test_select_num_restaurants_all():
    data = utils.scrape.scrape(dummy_flag=True)
    map_ = utils.viz.get_map(data)
    assert len([i for i in map_.to_dict()["children"] if "marker" in i]) == len(data)
