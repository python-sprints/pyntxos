from copy import deepcopy
import pandas as pd
import numpy as np


def get_distance(start, end, measure=None):
    return np.linalg.norm([start['longitude'] - end['longitude'], start['latitude'] - end['latitude']], ord=measure)


def get_df(data):
    df = pd.DataFrame(data)
    df['location'] = [
        pd.Series(item)
        for item in df[['longitude', 'latitude']].apply(lambda row: row.to_dict(), axis=1).to_list()
    ]
    return df


def get_straight_line(start, end, n_stops):
    longitude_line = np.linspace(start=start['longitude'], stop=end['longitude'], num=n_stops)
    latitude_line = np.linspace(start=start['latitude'], stop=end['latitude'], num=n_stops)
    straight_line = pd.DataFrame({'location': [
        pd.Series({'longitude': item[0], 'latitude': item[1]})
        for item in zip(longitude_line, latitude_line)
    ]})
    return straight_line


def get_distance_df(s_1, s_2, distance_measure=None):

    if isinstance(distance_measure, str):
        distance_measure_dict = {'Euclidean': 2, 'Manhattan': 1, 'Infinity': np.inf}
        distance_measure = distance_measure_dict.get(distance_measure, distance_measure_dict['Euclidean'])

    distance_df = pd.DataFrame(0, index=s_1.index, columns=s_2.index)
    for index_1, value_1 in s_1.iteritems():
        for index_2, value_2 in s_2.iteritems():
            distance_df.loc[index_1, index_2] = get_distance(start=value_1, end=value_2, measure=distance_measure)

    closest_nodes_df = pd.DataFrame(
        np.argsort(distance_df, axis=0),
        index=distance_df.index,
        columns=distance_df.columns
    )

    return distance_df, closest_nodes_df


def get_shortest_path(df, start, end, n_stops, distance_measure=None):

    if isinstance(start, str):
        start = df.index[df['name'] == start][0]

    if isinstance(end, str):
        end = df.index[df['name'] == end][0]

    # Get straight line from start to end
    straight_line_df = get_straight_line(start=df.loc[start], end=df.loc[end], n_stops=n_stops)
    distance_df, closest_nodes_df = get_distance_df(
        df['location'],
        straight_line_df['location'],
        distance_measure=distance_measure,
    )

    # Find closest unique nodes to the straight line which is evenly spaced out
    route = {0: start}
    taken_nodes = {start, end}
    for index, nodes in closest_nodes_df[np.arange(1, n_stops-1)].iteritems():
        route[index] = nodes.loc[~nodes.isin(taken_nodes)].sort_index().iloc[0]
        taken_nodes.add(route[index])
    route[n_stops-1] = end

    # Now need to do a second pass to move to the next node which is the closest
    distance_df, closest_nodes_df = get_distance_df(
        df['location'],
        df['location'],
        distance_measure=distance_measure,
    )

    index_to_adjust = range(1, n_stops - 1)
    left_nodes = set([route[item] for item in index_to_adjust])
    for index in index_to_adjust:
        previous = route[index-1]
        closest_nodes = closest_nodes_df[previous]
        route[index] = closest_nodes.loc[closest_nodes.isin(left_nodes)].sort_index().iloc[0]
        left_nodes.remove(route[index])

    route = pd.Series(route).sort_index().tolist()

    return route


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
