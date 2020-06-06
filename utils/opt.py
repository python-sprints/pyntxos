import pandas as pd
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from scipy.spatial import distance_matrix
from typing import Dict, Union


def get_df(data: Dict):
    return pd.DataFrame(data)


def constraint_programming(df: pd.DataFrame, start: int, end: int, n_stops: int,
                           distance_measure: Union[str, float] = None):

    # Distances between nodes will be very small, and this library requires
    # integers to work, so we will multiply them by this multiplier and round
    # to the nearest integer.
    MULTIPLIER = 10 ** 6

    def create_data_model(df: pd.DataFrame, n_stops: int, distance_measure: Union[str, float] = None) -> Dict:
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

    def get_route(manager, routing, assignment):
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
        data = create_data_model(df, n_stops, distance_measure)

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
            route = get_route(manager, routing, assignment)
            return route
        return None

    return main(df, start, end, n_stops, distance_measure)
