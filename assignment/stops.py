from typing import Tuple


class RouteStop:
    def __init__(self, x: int, y: int, size: float, is_pickup: bool, is_depot: bool):
        self.x = x
        self.y = y
        self.size = size
        self.is_pickup = is_pickup
        self.is_depot = is_depot

    def get_location(self) -> Tuple[int, int]:
        return self.x, self.y
