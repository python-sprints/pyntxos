from copy import deepcopy
import numpy as np


def distance(start, end):
    """Linear distance between start and end pyntox location"""
    dx = start["longitude"] - end["longitude"]
    dy = start["latitude"] - end["latitude"]
    return np.linalg.norm((dx, dy))


def route_length(route):
    return sum([distance(d1, d2) for d1, d2 in zip(route, route[1:])])


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


def shortest_N_stop_route(start, end, destinations, N):
    """From the pyntox location 'start' return a list of locations
    defining a route to the location 'end' with N stops, selected
    from the list 'destinations'. Attempts to find the shortest
    possible route.
    """
    dests = deepcopy(destinations)
    route = [start, end]
    for i in range(N):
        route_proposals = {}
        # get route proposals by inserting all possible destinations
        # into valid positions and calculating the resulting route length
        for dest in dests:
            for j in range(1, len(route)):
                route_proposal = route[:j] + [dest] + route[j:]
                route_proposals[route_length(route_proposal)] = route_proposal

        # choose the proposal with the shortest distance and remove
        # the added destination from the list of possibilities
        min_dist = min(route_proposals.keys())
        new_route = route_proposals[min_dist]
        for dest in new_route:
            if dest not in route:
                dests.pop(dests.index(dest))
        route = new_route

    return route
