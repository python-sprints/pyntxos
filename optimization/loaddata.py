import networkx
import json
import itertools
from distance import compute_distance

def load_data(file_name):
    data = None
    with open(file_name) as data_file:
        data = json.load(data_file)

    graph = networkx.Graph()
    for resturant1, resturant2 in itertools.product(data, repeat=2):
        dist = compute_distance(resturant1["latitude"], resturant1["longitude"],
                                resturant2["latitude"], resturant2["longitude"]
        graph.add_edge(resturant1["name"], resturant2["name"], weight= dist)
    return graph


def get_shortest_path(graph, start, end):
    return graph.shortest_path(source=star, target=end, weight='weight')
