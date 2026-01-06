"""Filename generation utilities."""

from pathlib import Path


def generate_spacer_filename(
    width_mm: float,
    depth_mm: float,
    tolerance: float,
    render_mode: str,
    file_format: str,
) -> str:
    """Generate spacer filename with relevant parameters.

    Args:
        width_mm: Drawer width in millimeters
        depth_mm: Drawer depth in millimeters
        tolerance: Spacer tolerance in millimeters
        render_mode: Rendering mode (half_set, full_set, full_with_baseplate)
        file_format: File format (stl, step, svg)

    Returns:
        Filename string without path

    Examples:
        >>> generate_spacer_filename(330, 340, 1.0, "half_set", "stl")
        'drawer_330x340_spacer_half_set.stl'
        >>> generate_spacer_filename(330, 340, 0.5, "half_set", "stl")
        'drawer_330x340_tol0.5_spacer_half_set.stl'
    """
    width_int = int(width_mm)
    depth_int = int(depth_mm)

    # Build base filename
    filename = f"drawer_{width_int}x{depth_int}"

    # Add tolerance if not default (1.0)
    if tolerance != 1.0:
        filename += f"_tol{tolerance}"

    # Add render mode and format
    filename += f"_spacer_{render_mode}.{file_format}"

    return filename


def generate_baseplate_filename(
    width_mm: float,
    depth_mm: float,
    units_width: int,
    units_depth: int,
    corner_screws: bool,
    file_format: str,
) -> str:
    """Generate baseplate filename with relevant parameters.

    Args:
        width_mm: Drawer width in millimeters
        depth_mm: Drawer depth in millimeters
        units_width: Baseplate width in Gridfinity units
        units_depth: Baseplate depth in Gridfinity units
        corner_screws: Whether corner screws are included
        file_format: File format (stl, step, svg)

    Returns:
        Filename string without path

    Examples:
        >>> generate_baseplate_filename(330, 340, 7, 8, False, "stl")
        'drawer_330x340_baseplate_7x8.stl'
        >>> generate_baseplate_filename(330, 340, 7, 8, True, "stl")
        'drawer_330x340_screws_baseplate_7x8.stl'
    """
    width_int = int(width_mm)
    depth_int = int(depth_mm)

    # Build base filename
    filename = f"drawer_{width_int}x{depth_int}"

    # Add corner screws indicator if present
    if corner_screws:
        filename += "_screws"

    # Add baseplate dimensions and format
    filename += f"_baseplate_{units_width}x{units_depth}.{file_format}"

    return filename


def generate_assembly_filename(
    width_mm: float,
    depth_mm: float,
    tolerance: float,
    file_format: str,
) -> str:
    """Generate assembly filename with relevant parameters.

    Args:
        width_mm: Drawer width in millimeters
        depth_mm: Drawer depth in millimeters
        tolerance: Spacer tolerance in millimeters
        file_format: File format (stl, step, svg)

    Returns:
        Filename string without path

    Examples:
        >>> generate_assembly_filename(330, 340, 1.0, "step")
        'drawer_330x340_full_assembly.step'
        >>> generate_assembly_filename(330, 340, 0.5, "step")
        'drawer_330x340_tol0.5_full_assembly.step'
    """
    width_int = int(width_mm)
    depth_int = int(depth_mm)

    # Build base filename
    filename = f"drawer_{width_int}x{depth_int}"

    # Add tolerance if not default (1.0)
    if tolerance != 1.0:
        filename += f"_tol{tolerance}"

    # Add assembly and format
    filename += f"_full_assembly.{file_format}"

    return filename


def add_path_to_filename(filename: str, output_dir: Path | str) -> Path:
    """Combine filename with output directory path.

    Args:
        filename: Filename string
        output_dir: Output directory path (str or Path)

    Returns:
        Full Path object

    Examples:
        >>> add_path_to_filename("test.stl", "output")
        PosixPath('output/test.stl')
        >>> add_path_to_filename("test.stl", Path("output"))
        PosixPath('output/test.stl')
    """
    output_path = Path(output_dir)
    return output_path / filename
