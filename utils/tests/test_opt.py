import pytest
import pandas as pd

import utils.data
import utils.opt


@pytest.fixture()
def data():
    return utils.data.load()


def test_get_df(data):
    df = utils.opt.get_df(data=data)
    assert isinstance(df, pd.DataFrame)


@pytest.fixture()
def df(data):
    return utils.opt.get_df(data)


@pytest.mark.parametrize('start, end, n_stops, distance_measure', [
    ('Urkia Taberna', 'Gure Toki', 10, 'Manhattan'),
    ('Urkia Taberna', 'Gure Toki', 2, 'Manhattan'),
    ('Urkia Taberna', 'Gure Toki', 40, 'Manhattan'),
    ('Urkia Taberna', 'Gure Toki', 10, 'Euclidean'),
    ('Urkia Taberna', 'Gure Toki', 10, 'Infinity'),
    ('Urkia Taberna', 'Gure Toki', 10, 1.75),
    ('Gure Toki', 'Urkia Taberna', 10, 'Manhattan'),
    ('Motrikes', 'Gure Toki', 10, 'Manhattan'),
    ('Urkia Taberna', 'Zuga', 10, 'Manhattan'),
    ('Motrikes', 'Zuga', 10, 'Manhattan'),
])
def test_get_constraint_programming(df, start, end, n_stops, distance_measure):
    route = utils.opt.constraint_programming(
        df[['longitude', 'latitude']],
        start=df.index[df['name'] == start][0],
        end=df.index[df['name'] == end][0],
        n_stops=n_stops,
        distance_measure=distance_measure,
    )
    assert len(set(route)) == n_stops
