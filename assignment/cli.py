import click
import logging
import sys

from assignment import constants
from assignment.routes import Route


logger = logging.getLogger(__name__)


def _configure_logger() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        format=constants.LOGGER_FORMAT,
        level=logging.INFO,
    )


@click.group()
@click.option(
    "--n-deliveries",
    type=int,
    required=False,
    help="Specifies the numebr of delivery events to generate, defaults to 1000",
)
@click.option(
    "--n-pickups",
    type=int,
    required=False,
    help="Specifies the numebr of pickup events to generate, defaults to 100",
)
@click.pass_context
def cli(ctx, n_deliveries: int = 1000, n_pickups: int = 100) -> None:
    _configure_logger()
    ctx.ensure_object(dict)

    ctx.obj["n_deliveries"] = n_deliveries
    ctx.obj["n_pickups"] = n_pickups


@cli.command()
@click.pass_context
def run_assignment(ctx):
    route = Route(n_deliveries=ctx.obj["n_deliveries"], n_pickups=ctx.obj["n_pickups"])

    route.run()


if __name__ == "__main__":
    cli(obj={})
