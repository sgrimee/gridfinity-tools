"""Spacer command for standalone spacer generation."""

from pathlib import Path

import click

from gridfinity_tools.core.spacer_generator import SpacerGenerator
from gridfinity_tools.utils.units import parse_dimension


@click.command(name="spacer")
@click.argument("width", type=str)
@click.argument("depth", type=str)
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["half_set", "full_set", "full_assembly"]),
    default="half_set",
    help="Rendering mode (default: half_set - print twice for complete set)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["stl", "step"]),
    default="stl",
    help="Output file format (default: stl)",
)
@click.option(
    "--tolerance",
    "-t",
    type=float,
    default=1.0,
    help="Spacer tolerance in mm (default: 1.0)",
)
@click.option(
    "--thickness",
    type=float,
    default=5.0,
    help="Spacer thickness in mm (default: 5.0)",
)
@click.option(
    "--chamfer",
    type=float,
    default=1.0,
    help="Edge chamfer radius in mm (default: 1.0)",
)
@click.option(
    "--no-arrows",
    is_flag=True,
    default=False,
    help="Disable orientation arrows",
)
@click.option(
    "--no-align",
    is_flag=True,
    default=False,
    help="Disable jigsaw interlocking features",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="output",
    help="Output directory (default: output)",
)
def spacer_command(
    width: str,
    depth: str,
    mode: str,
    format: str,
    tolerance: float,
    thickness: float,
    chamfer: float,
    no_arrows: bool,
    no_align: bool,
    output: str,
) -> None:
    """Generate drawer spacer components.

    The spacer components are designed to divide drawers into sections
    for organizing items.

    Modes:
      - half_set: Single half-set (print twice for complete set)
      - full_set: Complete set of all spacers
      - full_assembly: Full assembly with baseplate reference

    Examples:

        Generate half-set for 330×340mm drawer:
        $ gridfinity-tools spacer 330 340

        Generate full set in STEP format:
        $ gridfinity-tools spacer 330 340 -m full_set -f step

        Generate for IKEA drawer with custom tolerance:
        $ gridfinity-tools spacer 11.5in 20.5in -t 0.5
    """
    try:
        # Parse dimensions
        width_mm = parse_dimension(width)
        depth_mm = parse_dimension(depth)

        click.echo(f"📦 Spacer dimensions: {width_mm:.1f} × {depth_mm:.1f} mm")

        # Create spacer generator
        gen = SpacerGenerator(
            width_mm=width_mm,
            depth_mm=depth_mm,
            thickness_mm=thickness,
            tolerance_mm=tolerance,
            chamfer_mm=chamfer,
            show_arrows=not no_arrows,
            align_features=not no_align,
        )

        # Create output directory
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate and save
        click.echo(f"🔧 Generating spacer ({mode}, {format.upper()})...")

        from gridfinity_tools.utils.naming import (
            generate_assembly_filename,
            generate_spacer_filename,
        )

        filename: str
        if format == "stl":
            filename = generate_spacer_filename(
                width_mm=width_mm,
                depth_mm=depth_mm,
                tolerance=tolerance,
                render_mode=mode,
                file_format="stl",
            )
            file_path = output_path / filename
            gen.save_stl(file_path, render_mode=mode)
        else:  # format == "step"
            filename = generate_assembly_filename(
                width_mm=width_mm,
                depth_mm=depth_mm,
                tolerance=tolerance,
                file_format="step",
            )
            file_path = output_path / filename
            gen.save_step(file_path, render_mode=mode)

        click.echo("✨ Generation complete!")
        click.echo(f"📄 {filename}")

        if mode == "half_set":
            click.echo("ℹ️  Print this file twice to create a complete set")

        click.echo(f"💾 Output directory: {output_path.resolve()}")

    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise SystemExit(1) from None
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise SystemExit(1) from None
