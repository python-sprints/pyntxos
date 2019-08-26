print("Do not import utils.scrape without running pip install -r scrape_requirements.")

from functools import lru_cache

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim, OpenMapQuest

# import utils.data

bilbao_turismo_base_url = "http://www.bilbaoturismo.net"
max_bilbao_turismo_pintxo_finder_pages = 10

dummy = [
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


def scrape(dummy_flag=False, api_key=None):

    if dummy_flag:
        data = dummy
    else:
        data = get_bilbao_turismo_data(api_key=api_key)

    return data


@lru_cache(maxsize=1)
def get_requests_session():
    return requests.session()


def get_bilbao_turismo_data(api_key=None):
    restaurant_links = get_bilbao_turismo_restaurant_links()
    data = get_bilbao_turismo_restaurant_infos(restaurant_links=restaurant_links)
    data = get_longitude_latitude_info(data=data, api_key=api_key)
    return data


def get_bilbao_turismo_link(end_url):
    base_url = bilbao_turismo_base_url
    return f"{base_url}{end_url}"


def get_bilbao_turismo_restaurant_links():

    # This link contains all the zones which we will scrape through to get the restaurants
    pintxos_finder_link = get_bilbao_turismo_link("/BilbaoTurismo/en/pintxo-finder_2")
    print(f"pintxos_finder_link: {pintxos_finder_link}")

    session = get_requests_session()
    r = session.get(pintxos_finder_link)
    soup = BeautifulSoup(r.text, features="html.parser")

    # Get all href with "=zona" for zones
    all_links = soup.select("a[href*=zona]")
    zones = [
        link.attrs["href"].split("zona=")[-1].replace("&tipologia=", "").split(",")
        for link in all_links
    ]
    zones = list(set([item for sublist in zones for item in sublist if item != ""]))

    # Now get link with all the zones
    all_zones_link = f'{pintxos_finder_link}/?zona={",".join(zones)}'
    print(f"Link with all zones: {all_zones_link}")

    # Loop through pages to find restaurant links
    restaurant_links = []
    for page in range(1, max_bilbao_turismo_pintxo_finder_pages):
        page_link = f"{all_zones_link}&pagina={page}"
        print(f"Working on page {page}: {page_link}")

        r = session.get(page_link)
        soup = BeautifulSoup(r.text, features="html.parser")
        # Get all the restaurant links by filtering on "/pintxo-finder/"
        single_page_restaurant_links = [
            get_bilbao_turismo_link(item.attrs["href"])
            for item in soup.select("a[href*=\/pintxo-finder\/]")
        ]
        restaurant_links += single_page_restaurant_links

    restaurant_links = list(set(restaurant_links))

    return restaurant_links


def get_bilbao_turismo_restaurant_infos(restaurant_links):
    data = []
    session = get_requests_session()
    for index, restaurant_link in enumerate(restaurant_links):
        print(f"Working on getting restaurant info {index}: {restaurant_link}")
        r = session.get(restaurant_link)
        soup = BeautifulSoup(r.text, features="html.parser")

        # Get relevant data
        name = soup.find("h2", itemprop="name")
        description = soup.find("span", itemprop="description")
        address = soup.find("span", itemprop="address")

        # Massage the data
        name = " ".join([item.capitalize() for item in name.contents[0].split(" ")]).strip()
        description = str(description.contents[0].contents[0]).strip()

        telephone = address.find("span", itemprop="telephone")
        if telephone is not None:
            telephone = str(telephone.contents[0]).strip().replace(' ', '')

        email = address.find("span", itemprop="email")
        if email is not None:
            email = str(email.contents[0]).strip()

        try:
            metro_stop = [
                str(item.replace('Metro stop:', '')).strip()
                for item in address.contents
                if 'Metro stop:' in item
            ][0]
        except:
            metro_stop = None

        address = dict(
            street_address=str(address.find("span", itemprop="streetAddress").contents[0]).strip(),
            post_code=str(address.find("span", itemprop="postalCode").contents[0]).strip(),
            town=str(address.find("span", itemprop="addressLocality").contents[0]).strip(),
        )

        restaurant_info = dict(
            name=name,
            street_address=address["street_address"],
            post_code=address["post_code"],
            town=address["town"],
            telephone=telephone,
            email=email,
            address=f'{address["street_address"]} {address["post_code"]} {address["town"]}, Spain',
            metro_stop=metro_stop,
            description=description,
        )
        data.append(restaurant_info)
    return data


def get_longitude_latitude_info(data, api_key=None):

    if api_key is None:
        geolocator = Nominatim(user_agent='pyntxos')
    else:
        geolocator = OpenMapQuest(user_agent='pyntxos', api_key=api_key)

    failure_count = 0
    for index, pintxo in enumerate(data):
        location = geolocator.geocode(f'{pintxo["name"]}, {pintxo["post_code"]}, Bilbao, Spain')

        if location is None:
            location = geolocator.geocode(pintxo["address"])

        if location is not None:
            print(
                f'{index} - Success - {pintxo["name"]} - Getting Longitude and Latitude'
            )
            data[index]["geopy_address"] = location.address
            data[index]["longitude"] = location.longitude
            data[index]["latitude"] = location.latitude
        else:
            data[index]["longitude"] = None
            data[index]["latitude"] = None
            print(
                f'{index} - Failure - {pintxo["name"]} - Getting Longitude and Latitude'
            )
            failure_count += 1

    print(
        f'{failure_count / len(data) * 100:.0f}% failed for getting longitude and latitude.'
    )
    return data
