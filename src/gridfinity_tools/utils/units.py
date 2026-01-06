"""Unit conversion utilities."""

from gridfinity_tools.constants import MM_PER_INCH


def inches_to_mm(inches: float) -> float:
    """Convert inches to millimeters.

    Args:
        inches: Measurement in inches

    Returns:
        Measurement in millimeters

    Examples:
        >>> inches_to_mm(1.0)
        25.4
        >>> inches_to_mm(11.5)
        292.1
    """
    return inches * MM_PER_INCH


def mm_to_inches(mm: float) -> float:
    """Convert millimeters to inches.

    Args:
        mm: Measurement in millimeters

    Returns:
        Measurement in inches

    Examples:
        >>> mm_to_inches(25.4)
        1.0
        >>> mm_to_inches(292.1)
        11.5
    """
    return mm / MM_PER_INCH


def parse_dimension(dim_str: str) -> float:
    """Parse dimension string to millimeters.

    Supports plain numbers (assumed to be mm) and inch suffixes.

    Args:
        dim_str: Dimension string like "330", "11.5in", "20.5in"

    Returns:
        Dimension in millimeters

    Raises:
        ValueError: If dimension format is invalid or value is not positive

    Examples:
        >>> parse_dimension("330")
        330.0
        >>> parse_dimension("11.5in")
        292.1
        >>> parse_dimension("1.0in")
        25.4
    """
    dim_str = dim_str.strip().lower()

    # Handle inch suffix
    if dim_str.endswith("in"):
        try:
            inches = float(dim_str[:-2])
            if inches <= 0:
                raise ValueError(f"Dimension must be positive, got: {inches} inches")
            return inches_to_mm(inches)
        except ValueError as e:
            if "positive" in str(e):
                raise
            raise ValueError(f"Invalid inch dimension format: {dim_str}") from e

    # Handle plain number (millimeters)
    try:
        mm = float(dim_str)
        if mm <= 0:
            raise ValueError(f"Dimension must be positive, got: {mm} mm")
        return mm
    except ValueError as e:
        if "positive" in str(e):
            raise
        raise ValueError(f"Invalid dimension format: {dim_str}") from e
