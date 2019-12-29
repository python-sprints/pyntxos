from copy import deepcopy
import pandas as pd
import numpy as np
# import mlrose
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from scipy.spatial import distance_matrix
from typing import Dict


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

    # inverse_route = {value: key for key, value in route.items()}
    #
    # tsp_series = (distance_df
    #     .loc[route.values(), route.values()]
    #     .rename(columns=inverse_route, index=inverse_route)
    #     .stack()
    #     )
    # tsp_series = tsp_series.loc[tsp_series != 0] * 1_000_000
    # tsp_series.loc[(inverse_route[end], inverse_route[start])] = 0.0001
    # tsp_series.loc[(inverse_route[start], inverse_route[end])] = 0.0001
    # tsp_dist_list = zip(tsp_series.index.get_level_values(0), tsp_series.index.get_level_values(1), tsp_series.values)
    # fitness_dist = mlrose.TravellingSales(distances=tsp_dist_list)
    # problem_fit = mlrose.TSPOpt(length=n_stops, fitness_fn=fitness_dist, maximize=False)
    # best_route, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob=0.2, max_attempts=100, random_state=2)
    # best_route = np.roll(best_route, -np.argwhere(best_route == inverse_route[start])[0])
    # if best_route[1] == inverse_route[end]:
    #     best_route = np.roll(best_route[::-1], 1)
    # route = [route[item] for item in best_route]

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


def constraint_programming(df, start, end, n_stops, distance_measure=None):

    # Distances between nodes will be very small, and this library requires
    # integers to work, so we will multiply them by this multiplier and round
    # to the nearest integer.
    MULTIPLIER = 10 ** 6

    def create_data_model(
        df: pd.DataFrame, start: int, end: int, n_stops: int, distance_measure: str
    ) -> Dict:
        """Stores the data for the problem."""
        data = {}
        if isinstance(distance_measure, str):
            distance_measure_dict = {"Euclidean": 2, "Manhattan": 1, "Infinity": np.inf}
            distance_measure = distance_measure_dict.get(
                distance_measure, distance_measure_dict["Euclidean"]
            )
        data["distance_matrix"] = (
            distance_matrix(df, df, p=distance_measure) * MULTIPLIER
        ).astype(int)
        data["vehicle_capacities"] = [n_stops - 1]
        data["demands"] = [1] * len(df)
        return data

    def get_route(data, manager, routing, assignment):
        total_distance = 0
        index = routing.Start(0)
        route_distance = 0
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
            route.append(node_index)
        route.append(manager.IndexToNode(index))
        total_distance += route_distance
        return route

    def main(df: pd.DataFrame, start: int, end: int, n_stops: int, distance_measure: str):
        """Entry point of the program."""
        data = create_data_model(df, start, end, n_stops, distance_measure)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), 1, [int(start)], [int(end)]
        )

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data["vehicle_capacities"],  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity",
        )

        # Allow for missing nodes
        for node in range(len(data["distance_matrix"])):
            if node in [start, end]:
                continue
            routing.AddDisjunction([manager.NodeToIndex(node)], MULTIPLIER ** 2)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if assignment:
            route = get_route(data, manager, routing, assignment)
            return route
        return None

    return main(df, start, end, n_stops, distance_measure)
