"""Drawer spacer generation module."""

from pathlib import Path
from typing import Any

from cqgridfinity import GridfinityDrawerSpacer

from gridfinity_tools.constants import (
    DEFAULT_ALIGN_FEATURES,
    DEFAULT_ALIGN_TOLERANCE,
    DEFAULT_MIN_MARGIN,
    DEFAULT_SHOW_ARROWS,
    DEFAULT_SPACER_CHAMFER,
    DEFAULT_SPACER_THICKNESS,
    DEFAULT_TOLERANCE,
)
from gridfinity_tools.utils.validation import validate_drawer_dimensions


class SpacerGenerator:
    """Generate drawer spacer components.

    This class wraps the GridfinityDrawerSpacer from cqgridfinity library
    and provides an interface for generating spacer components for custom drawers.
    """

    def __init__(
        self,
        width_mm: float,
        depth_mm: float,
        thickness_mm: float = DEFAULT_SPACER_THICKNESS,
        tolerance_mm: float = DEFAULT_TOLERANCE,
        chamfer_mm: float = DEFAULT_SPACER_CHAMFER,
        show_arrows: bool = DEFAULT_SHOW_ARROWS,
        align_features: bool = DEFAULT_ALIGN_FEATURES,
        align_tolerance_mm: float = DEFAULT_ALIGN_TOLERANCE,
        min_margin_mm: float = DEFAULT_MIN_MARGIN,
        verbose: bool = False,
    ) -> None:
        """Initialize spacer generator.

        Args:
            width_mm: Drawer width in millimeters
            depth_mm: Drawer depth in millimeters
            thickness_mm: Spacer thickness in millimeters (default: 5.0)
            tolerance_mm: Overall tolerance in millimeters (default: 1.0)
            chamfer_mm: Edge chamfer radius in millimeters (default: 1.0)
            show_arrows: Show orientation arrows (default: True)
            align_features: Add jigsaw interlocking features (default: True)
            align_tolerance_mm: Tolerance for interlocking joints (default: 0.15)
            min_margin_mm: Minimum spacer size to generate (default: 4.0)
            verbose: Enable verbose output (default: False)

        Raises:
            ValueError: If dimensions are invalid
        """
        validate_drawer_dimensions(width_mm, depth_mm)

        self.width_mm = width_mm
        self.depth_mm = depth_mm
        self.thickness_mm = thickness_mm
        self.tolerance_mm = tolerance_mm
        self.chamfer_mm = chamfer_mm
        self.show_arrows = show_arrows
        self.align_features = align_features
        self.align_tolerance_mm = align_tolerance_mm
        self.min_margin_mm = min_margin_mm
        self.verbose = verbose

        # Create the underlying spacer object
        self._spacer: GridfinityDrawerSpacer | None = None

    def _create_spacer(self) -> GridfinityDrawerSpacer:
        """Create the underlying GridfinityDrawerSpacer object (lazy initialization).

        Returns:
            GridfinityDrawerSpacer instance
        """
        if self._spacer is None:
            self._spacer = GridfinityDrawerSpacer(
                self.width_mm,
                self.depth_mm,
                thickness=self.thickness_mm,
                tolerance=self.tolerance_mm,
                chamf_rad=self.chamfer_mm,
                show_arrows=self.show_arrows,
                align_features=self.align_features,
                align_tol=self.align_tolerance_mm,
                min_margin=self.min_margin_mm,
                verbose=self.verbose,
            )
        return self._spacer

    def generate_half_set(self) -> Any:
        """Generate half set of spacer components for 3D printing.

        The half set should be printed twice to create a complete set.

        Returns:
            CadQuery object representing the half set
        """
        spacer = self._create_spacer()
        spacer.render_half_set()
        return spacer.cq_obj

    def generate_full_set(self) -> Any:
        """Generate full set of spacer components for reference.

        Returns:
            CadQuery object representing the full set
        """
        spacer = self._create_spacer()
        spacer.render_full_set()
        return spacer.cq_obj

    def generate_full_assembly(self, include_baseplate: bool = True) -> Any:
        """Generate full assembly with spacers and optional baseplate.

        Args:
            include_baseplate: Include baseplate in assembly (default: True)

        Returns:
            CadQuery object representing the full assembly
        """
        spacer = self._create_spacer()
        spacer.render_full_set(include_baseplate=include_baseplate)
        return spacer.cq_obj

    def save_stl(self, output_path: str | Path, render_mode: str = "half_set") -> None:
        """Save spacer components to STL file.

        Args:
            output_path: Path to output STL file
            render_mode: Rendering mode ("half_set" or "full_set") (default: "half_set")

        Raises:
            ValueError: If render_mode is invalid
        """
        if render_mode == "half_set":
            self.generate_half_set()
        elif render_mode == "full_set":
            self.generate_full_set()
        else:
            raise ValueError(f"Invalid render_mode: {render_mode}")

        spacer = self._create_spacer()
        spacer.save_stl_file(str(output_path))

    def save_step(self, output_path: str | Path, render_mode: str = "full_assembly") -> None:
        """Save spacer assembly to STEP file.

        Args:
            output_path: Path to output STEP file
            render_mode: Rendering mode ("full_set" or "full_assembly") (default: "full_assembly")

        Raises:
            ValueError: If render_mode is invalid
        """
        if render_mode == "full_assembly":
            self.generate_full_assembly()
        elif render_mode == "full_set":
            self.generate_full_set()
        else:
            raise ValueError(f"Invalid render_mode: {render_mode}")

        spacer = self._create_spacer()
        spacer.save_step_file(str(output_path))
