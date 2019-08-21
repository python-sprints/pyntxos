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
    for i in range(N):
        mini = np.argmin([distance(current, dest) for dest in dests])
        current = dests.pop(mini)
        route.append(current["name"])
    return route


def traverse(start, end, destinations, N):
    """From the pyntox location 'start' return a list of locations
    defining a route to the location 'end' with N stops, selected
    from the list 'destinations',
    """
    dests = deepcopy(destinations)
    route = [start]
    current = start
    for i in range(N):
        dists = [distance(current, dest) for dest in dests]
        end_dists = [distance(dest, end) for dest in dests]
        min_ind = np.argmin([d + ed for d, ed in zip(dists, end_dists)])
        current = dests.pop(min_ind)
        route.append(current)
    return route + [end]
