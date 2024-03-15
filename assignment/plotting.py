import matplotlib.pyplot as plt


def plot_route(route, extra_stops_to_plot=[]):
    plt.figure(figsize=(20, 14))

    if len(extra_stops_to_plot) > 0:
        for stop in extra_stops_to_plot:
            x, y = stop.get_location()
            plt.scatter(x, y, s=30, c="gray")

    prev_x = None
    prev_y = None
    for stop in route:
        x, y = stop.get_location()
        if stop.is_depot:
            color = "green"
        elif stop.is_pickup:
            color = "red"
        else:
            color = "blue"
        plt.scatter(x, y, s=30, c=color)
        if prev_x is not None:
            # plt.plot([prev_x, x], [prev_y, y], color="black")
            plt.arrow(
                prev_x,
                prev_y,
                x - prev_x,
                y - prev_y,
                color="black",
                length_includes_head=True,
                head_width=5,
            )
        prev_x = x
        prev_y = y

    plt.show()
