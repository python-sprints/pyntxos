import os
import json
from requests_html import HTMLSession
from functools import lru_cache
from bs4 import BeautifulSoup

default_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
default_file_name = 'data.json'
bilbao_turismo_base_url = 'http://www.bilbaoturismo.net'


dummy = [
    {'name': 'Argotia', 'latitude': 43.2590929, 'longitude': -2.9244257, 'address': 'Plaza Nueva, 48005 Bilbao, Vizcaya, Spain'},
    {'name': 'Sorginzulo', 'latitude': 43.259387, 'longitude': -2.9233905, 'address': 'Plaza Nueva, 12, 48005 Bilbao, BI, Spain'},
    ]


def scrape(dummy_flag=False):

    if dummy_flag:
        data = dummy
    else:
        # TODO Need to change the following to have real data
        restaurant_links = get_bilbao_turismo_restaurant_links()
        session = get_html_session()
        for restaurant_link in restaurant_links:
            r = session.get(get_bilbao_turismo_link(restaurant_link))
            soup = BeautifulSoup(r.text, 'html.parser')
            name = soup.find('h2', itemprop='name')
            address = soup.find('span', itemprop='address')
            description = soup.find('span', itemprop='description')
            data = dummy

    return data


@lru_cache(maxsize=1)
def get_html_session():
    return HTMLSession()


def get_bilbao_turismo_link(end_url):
    base_url = bilbao_turismo_base_url
    return f'{base_url}/{end_url}'


def get_bilbao_turismo_restaurant_links():

    pintxos_finder_link = get_bilbao_turismo_link('BilbaoTurismo/en/pintxo-finder_2')
    session = get_html_session()
    r = session.get(pintxos_finder_link)
    zones = [
        link.split('zona=')[-1].replace('&tipologia=', '')
        for link in r.html.links if 'pintxo-finder_2?zona=' in link
    ]
    all_zones_link = f'{pintxos_finder_link}/?zona={",".join(zones)}'
    restaurant_links = []
    for page in range(1, 10):
        r = session.get(f'{all_zones_link}&pagina={page}')
        restaurant_links.append([link for link in r.html.links if 'pintxo-finder/' in link])

    restaurant_links = list(set([item for sublist in restaurant_links for item in sublist]))

    return restaurant_links


def dump(data, data_path=None):

    if data_path is None:
        data_path = default_data_path

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    data_file_path = os.path.join(data_path, default_file_name)

    with open(data_file_path, 'w') as file:
        json.dump(data, file)


def load(data_path=None):

    if data_path is None:
        data_path = default_data_path

    data_file_path = os.path.join(data_path, default_file_name)

    with open(data_file_path, 'r') as file:
        data = json.load(file)

    return data
