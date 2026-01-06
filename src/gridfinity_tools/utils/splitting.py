"""Baseplate splitting and calculation utilities."""

from gridfinity_tools.constants import GRIDFINITY_UNIT


def calculate_baseplate_units(drawer_mm: float) -> int:
    """Calculate optimal Gridfinity baseplate units for a drawer dimension.

    Args:
        drawer_mm: Drawer dimension in millimeters

    Returns:
        Number of Gridfinity units that fit in the drawer

    Examples:
        >>> calculate_baseplate_units(330.0)
        7
        >>> calculate_baseplate_units(340.0)
        8
        >>> calculate_baseplate_units(292.1)
        6
    """
    return int(drawer_mm // GRIDFINITY_UNIT)


def calculate_baseplate_split(total_units: int, max_dimension_mm: float | int) -> list[int]:
    """Calculate how to split baseplate units to fit within max print dimension.

    Splits a baseplate into the minimum number of pieces needed to fit within
    the printer's maximum dimension. Units are distributed as evenly as possible.

    Args:
        total_units: Total number of Gridfinity units needed
        max_dimension_mm: Maximum printer dimension in millimeters

    Returns:
        List of unit counts for each piece (e.g., [4, 3] means two pieces of 4 and 3 units)

    Raises:
        ValueError: If total_units is less than 1 or max_dimension_mm is less than GRIDFINITY_UNIT

    Examples:
        >>> calculate_baseplate_split(7, 256)
        [7]
        >>> calculate_baseplate_split(13, 256)
        [7, 6]
        >>> calculate_baseplate_split(8, 200)
        [5, 3]
    """
    if total_units < 1:
        raise ValueError(f"total_units must be at least 1, got {total_units}")
    if max_dimension_mm < GRIDFINITY_UNIT:
        raise ValueError(
            f"max_dimension_mm must be at least {GRIDFINITY_UNIT}mm, got {max_dimension_mm}mm"
        )

    total_mm = total_units * GRIDFINITY_UNIT
    max_dim_mm = int(max_dimension_mm)

    # If it fits in one piece, return single piece
    if total_mm <= max_dim_mm:
        return [total_units]

    # Calculate minimum number of pieces needed
    num_pieces = (total_mm + max_dim_mm - 1) // max_dim_mm

    # Distribute units as evenly as possible
    base_units = total_units // num_pieces
    extra_units = total_units % num_pieces

    # Create list of pieces, distributing extra units to first pieces
    pieces = []
    for i in range(num_pieces):
        units = base_units + (1 if i < extra_units else 0)
        pieces.append(units)

    return pieces


def calculate_split_grid(
    width_units: int,
    depth_units: int,
    max_width_mm: float | int,
    max_depth_mm: float | int,
) -> tuple[list[int], list[int]]:
    """Calculate 2D grid split for baseplate dimensions.

    Calculates how to split a baseplate in both width and depth dimensions
    to fit within printer constraints.

    Args:
        width_units: Baseplate width in Gridfinity units
        depth_units: Baseplate depth in Gridfinity units
        max_width_mm: Maximum printer width in millimeters
        max_depth_mm: Maximum printer depth in millimeters

    Returns:
        Tuple of (width_pieces, depth_pieces) lists

    Examples:
        >>> calculate_split_grid(7, 8, 256, 256)
        ([7], [8])
        >>> calculate_split_grid(13, 11, 256, 256)
        ([7, 6], [6, 5])
    """
    width_pieces = calculate_baseplate_split(width_units, max_width_mm)
    depth_pieces = calculate_baseplate_split(depth_units, max_depth_mm)
    return width_pieces, depth_pieces


def calculate_total_pieces(
    width_units: int,
    depth_units: int,
    max_width_mm: float | int,
    max_depth_mm: float | int,
) -> int:
    """Calculate total number of baseplate pieces needed.

    Args:
        width_units: Baseplate width in Gridfinity units
        depth_units: Baseplate depth in Gridfinity units
        max_width_mm: Maximum printer width in millimeters
        max_depth_mm: Maximum printer depth in millimeters

    Returns:
        Total number of pieces in 2D grid

    Examples:
        >>> calculate_total_pieces(7, 8, 256, 256)
        1
        >>> calculate_total_pieces(13, 11, 256, 256)
        4
    """
    width_pieces, depth_pieces = calculate_split_grid(
        width_units, depth_units, max_width_mm, max_depth_mm
    )
    return len(width_pieces) * len(depth_pieces)
