"""Drawer command for complete drawer solutions."""

from pathlib import Path

import click

from gridfinity_tools.core.drawer_generator import DrawerGenerator
from gridfinity_tools.core.printer import PrinterConfig
from gridfinity_tools.utils.units import parse_dimension


@click.command(name="drawer")
@click.argument("width", type=str)
@click.argument("depth", type=str)
@click.option(
    "--printer",
    "-p",
    type=click.Choice(["bambu-x1c", "bambu-p1p", "prusa-mk4", "prusa-mini", "ender3"]),
    default="bambu-x1c",
    help="Printer model (default: bambu-x1c)",
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
    "--corner-screws",
    is_flag=True,
    default=False,
    help="Add corner mounting screws to baseplate",
)
@click.option(
    "--no-arrows",
    is_flag=True,
    default=False,
    help="Disable orientation arrows on spacers",
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
def drawer_command(
    width: str,
    depth: str,
    printer: str,
    tolerance: float,
    thickness: float,
    chamfer: float,
    corner_screws: bool,
    no_arrows: bool,
    no_align: bool,
    output: str,
) -> None:
    """Generate a complete drawer solution with spacers and baseplate(s).

    This command creates a complete organizing system for a custom drawer:
    - Spacers optimized for the drawer dimensions
    - Baseplate(s) split to fit your printer's build volume

    Examples:

        Generate for 330×340mm drawer with Bambu X1C:
        $ gridfinity-tools drawer 330 340

        Generate for IKEA ALEX drawer (11.5×20.5 inches):
        $ gridfinity-tools drawer 11.5in 20.5in

        Generate with custom tolerance and corner screws:
        $ gridfinity-tools drawer 330 340 -t 0.5 --corner-screws
    """
    try:
        # Parse dimensions
        width_mm = parse_dimension(width)
        depth_mm = parse_dimension(depth)

        click.echo(f"📦 Drawer dimensions: {width_mm:.1f} × {depth_mm:.1f} mm")

        # Load printer configuration
        printer_config = PrinterConfig.from_preset(printer)
        click.echo(f"🖨️  Printer: {printer_config}")

        # Create drawer generator
        gen = DrawerGenerator(
            width_mm=width_mm,
            depth_mm=depth_mm,
            printer_config=printer_config,
            tolerance_mm=tolerance,
            spacer_thickness_mm=thickness,
            chamfer_mm=chamfer,
            corner_screws=corner_screws,
            show_arrows=not no_arrows,
            align_features=not no_align,
        )

        # Get solution info
        solution = gen.get_solution()
        layout = solution.baseplate_layout

        click.echo(
            f"📐 Baseplate dimensions: {solution.baseplate_width_units}×"
            f"{solution.baseplate_depth_units} units "
            f"({solution.baseplate_width_units * 42}×"
            f"{solution.baseplate_depth_units * 42} mm)"
        )

        if layout.is_split:
            click.echo(
                f"⚠️  Baseplate will be split into {layout.total_pieces} pieces"
                f" to fit printer constraints"
            )
        else:
            click.echo("✅ Baseplate fits on printer in one piece")

        # Create output directory
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate and save
        click.echo("\n🔧 Generating components...")
        results = gen.save_all(output_path)

        # Report results
        click.echo("\n✨ Generation complete!")
        click.echo("\nGenerated files:")
        for spacer_file in results["spacers"]:
            click.echo(f"  📄 {spacer_file.name}")
        for baseplate_file in results["baseplates"]:
            click.echo(f"  📄 {baseplate_file.name}")

        click.echo(f"\n💾 Output directory: {output_path.resolve()}")

    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise SystemExit(1) from None
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise SystemExit(1) from None
