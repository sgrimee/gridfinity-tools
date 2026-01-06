#!/usr/bin/env python3
"""Generate drawer spacers and baseplate for a 330mm x 340mm drawer.

This script creates Gridfinity drawer spacers and a matching baseplate tailored
to fit a drawer with specified dimensions. The GridfinityDrawerSpacer library
automatically calculates the optimal baseplate size and spacer dimensions.

Output:
    - drawer_WxD_spacer_half_set.stl - Spacers for 3D printing (print twice)
    - drawer_WxD_spacer_full_set.step - Full assembly reference
    - drawer_WxD_baseplate_UxU.stl - Baseplate for 3D printing

Usage:
    python scripts/generate_drawer_spacer.py
"""

from pathlib import Path

from cqgridfinity import GridfinityBaseplate, GridfinityDrawerSpacer

# Gridfinity base unit constant
GRIDFINITY_UNIT = 42  # 1 Gridfinity square = 42mm

# Bambu Lab X1C build volume (in mm)
MAX_PRINT_WIDTH = 256
MAX_PRINT_DEPTH = 256


def calculate_baseplate_split(total_units: int, max_dimension: int) -> list[int]:
    """Calculate how to split baseplate units to fit within max print dimension.

    Args:
        total_units: Total number of Gridfinity units needed
        max_dimension: Maximum print dimension in mm

    Returns:
        List of unit counts for each piece (e.g., [4, 3] means two pieces)
    """
    total_mm = total_units * GRIDFINITY_UNIT

    # If it fits, return single piece
    if total_mm <= max_dimension:
        return [total_units]

    # Calculate minimum number of pieces needed
    num_pieces = (total_mm + max_dimension - 1) // max_dimension

    # Distribute units as evenly as possible
    base_units = total_units // num_pieces
    extra_units = total_units % num_pieces

    # Create list of pieces, distributing extra units to first pieces
    pieces = []
    for i in range(num_pieces):
        units = base_units + (1 if i < extra_units else 0)
        pieces.append(units)

    return pieces


def main() -> None:
    """Generate drawer spacers and baseplate for specified drawer dimensions."""
    # Drawer dimensions in millimeters
    drawer_width = 330.0
    drawer_depth = 340.0

    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Gridfinity Drawer Spacer & Baseplate Generator")
    print("=" * 60)
    print(f"Drawer: {drawer_width} mm x {drawer_depth} mm")
    print()

    # Create drawer spacer - library calculates optimal baseplate size
    print("Calculating optimal baseplate size and spacers...")
    spacer = GridfinityDrawerSpacer(
        drawer_width,
        drawer_depth,
        verbose=True,  # Show library's automatic calculations
        thickness=5.0,  # Standard baseplate thickness
        tolerance=1.0,  # 1mm tolerance for fit
        show_arrows=True,  # Show orientation arrows
        align_features=True,  # Add jigsaw interlocking features
    )

    # Calculate baseplate units from drawer dimensions (same logic library uses)
    baseplate_width_units = int(drawer_width // GRIDFINITY_UNIT)
    baseplate_depth_units = int(drawer_depth // GRIDFINITY_UNIT)

    # Calculate baseplate dimensions in mm
    baseplate_width_mm = baseplate_width_units * GRIDFINITY_UNIT
    baseplate_depth_mm = baseplate_depth_units * GRIDFINITY_UNIT

    print()
    print("-" * 60)
    print("Analyzing baseplate fit for printer...")
    print("-" * 60)
    print(
        f"Full baseplate: {baseplate_width_units}U × {baseplate_depth_units}U "
        f"({baseplate_width_mm}mm × {baseplate_depth_mm}mm)"
    )
    print(f"Printer build volume: {MAX_PRINT_WIDTH}mm × {MAX_PRINT_DEPTH}mm")

    # Calculate splits needed
    width_pieces = calculate_baseplate_split(baseplate_width_units, MAX_PRINT_WIDTH)
    depth_pieces = calculate_baseplate_split(baseplate_depth_units, MAX_PRINT_DEPTH)

    total_pieces = len(width_pieces) * len(depth_pieces)

    if total_pieces == 1:
        print("✓ Single baseplate will fit on printer bed")
    else:
        print(
            f"⚠️  Baseplate must be split into {total_pieces} pieces "
            f"({len(width_pieces)}×{len(depth_pieces)} grid)"
        )
        print(f"   Width split: {width_pieces} units per piece")
        print(f"   Depth split: {depth_pieces} units per piece")

    print()
    print("-" * 60)
    print("Generating spacer half set for 3D printing...")
    print("-" * 60)

    # Render half set (print this twice for a complete set)
    spacer.render_half_set()
    half_set_file = (
        output_dir / f"drawer_{int(drawer_width)}x{int(drawer_depth)}_spacer_half_set.stl"
    )
    spacer.save_stl_file(str(half_set_file))
    print(f"✓ Saved: {half_set_file}")
    print("  (Print this file twice to make a complete set)")

    print()
    print("-" * 60)
    print("Generating spacer full assembly for reference...")
    print("-" * 60)

    # Render full set with baseplate for visualization
    spacer.render_full_set(include_baseplate=True)
    full_set_file = (
        output_dir / f"drawer_{int(drawer_width)}x{int(drawer_depth)}_spacer_full_set.step"
    )
    spacer.save_step_file(str(full_set_file))
    print(f"✓ Saved: {full_set_file}")
    print("  (Reference file showing complete assembly)")

    print()
    print("-" * 60)
    print("Generating baseplate(s) for 3D printing...")
    print("-" * 60)

    # Collect unique piece types and count occurrences
    piece_types: dict[tuple[int, int], int] = {}
    for depth_units in depth_pieces:
        for width_units in width_pieces:
            key = (width_units, depth_units)
            piece_types[key] = piece_types.get(key, 0) + 1

    # Generate only unique pieces
    baseplate_files = []
    for (width_units, depth_units), count in piece_types.items():
        # Create baseplate piece
        baseplate = GridfinityBaseplate(
            width_units,
            depth_units,
            corner_screws=False,
        )

        # Generate filename
        if total_pieces == 1:
            baseplate_file = (
                output_dir
                / f"drawer_{int(drawer_width)}x{int(drawer_depth)}_baseplate_{baseplate_width_units}x{baseplate_depth_units}.stl"
            )
        else:
            baseplate_file = (
                output_dir
                / f"drawer_{int(drawer_width)}x{int(drawer_depth)}_baseplate_{width_units}x{depth_units}.stl"
            )

        baseplate.save_stl_file(str(baseplate_file))
        baseplate_files.append((baseplate_file, count))

        print(f"✓ Saved: {baseplate_file.name}")
        print(
            f"  ({width_units}×{depth_units} Gridfinity units = "
            f"{width_units * GRIDFINITY_UNIT}mm × {depth_units * GRIDFINITY_UNIT}mm)"
        )
        if count > 1:
            print(f"  Print this piece {count} times")

    print()
    print("=" * 60)
    print("Done! Files saved to 'output/' directory")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"  1. Print '{half_set_file.name}' twice")
    if total_pieces == 1:
        print(f"  2. Print '{baseplate_files[0][0].name}' once")
    else:
        print(f"  2. Print baseplate pieces ({total_pieces} total pieces):")
        for bf, count in baseplate_files:
            if count == 1:
                print(f"     - {bf.name} (print once)")
            else:
                print(f"     - {bf.name} (print {count} times)")
    print("  3. Assemble spacers around the baseplate")
    print("  4. Place assembled set in your drawer")
    print()


if __name__ == "__main__":
    main()
