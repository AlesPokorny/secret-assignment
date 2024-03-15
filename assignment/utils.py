import numpy as np
import logging


logger = logging.getLogger(__name__)


def generate_stops(
    n: int = 1000,
    min_coordinate: int = 1,
    max_coordinate: int = 1000,
    min_size: int = 1,
    max_size: int = 10,
    seed: int = 42,
) -> np.ndarray:
    """Generates stops location including their size, making sure there are no two stop

    Args:
        n (int, optional): Number of stops to generate. Defaults to 1000.
        min_coordinate (int, optional): Minimum X and Y coordinate possible, 0 0 would be the depot.
        Defaults to 1.

        max_coordinate (int, optional): Maximum X and Y coordinate po. Defaults to 1000.
        min_size (int, optional): Minimum package size. Defaults to 1.
        max_size (int, optional): Maxixmum package size. Defaults to 10.
        seed (int, optional): Le seed. Defaults to 42.

    Returns:
        np.ndarary: Stops per row with [x, y, size]
    """

    if (max_coordinate - min_coordinate) ** 2 < n:
        raise ValueError(f"Cannot generate {n} distinct stops in such a small plane")

    random_state = np.random.RandomState(seed)
    random_stops = random_state.randint(
        low=min_coordinate, high=max_coordinate, size=(n, 2)
    )
    random_sizes = random_state.random_sample(size=(1, n)) * max_size + min_size

    unique_stops = np.unique(random_stops, axis=0)
    n_missing_stops = n - len(unique_stops)

    while n_missing_stops > 0:
        new_stop = random_state.randint(
            low=min_coordinate, high=max_coordinate, size=(1, 2)
        )
        stop_exists = any(np.array_equal(stop, new_stop[0]) for stop in unique_stops)
        if not stop_exists:
            unique_stops = np.concatenate([unique_stops, new_stop])
            n_missing_stops -= 1

    stops_with_sizes_transposed = np.concatenate([unique_stops.T, random_sizes])
    stops_with_sizes = stops_with_sizes_transposed.T

    return stops_with_sizes
