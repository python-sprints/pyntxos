"""
Example of how to run:

>>> 

This will save an html.
"""

import folium
import argparse
import json

def make_and_save_map(filename):

    m = folium.Map(location=[43.2590929, -2.9244257], zoom_start=20)

    tooltip = "Click me!"


    with open(filename, 'r') as file_:
        data = json.load(file_)['data']


    for i in data:
        folium.Marker(
            [i["latitude"], i["longitude"]],
            popup=f"<i>{i['name']}</i>\n{i['address']}",
            tooltip=tooltip,
        ).add_to(m)

    for n in range(len(data) - 1):
        folium.ColorLine(
            [
                (data[n]["latitude"], data[n]["longitude"]),
                (data[n + 1]["latitude"], data[n + 1]["longitude"]),
            ],
            [1],
            weight=3,
            colormap=["green", "red"],
        ).add_to(m)

    return m
