"""Baseplate generation module."""

from pathlib import Path
from typing import Any

from cqgridfinity import GridfinityBaseplate

from gridfinity_tools.constants import (
    DEFAULT_COUNTERSINK_ANGLE,
    DEFAULT_COUNTERSINK_DIAM,
    DEFAULT_SCREW_HOLE_DIAM,
)
from gridfinity_tools.utils.validation import validate_baseplate_units


class BaseplateGenerator:
    """Generate Gridfinity baseplate components.

    This class wraps the GridfinityBaseplate from cqgridfinity library
    and provides an interface for generating baseplate components.
    """

    def __init__(
        self,
        units_width: int,
        units_depth: int,
        corner_screws: bool = False,
        screw_hole_diam_mm: float = DEFAULT_SCREW_HOLE_DIAM,
        countersink_diam_mm: float = DEFAULT_COUNTERSINK_DIAM,
        countersink_angle_deg: float = DEFAULT_COUNTERSINK_ANGLE,
        ext_depth_mm: float = 0.0,
        straight_bottom: bool = False,
    ) -> None:
        """Initialize baseplate generator.

        Args:
            units_width: Baseplate width in Gridfinity units
            units_depth: Baseplate depth in Gridfinity units
            corner_screws: Add corner mounting screw tabs (default: False)
            screw_hole_diam_mm: Screw hole diameter in mm (default: 5.0)
            countersink_diam_mm: Countersink diameter in mm (default: 10.0)
            countersink_angle_deg: Countersink angle in degrees (default: 82)
            ext_depth_mm: Extended depth under baseplate in mm (default: 0)
            straight_bottom: Add straight bottom (remove chamfer) (default: False)

        Raises:
            ValueError: If units are invalid
        """
        validate_baseplate_units(units_width, units_depth)

        self.units_width = units_width
        self.units_depth = units_depth
        self.corner_screws = corner_screws
        self.screw_hole_diam_mm = screw_hole_diam_mm
        self.countersink_diam_mm = countersink_diam_mm
        self.countersink_angle_deg = countersink_angle_deg
        self.ext_depth_mm = ext_depth_mm
        self.straight_bottom = straight_bottom

        # Create the underlying baseplate object
        self._baseplate: GridfinityBaseplate | None = None

    def _create_baseplate(self) -> GridfinityBaseplate:
        """Create the underlying GridfinityBaseplate object (lazy initialization).

        Returns:
            GridfinityBaseplate instance
        """
        if self._baseplate is None:
            self._baseplate = GridfinityBaseplate(
                self.units_width,
                self.units_depth,
                corner_screws=self.corner_screws,
                csk_hole=self.screw_hole_diam_mm,
                csk_diam=self.countersink_diam_mm,
                csk_angle=self.countersink_angle_deg,
                ext_depth=self.ext_depth_mm,
                straight_bottom=self.straight_bottom,
            )
        return self._baseplate

    def generate(self) -> Any:
        """Generate baseplate component.

        Returns:
            CadQuery object representing the baseplate
        """
        baseplate = self._create_baseplate()
        return baseplate.cq_obj

    def save_stl(self, output_path: str | Path) -> None:
        """Save baseplate to STL file.

        Args:
            output_path: Path to output STL file
        """
        baseplate = self._create_baseplate()
        baseplate.save_stl_file(str(output_path))

    def save_step(self, output_path: str | Path) -> None:
        """Save baseplate to STEP file.

        Args:
            output_path: Path to output STEP file
        """
        baseplate = self._create_baseplate()
        baseplate.save_step_file(str(output_path))

    def save_svg(self, output_path: str | Path) -> None:
        """Save baseplate to SVG file.

        Args:
            output_path: Path to output SVG file
        """
        baseplate = self._create_baseplate()
        baseplate.save_svg_file(str(output_path))
