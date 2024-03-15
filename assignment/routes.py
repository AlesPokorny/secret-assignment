import logging
import numpy as np
from typing import List, Tuple
from assignment.stops import RouteStop
from assignment.utils import generate_stops
from assignment import constants

logger = logging.getLogger(__name__)


class Route:
    def __init__(self, n_deliveries: int, n_pickups: int):
        self.n_deliveries = n_deliveries
        self.n_pickups = n_pickups

        self.possible_delivery_stops: List[RouteStop] = []
        self.chosen_deliveries: List[RouteStop] = []
        self.pickup_stops: List[RouteStop] = []

        self.planned_delivery_route: List[RouteStop] = []

        self.chosen_pickup_stop = None

        self.route_capacity_usage = 0
        self.segment_capacities: List[float] = []
        self.route_segments: List[Tuple] = []

        self.final_route: List[RouteStop] = []

    def run(self):
        self.load_all_stops()
        self.choose_most_fitting_stops()
        self.create_route()
        self.get_route_segments()
        self.calculate_route_segment_capacities()
        self.add_pickup_stop_to_route()

        # Not productionizing the the plotting but in case you wanna see it, it is here
        from assignment.plotting import plot_route

        plot_route(self.final_route)

    def load_all_stops(self):
        """
        Gets delivery and pickup stops from somewhere
        In this case it generates them but you get the point
        """
        self.get_possible_delivery_stops()
        self.get_pickup_stops()

    def get_possible_delivery_stops(self):
        """
        Generates delivery stops and saves them as classes
        in self.possible_delivery_stops.append(delivery_stop)

        It would be nice to keep the nd array for later
        but I feel like it is cheating so I throw it away
        Right now it is ok to store it in arrays but the customer stop would have more info
        so that is why I chose classes
        """
        stops = generate_stops(n=self.n_deliveries)

        for stop in stops:
            delivery_stop = RouteStop(
                x=int(stop[0]),
                y=int(stop[1]),
                size=stop[2],
                is_pickup=False,
                is_depot=False,
            )
            self.possible_delivery_stops.append(delivery_stop)

    def get_pickup_stops(self):
        """
        Generates delivery stops and saves them as classes
        in self.possible_delivery_stops.append(delivery_stop)
        """
        stops = generate_stops(n=self.n_pickups)

        for stop in stops:
            pickup_stop = RouteStop(
                x=int(stop[0]),
                y=int(stop[1]),
                size=stop[2],
                is_pickup=True,
                is_depot=False,
            )
            self.pickup_stops.append(pickup_stop)

    def choose_most_fitting_stops(self):
        """
        Selects as many of the smallest stops as it would fit the van capacity constraints
        Saves the stops self.chosen_deliveries and capacity used in self.route_capacity_usage
        """
        sorted_sizes_with_indices = self.sort_stops_by_size()

        total_selected_size = 0
        for stop in sorted_sizes_with_indices:
            stop_index = stop[0]
            stop_size = stop[1]

            if total_selected_size + stop_size <= constants.VAN_CAPACITY:
                total_selected_size += stop_size
                self.chosen_deliveries.append(self.possible_delivery_stops[stop_index])
            else:
                break

        self.route_capacity_usage = total_selected_size

        logger.info(f"Selected {len(self.chosen_deliveries)} smallest orders")

    def sort_stops_by_size(self) -> List:
        """
        Sorts delivery stops by their size and returns the sizes and indices
        It does not sort on distance, even if size is the same

        Returns:
            List: List of tuples with indices and sizes
        """
        all_sizes = [
            customer_stop.size for customer_stop in self.possible_delivery_stops
        ]
        indices = list(range(len(all_sizes)))
        sorted_sizes_with_indices = [
            (i, size) for size, i in sorted(zip(all_sizes, indices))
        ]
        return sorted_sizes_with_indices

    def create_route(self):
        """
        Creates a route based on the nearest stop. Adds depot at the beginning and the end
        Saves route in self.planned_delivery_route
        """
        self.add_depot_stop_to_route()
        previous_stop_xy = constants.DEPOT_LOCATION
        stops_left = self.chosen_deliveries.copy()

        for _ in range(len(self.chosen_deliveries)):
            distances = [
                self.calculate_distance_between_stops(
                    previous_stop_xy=previous_stop_xy, next_stop_xy=stop.get_location()
                )
                for stop in stops_left
            ]

            closest_stop_index = distances.index(min(distances))
            stop_to_plan = stops_left[closest_stop_index]

            self.planned_delivery_route.append(stop_to_plan)

            previous_stop_xy = stop_to_plan.get_location()
            stops_left.pop(closest_stop_index)
        self.add_depot_stop_to_route()

    def add_depot_stop_to_route(self):
        """
        Adds depot to a route
        """
        depot_stop = RouteStop(
            x=constants.DEPOT_LOCATION[0],
            y=constants.DEPOT_LOCATION[1],
            is_pickup=False,
            is_depot=True,
            size=0,
        )
        self.planned_delivery_route.append(depot_stop)

    @staticmethod
    def calculate_distance_between_stops(
        previous_stop_xy: Tuple[int, int], next_stop_xy: Tuple[int, int]
    ) -> int:
        """
        Calculates the squared distance between two stops

        Args:
            previous_stop_xy (Tuple[int, int]): the X and Y coordinates of the previous stop
            next_stop_xy (Tuple[int, int]): the X and Y coordinates of the stop to check

        Returns:
            int: the squared distance
        """
        distance_x = previous_stop_xy[0] - next_stop_xy[0]
        distance_y = previous_stop_xy[1] - next_stop_xy[1]

        return distance_x**2 + distance_y**2

    def get_route_segments(self):
        """
        Gets route segments from the routes and saves it in self.route_segments
        """
        self.route_segments = [
            (stop.x, stop.y, next_stop.x, next_stop.y)
            for stop, next_stop in zip(
                self.planned_delivery_route, self.planned_delivery_route[1:]
            )
        ]

    def calculate_route_segment_capacities(self):
        """
        Calculates the route capacity at each segment - after the starting stop
        and saves in self.segment_capacities
        """
        capacity = 50 - self.route_capacity_usage
        self.segment_capacities.append(capacity)
        for chosen_delivery in self.planned_delivery_route[1:-1]:
            capacity += chosen_delivery.size
            self.segment_capacities.append(capacity)

    def add_pickup_stop_to_route(self):
        """
        Adds one pickup stop to the delivery route by finding the distance
        of each stop to the delivery route and choosing the one with the smallest distance.
        If two distances are equal, it prioritizes the smaller one so the delivery people
        don't have to carry too much.

        If the closest pickup stop fits into the route, it inserts the stop in the route,
        otherwise it checks the next one

        Final route is saved in self.final_route and chosen stop in self.chosen_pickup_stop
        """
        closest_distances = self.calculate_pickup_stop_distances_to_nearest_segment()

        sizes = np.array([stop.size for stop in self.pickup_stops])
        best_pickup_stops = np.lexsort((sizes, closest_distances[:, 0]))

        for best_stop_index in best_pickup_stops:
            stop_size = self.pickup_stops[best_stop_index].size
            segment_index = closest_distances[best_stop_index, 1]

            if stop_size <= self.segment_capacities[segment_index]:
                self.chosen_pickup_stop = self.pickup_stops[best_stop_index]
                self.final_route = self.planned_delivery_route.copy()
                self.final_route.insert(segment_index, self.chosen_pickup_stop)

                logger.info(
                    f"Pickup stop with location {self.chosen_pickup_stop.get_location()} was chosen"
                )
                break

    def calculate_pickup_stop_distances_to_nearest_segment(self) -> np.array:
        """_summary_
            It calculates the squared distance between the stop and the delivery route
        Returns:
            np.array: array of tuples containing the squared distances between each
            pickup stops and the index of the closest index to the stop
        """
        n_pickups = len(self.pickup_stops)
        pickup_stops = [stop.get_location() for stop in self.pickup_stops]

        closest_distances = np.zeros((n_pickups, 2), dtype=int)

        route_segments = np.array(self.route_segments).T

        x_diffs = route_segments[2, :] - route_segments[0, :]
        y_diffs = route_segments[3, :] - route_segments[1, :]

        segment_lengths_squared = x_diffs**2 + y_diffs**2
        x_diffs_sq = x_diffs / segment_lengths_squared
        y_diffs_sq = y_diffs / segment_lengths_squared

        for i, pickup_stop_location in enumerate(pickup_stops):
            stop_x_diff = pickup_stop_location[0] - route_segments[0]
            stop_y_diff = pickup_stop_location[1] - route_segments[1]

            u = stop_x_diff * x_diffs_sq + stop_y_diff * y_diffs_sq
            u = np.clip(u, 0, 1)

            distance_squared = (stop_x_diff - u * x_diffs) ** 2 + (
                stop_y_diff - u * y_diffs
            ) ** 2

            min_distance = min(distance_squared)
            segment_index = np.where(distance_squared == min_distance)[0][-1]

            closest_distances[i] = [min_distance, segment_index]

        return closest_distances
