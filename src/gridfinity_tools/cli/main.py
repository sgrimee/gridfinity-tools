"""Main CLI entry point and command group."""

import click

from gridfinity_tools.cli.baseplate import baseplate_command
from gridfinity_tools.cli.drawer import drawer_command
from gridfinity_tools.cli.spacer import spacer_command


@click.group()
@click.version_option(version="0.1.0", prog_name="gridfinity-tools")
def cli() -> None:
    """Gridfinity Tools: Generate custom Gridfinity storage solutions.

    This tool helps you create drawer organizing systems with spacers and
    matching baseplates optimized for your specific drawer dimensions and
    printer constraints.
    """
    pass


# Add command groups
cli.add_command(drawer_command, name="drawer")
cli.add_command(baseplate_command, name="baseplate")
cli.add_command(spacer_command, name="spacer")


if __name__ == "__main__":
    cli()
