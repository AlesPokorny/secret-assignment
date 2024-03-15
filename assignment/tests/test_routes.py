from unittest import mock
import pytest
import numpy as np
from assignment.routes import Route


@pytest.fixture
def mock_route() -> Route:
    route = Route(n_deliveries=10, n_pickups=5)
    return route


@mock.patch("assignment.routes.Route.load_all_stops")
@mock.patch("assignment.routes.Route.choose_most_fitting_stops")
@mock.patch("assignment.routes.Route.create_route")
@mock.patch("assignment.routes.Route.get_route_segments")
@mock.patch("assignment.routes.Route.calculate_route_segment_capacities")
@mock.patch("assignment.routes.Route.add_pickup_stop_to_route")
@mock.patch("assignment.plotting.plot_route")
def test_run(
    mock_plot_route,
    mock_add_pickup_stop_to_route,
    mock_calculate_route_segment_capacities,
    mock_get_route_segments,
    mock_create_route,
    mock_choose_most_fitting_stops,
    mock_load_all_stops,
    mock_route,
):
    mock_route.run()

    mock_load_all_stops.called
    mock_choose_most_fitting_stops.called
    mock_create_route.called
    mock_get_route_segments.called
    mock_calculate_route_segment_capacities.called
    mock_add_pickup_stop_to_route.called


def test_get_possible_delivery_stops(mock_route):
    mock_route.get_possible_delivery_stops()

    first_stop = mock_route.possible_delivery_stops[0]

    assert len(mock_route.possible_delivery_stops) == mock_route.n_deliveries
    assert not first_stop.is_pickup
    assert not first_stop.is_depot


def test_get_pickup_stops(mock_route):
    mock_route.get_pickup_stops()

    first_stop = mock_route.pickup_stops[0]

    assert len(mock_route.pickup_stops) == mock_route.n_pickups
    assert first_stop.is_pickup
    assert not first_stop.is_depot


@mock.patch("assignment.constants.VAN_CAPACITY", 4.5)
def test_choose_most_fitting_stops(mock_route, mock_possible_deliveries):
    mock_route.possible_delivery_stops = mock_possible_deliveries.copy()
    mock_route.choose_most_fitting_stops()

    assert len(mock_route.chosen_deliveries) == 2
    assert mock_route.chosen_deliveries[0].get_location() == (88, 373)
    assert mock_route.chosen_deliveries[1].get_location() == (331, 459)
    assert mock_route.route_capacity_usage == 4.0

    print()


def test_create_route(mock_route, mock_chosen_deliveries):

    mock_route.chosen_deliveries = mock_chosen_deliveries.copy()

    mock_route.create_route()

    expected_stop_order = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (0, 0)]

    for stop_i, route_stop in enumerate(mock_route.planned_delivery_route):
        assert route_stop.get_location() == expected_stop_order[stop_i]


def test_calculate_distance_between_stops(mock_route):
    output = mock_route.calculate_distance_between_stops(
        previous_stop_xy=(5, 10), next_stop_xy=(2, 12)
    )
    expected_output = 13
    assert output == expected_output


def test_get_route_segments(mock_route, mock_chosen_deliveries, mock_route_segments):
    mock_route.chosen_deliveries = mock_chosen_deliveries.copy()
    mock_route.create_route()
    mock_route.get_route_segments()

    assert mock_route.route_segments == mock_route_segments


def test_calculate_segment_capacities(mock_route, mock_chosen_deliveries):
    mock_route.chosen_deliveries = mock_chosen_deliveries.copy()
    mock_route.create_route()
    mock_route.route_capacity_usage = 8
    mock_route.calculate_route_segment_capacities()

    expected_output = [42, 44, 46, 48, 50]
    assert expected_output == mock_route.segment_capacities


def test_calculate_pickup_stop_distances_to_nearest_segment(
    mock_route, mock_pickup_stops, mock_route_segments
):
    mock_route.route_segments = mock_route_segments.copy()
    mock_route.pickup_stops = mock_pickup_stops.copy()

    output = mock_route.calculate_pickup_stop_distances_to_nearest_segment()
    expected_output = np.array([[2, 4], [5, 4], [1, 4]])

    np.testing.assert_equal(output, expected_output)


@mock.patch(
    "assignment.routes.Route.calculate_pickup_stop_distances_to_nearest_segment"
)
def test_add_pickup_stop_to_route(
    mock_distances, mock_route, mock_pickup_stops, mock_planned_delivery_route
):
    mock_pickup_stops[2].size = 5
    mock_distances.return_value = np.array([[2, 4], [5, 4], [1, 4]])
    mock_route.pickup_stops = mock_pickup_stops
    mock_route.segment_capacities = [0, 1, 2, 3, 4]
    mock_route.planned_delivery_route = mock_planned_delivery_route.copy()

    mock_route.add_pickup_stop_to_route()

    assert mock_route.chosen_pickup_stop.get_location() == (2, 4)
    assert mock_route.final_route[4].get_location() == (2, 4)
