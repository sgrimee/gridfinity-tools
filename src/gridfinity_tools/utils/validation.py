"""Input validation utilities."""

from gridfinity_tools.constants import GRIDFINITY_UNIT


def validate_positive(value: float, name: str) -> None:
    """Validate that a value is positive.

    Args:
        value: Value to validate
        name: Name of the parameter (for error messages)

    Raises:
        ValueError: If value is not positive

    Examples:
        >>> validate_positive(330.0, "width")
        >>> validate_positive(-10.0, "width")
        Traceback (most recent call last):
            ...
        ValueError: width must be positive, got -10.0
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_drawer_dimensions(width_mm: float, depth_mm: float) -> None:
    """Validate drawer dimensions.

    Args:
        width_mm: Drawer width in millimeters
        depth_mm: Drawer depth in millimeters

    Raises:
        ValueError: If dimensions are invalid

    Examples:
        >>> validate_drawer_dimensions(330.0, 340.0)
        >>> validate_drawer_dimensions(0.0, 340.0)
        Traceback (most recent call last):
            ...
        ValueError: drawer width must be positive, got 0.0
    """
    validate_positive(width_mm, "drawer width")
    validate_positive(depth_mm, "drawer depth")

    # Warn if drawer is too small to fit even 1 unit
    min_size = GRIDFINITY_UNIT
    if width_mm < min_size or depth_mm < min_size:
        raise ValueError(
            f"Drawer must be at least {min_size}mm in both dimensions "
            f"(got {width_mm}mm x {depth_mm}mm)"
        )


def validate_baseplate_units(units_width: int, units_depth: int) -> None:
    """Validate baseplate units.

    Args:
        units_width: Baseplate width in Gridfinity units
        units_depth: Baseplate depth in Gridfinity units

    Raises:
        ValueError: If units are invalid

    Examples:
        >>> validate_baseplate_units(7, 8)
        >>> validate_baseplate_units(0, 8)
        Traceback (most recent call last):
            ...
        ValueError: baseplate width must be at least 1 unit, got 0
    """
    if units_width < 1:
        raise ValueError(f"baseplate width must be at least 1 unit, got {units_width}")
    if units_depth < 1:
        raise ValueError(f"baseplate depth must be at least 1 unit, got {units_depth}")


def validate_tolerance(tolerance_mm: float) -> None:
    """Validate spacer tolerance value.

    Args:
        tolerance_mm: Tolerance in millimeters

    Raises:
        ValueError: If tolerance is invalid

    Examples:
        >>> validate_tolerance(1.0)
        >>> validate_tolerance(-0.5)
        Traceback (most recent call last):
            ...
        ValueError: tolerance must be positive, got -0.5
    """
    validate_positive(tolerance_mm, "tolerance")

    if tolerance_mm > 5.0:
        raise ValueError(f"tolerance should be reasonable (0.1-2.0mm), got {tolerance_mm}mm")


def validate_printer_dimensions(max_width_mm: float, max_depth_mm: float) -> None:
    """Validate printer build volume dimensions.

    Args:
        max_width_mm: Maximum printer width in millimeters
        max_depth_mm: Maximum printer depth in millimeters

    Raises:
        ValueError: If dimensions are invalid

    Examples:
        >>> validate_printer_dimensions(256.0, 256.0)
        >>> validate_printer_dimensions(100.0, 256.0)
        Traceback (most recent call last):
            ...
        ValueError: printer max_width must be at least 42mm, got 100.0mm
    """
    min_size = GRIDFINITY_UNIT  # Minimum to fit one unit
    if max_width_mm < min_size:
        raise ValueError(f"printer max_width must be at least {min_size}mm, got {max_width_mm}mm")
    if max_depth_mm < min_size:
        raise ValueError(f"printer max_depth must be at least {min_size}mm, got {max_depth_mm}mm")


def validate_file_format(file_format: str, valid_formats: set[str]) -> None:
    """Validate file format is supported.

    Args:
        file_format: File format to validate
        valid_formats: Set of valid format strings

    Raises:
        ValueError: If format is not supported

    Examples:
        >>> validate_file_format("stl", {"stl", "step", "svg"})
        >>> validate_file_format("obj", {"stl", "step", "svg"})
        Traceback (most recent call last):
            ...
        ValueError: unsupported file format 'obj', must be one of: ...
    """
    if file_format.lower() not in valid_formats:
        valid_str = ", ".join(sorted(valid_formats))
        raise ValueError(f"unsupported file format '{file_format}', must be one of: {valid_str}")
