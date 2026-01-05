#!/usr/bin/env python3
"""Generate drawer spacers for a 220mm x 425mm drawer.

This script creates Gridfinity drawer spacers tailored to fit a drawer
with dimensions 220mm (width) x 425mm (depth). The spacers help secure
Gridfinity baseplates snugly inside the drawer.

The script generates a half set of spacers which should be printed twice
to create a complete set for one drawer.

Output:
    - drawer_220x425_spacer_half_set.stl - STL file for 3D printing
    - drawer_220x425_spacer_full_set.step - STEP file showing full assembly

Usage:
    python scripts/generate_drawer_spacer.py
"""

from pathlib import Path

from cqgridfinity import GridfinityDrawerSpacer


def main() -> None:
    """Generate drawer spacers for 220mm x 425mm drawer."""
    # Drawer dimensions in millimeters
    drawer_width = 220.0
    drawer_depth = 425.0

    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Gridfinity Drawer Spacer Generator")
    print("=" * 60)
    print(f"Drawer dimensions: {drawer_width} mm x {drawer_depth} mm")
    print()

    # Create drawer spacer with verbose output to show calculations
    spacer = GridfinityDrawerSpacer(
        drawer_width,
        drawer_depth,
        verbose=True,
        thickness=5.0,  # Standard baseplate thickness
        tolerance=0.5,  # 0.5mm tolerance for snug fit
        show_arrows=True,  # Show orientation arrows
        align_features=True,  # Add jigsaw interlocking features
    )

    print()
    print("-" * 60)
    print("Generating half set for 3D printing...")
    print("-" * 60)

    # Render half set (print this twice for a complete set)
    spacer.render_half_set()
    half_set_file = output_dir / "drawer_220x425_spacer_half_set.stl"
    spacer.save_stl_file(str(half_set_file))
    print(f"✓ Saved half set: {half_set_file}")
    print("  (Print this file twice to make a complete set)")

    print()
    print("-" * 60)
    print("Generating full assembly for reference...")
    print("-" * 60)

    # Render full set with baseplate for visualization
    spacer.render_full_set(include_baseplate=True)
    full_set_file = output_dir / "drawer_220x425_spacer_full_set.step"
    spacer.save_step_file(str(full_set_file))
    print(f"✓ Saved full assembly: {full_set_file}")
    print("  (This shows the complete layout - for reference only)")

    print()
    print("=" * 60)
    print("Done! Files saved to 'output/' directory")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Print 'drawer_220x425_spacer_half_set.stl' twice")
    print("  2. Assemble spacers around your Gridfinity baseplate")
    print("  3. Place assembled set in your drawer")
    print()


if __name__ == "__main__":
    main()
