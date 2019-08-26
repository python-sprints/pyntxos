import pytest
import numpy as np
import pandas as pd
import networkx as nx

import utils.data
import utils.opt


@pytest.mark.parametrize('input, expected_distance', [
    [dict(start={'longitude': 0, 'latitude': 0}, end={'longitude': 0, 'latitude': 0}), 0],
    [dict(start={'longitude': 1, 'latitude': 0}, end={'longitude': 0, 'latitude': 1}), np.sqrt(2)],
    [dict(start={'longitude': 1, 'latitude': 0}, end={'longitude': 0, 'latitude': 1}, measure=1), 2],
    [dict(start={'longitude': 1, 'latitude': 0}, end={'longitude': 0, 'latitude': 1}, measure=np.inf), 1],
])
def test_get_distance(input, expected_distance):
    distance = utils.opt.get_distance(**input)
    assert distance == expected_distance



@pytest.fixture()
def dummy_data():
    data = [
        {
            "name": "Argotia",
            "latitude": 43.2590929,
            "longitude": -2.9244257,
            "address": "Plaza Nueva, 48005 Bilbao, Vizcaya, Spain",
            "telephone": None,
        },
        {
            "name": "Sorginzulo",
            "latitude": 43.259387,
            "longitude": -2.9233905,
            "address": "Plaza Nueva, 12, 48005 Bilbao, BI, Spain",
            "telephone": None,
        },
    ]
    return data


@pytest.fixture()
def data():
    return utils.data.load()


def test_get_df(data):
    df = utils.opt.get_df(data=data)
    assert isinstance(df, pd.DataFrame)


@pytest.fixture()
def df(data):
    return utils.opt.get_df(data)


def test_get_straight_line(dummy_data):
    data = dummy_data
    start = data[0]
    end = data[1]
    n_stops = 10

    line_df = utils.opt.get_straight_line(start=start, end=end, n_stops=n_stops)

    start_line = line_df['location'].iloc[0]
    end_line = line_df['location'].iloc[-1]

    assert len(line_df) == n_stops
    assert start_line['longitude'] == start['longitude'] and start_line['latitude'] == start['latitude']
    assert end_line['longitude'] == end['longitude'] and end_line['latitude'] == end['latitude']


def test_get_shortest_path(df):
    n_stops = 10
    route = utils.opt.get_shortest_path(df, start=0, end=1, n_stops=n_stops)
    assert len(set(route)) == n_stops



