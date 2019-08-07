"""
Example of how to run:

$ python geoviz -f data.json

This will save an html.
"""

import folium
import argparse
import json

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', type=str,
                    help='filename')

m = folium.Map(location=[43.2590929, -2.9244257], zoom_start=20)

tooltip = "Click me!"

args = parser.parse_args()
print(args.f)

with open(args.f, 'r') as file_:
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

m.save('visualisation.html')
