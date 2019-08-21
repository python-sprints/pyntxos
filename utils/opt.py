from copy import deepcopy
import numpy as np


def distance(start, end):
    """Linear distance between start and end pyntox location"""
    dx = start["longitude"] - end["longitude"]
    dy = start["latitude"] - end["latitude"]
    return np.linalg.norm((dx, dy))


def traverse_closest(start, destinations, N):
    """From the pyntox location 'start' provide a list of N
    locations from 'destinations' by always moving to the closest one."""
    dests = deepcopy(destinations)
    route = []
    current = start
    for i in range(5):
        mini = np.argmin([distance(current, dest) for dest in dests])
        current = dests.pop(mini)
        route.append(current["name"])
    return route
