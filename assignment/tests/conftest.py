import pytest
from typing import List, Tuple
from assignment.stops import RouteStop


@pytest.fixture
def mock_possible_deliveries() -> List[RouteStop]:
    coordinates = [
        (88, 373),
        (100, 872),
        (103, 436),
        (107, 72),
        (331, 459),
        (467, 215),
        (615, 122),
        (664, 131),
        (701, 21),
        (861, 271),
    ]
    sizes = [1.2, 10.6, 9.3, 3.1, 2.8, 3.7, 4.0, 6.2, 5.3, 3.9]
    possible_deliveries = [
        RouteStop(x=x, y=y, size=size, is_depot=False, is_pickup=False)
        for (x, y), size in zip(coordinates, sizes)
    ]
    return possible_deliveries


@pytest.fixture
def mock_chosen_deliveries() -> List[RouteStop]:
    coordinates = [(1, 2), (0, 2), (1, 3), (0, 1)]
    possible_deliveries = [
        RouteStop(x=x, y=y, size=2, is_depot=False, is_pickup=False)
        for x, y in coordinates
    ]
    return possible_deliveries


@pytest.fixture
def mock_pickup_stops() -> List[RouteStop]:
    coordinates = [(2, 4), (3, 4), (2, 3)]
    pickup_stops = [
        RouteStop(x=x, y=y, size=2, is_depot=False, is_pickup=True)
        for x, y in coordinates
    ]
    return pickup_stops


@pytest.fixture
def mock_route_segments() -> List[Tuple]:
    return [(0, 0, 0, 1), (0, 1, 0, 2), (0, 2, 1, 2), (1, 2, 1, 3), (1, 3, 0, 0)]


@pytest.fixture
def mock_planned_delivery_route() -> List[RouteStop]:
    coordinates = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (0, 0)]
    planned_delivery_route = [
        RouteStop(x=x, y=y, size=2, is_depot=False, is_pickup=False)
        for x, y in coordinates
    ]
    return planned_delivery_route
