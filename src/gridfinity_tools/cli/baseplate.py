"""Baseplate command for standalone baseplate generation."""

from pathlib import Path

import click

from gridfinity_tools.core.baseplate_generator import BaseplateGenerator
from gridfinity_tools.utils.naming import generate_baseplate_filename


@click.command(name="baseplate")
@click.argument("width", type=int)
@click.argument("depth", type=int)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["stl", "step", "svg"]),
    default="stl",
    help="Output file format (default: stl)",
)
@click.option(
    "--corner-screws",
    is_flag=True,
    default=False,
    help="Add corner mounting screws",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="output",
    help="Output directory (default: output)",
)
def baseplate_command(
    width: int,
    depth: int,
    format: str,
    corner_screws: bool,
    output: str,
) -> None:
    """Generate a Gridfinity baseplate with specified dimensions.

    Units are in Gridfinity units where 1 unit = 42mm.

    Examples:

        Generate 7×8 baseplate:
        $ gridfinity-tools baseplate 7 8

        Generate 10×10 baseplate with corner screws in STEP format:
        $ gridfinity-tools baseplate 10 10 --corner-screws -f step
    """
    try:
        click.echo(f"📐 Baseplate dimensions: {width}×{depth} units ({width * 42}×{depth * 42} mm)")

        # Create baseplate generator
        gen = BaseplateGenerator(
            units_width=width,
            units_depth=depth,
            corner_screws=corner_screws,
        )

        # Create output directory
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = generate_baseplate_filename(
            width_mm=width * 42,
            depth_mm=depth * 42,
            units_width=width,
            units_depth=depth,
            corner_screws=corner_screws,
            file_format=format,
        )
        file_path = output_path / filename

        # Generate and save
        click.echo(f"🔧 Generating baseplate ({format.upper()})...")

        if format == "stl":
            gen.save_stl(file_path)
        elif format == "step":
            gen.save_step(file_path)
        elif format == "svg":
            gen.save_svg(file_path)

        click.echo("✨ Generation complete!")
        click.echo(f"📄 {filename}")
        click.echo(f"💾 Output directory: {output_path.resolve()}")

    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise SystemExit(1) from None
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise SystemExit(1) from None
