"""Drawer solution generation module (orchestrator)."""

from pathlib import Path
from typing import Any, NamedTuple

from gridfinity_tools.core.baseplate_generator import BaseplateGenerator
from gridfinity_tools.core.printer import PrinterConfig
from gridfinity_tools.core.spacer_generator import SpacerGenerator
from gridfinity_tools.utils.naming import (
    generate_assembly_filename,
    generate_baseplate_filename,
    generate_spacer_filename,
)
from gridfinity_tools.utils.splitting import (
    calculate_baseplate_units,
    calculate_split_grid,
    calculate_total_pieces,
)
from gridfinity_tools.utils.validation import validate_drawer_dimensions


class BaseplateConfig(NamedTuple):
    """Configuration for a single baseplate piece."""

    units_width: int
    units_depth: int
    position_x: int
    position_y: int
    print_count: int


class BaseplateLayout(NamedTuple):
    """Layout information for baseplate splitting."""

    is_split: bool
    total_pieces: int
    width_units_list: list[int]
    depth_units_list: list[int]
    grid: list[list[BaseplateConfig]]


class DrawerSolution(NamedTuple):
    """Complete solution for a drawer setup."""

    drawer_width_mm: float
    drawer_depth_mm: float
    baseplate_width_units: int
    baseplate_depth_units: int
    baseplate_layout: BaseplateLayout
    spacer_config: dict[str, Any]
    baseplate_config: dict[str, Any]


class DrawerGenerator:
    """Generate complete drawer solutions with spacers and baseplates.

    This class orchestrates the creation of drawer organizing systems by:
    1. Calculating optimal baseplate dimensions from drawer size
    2. Determining if baseplate needs splitting for printer constraints
    3. Generating spacer components
    4. Generating baseplate components (one or more pieces)
    """

    def __init__(
        self,
        width_mm: float,
        depth_mm: float,
        printer_config: PrinterConfig,
        tolerance_mm: float = 1.0,
        corner_screws: bool = False,
        spacer_thickness_mm: float = 5.0,
        chamfer_mm: float = 1.0,
        show_arrows: bool = True,
        align_features: bool = True,
    ) -> None:
        """Initialize drawer generator.

        Args:
            width_mm: Drawer width in millimeters
            depth_mm: Drawer depth in millimeters
            printer_config: Printer configuration with build volume constraints
            tolerance_mm: Spacer tolerance in millimeters (default: 1.0)
            corner_screws: Add corner mounting screws to baseplate (default: False)
            spacer_thickness_mm: Spacer thickness in millimeters (default: 5.0)
            chamfer_mm: Edge chamfer radius in millimeters (default: 1.0)
            show_arrows: Show orientation arrows on spacers (default: True)
            align_features: Add jigsaw interlocking features (default: True)

        Raises:
            ValueError: If dimensions are invalid
        """
        validate_drawer_dimensions(width_mm, depth_mm)

        self.width_mm = width_mm
        self.depth_mm = depth_mm
        self.printer_config = printer_config
        self.tolerance_mm = tolerance_mm
        self.corner_screws = corner_screws
        self.spacer_thickness_mm = spacer_thickness_mm
        self.chamfer_mm = chamfer_mm
        self.show_arrows = show_arrows
        self.align_features = align_features

        # Calculate baseplate dimensions
        self.baseplate_width_units = calculate_baseplate_units(width_mm)
        self.baseplate_depth_units = calculate_baseplate_units(depth_mm)

        # Calculate baseplate layout (may be split)
        self._layout: BaseplateLayout | None = None
        self._solution: DrawerSolution | None = None

    def _calculate_layout(self) -> BaseplateLayout:
        """Calculate baseplate layout with splitting if needed.

        Returns:
            BaseplateLayout with piece information
        """
        width_units_list, depth_units_list = calculate_split_grid(
            self.baseplate_width_units,
            self.baseplate_depth_units,
            self.printer_config.max_width_mm,
            self.printer_config.max_depth_mm,
        )

        total = calculate_total_pieces(
            self.baseplate_width_units,
            self.baseplate_depth_units,
            self.printer_config.max_width_mm,
            self.printer_config.max_depth_mm,
        )

        is_split = total > 1

        # Build 2D grid of baseplate pieces
        grid = []
        for y, depth_units in enumerate(depth_units_list):
            row = []
            for x, width_units in enumerate(width_units_list):
                piece = BaseplateConfig(
                    units_width=width_units,
                    units_depth=depth_units,
                    position_x=x,
                    position_y=y,
                    print_count=1,  # Each piece prints once in grid
                )
                row.append(piece)
            grid.append(row)

        return BaseplateLayout(
            is_split=is_split,
            total_pieces=total,
            width_units_list=width_units_list,
            depth_units_list=depth_units_list,
            grid=grid,
        )

    def get_layout(self) -> BaseplateLayout:
        """Get baseplate layout (lazy initialization).

        Returns:
            BaseplateLayout with piece information
        """
        if self._layout is None:
            self._layout = self._calculate_layout()
        return self._layout

    def get_solution(self) -> DrawerSolution:
        """Get complete drawer solution (lazy initialization).

        Returns:
            DrawerSolution with all configuration information
        """
        if self._solution is None:
            layout = self.get_layout()

            self._solution = DrawerSolution(
                drawer_width_mm=self.width_mm,
                drawer_depth_mm=self.depth_mm,
                baseplate_width_units=self.baseplate_width_units,
                baseplate_depth_units=self.baseplate_depth_units,
                baseplate_layout=layout,
                spacer_config={
                    "width_mm": self.width_mm,
                    "depth_mm": self.depth_mm,
                    "thickness_mm": self.spacer_thickness_mm,
                    "tolerance_mm": self.tolerance_mm,
                    "chamfer_mm": self.chamfer_mm,
                    "show_arrows": self.show_arrows,
                    "align_features": self.align_features,
                },
                baseplate_config={
                    "corner_screws": self.corner_screws,
                },
            )

        return self._solution

    def generate_spacer(self, render_mode: str = "half_set") -> Any:
        """Generate spacer component.

        Args:
            render_mode: "half_set", "full_set", or "full_assembly" (default: "half_set")

        Returns:
            CadQuery object for the spacer
        """
        spacer_gen = SpacerGenerator(
            width_mm=self.width_mm,
            depth_mm=self.depth_mm,
            thickness_mm=self.spacer_thickness_mm,
            tolerance_mm=self.tolerance_mm,
            chamfer_mm=self.chamfer_mm,
            show_arrows=self.show_arrows,
            align_features=self.align_features,
        )

        if render_mode == "half_set":
            return spacer_gen.generate_half_set()
        elif render_mode == "full_set":
            return spacer_gen.generate_full_set()
        elif render_mode == "full_assembly":
            return spacer_gen.generate_full_assembly(include_baseplate=False)
        else:
            raise ValueError(f"Invalid render_mode: {render_mode}")

    def generate_baseplate_piece(self, piece_config: BaseplateConfig) -> Any:
        """Generate a single baseplate piece.

        Args:
            piece_config: Configuration for the piece

        Returns:
            CadQuery object for the baseplate piece
        """
        baseplate_gen = BaseplateGenerator(
            units_width=piece_config.units_width,
            units_depth=piece_config.units_depth,
            corner_screws=self.corner_screws,
        )
        return baseplate_gen.generate()

    def save_spacer_half_set(self, output_dir: str | Path) -> Path:
        """Save spacer half-set to STL file.

        The half-set should be printed twice to create a complete set.

        Args:
            output_dir: Output directory

        Returns:
            Path to saved file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        filename = generate_spacer_filename(
            width_mm=self.width_mm,
            depth_mm=self.depth_mm,
            tolerance=self.tolerance_mm,
            render_mode="half_set",
            file_format="stl",
        )
        file_path = output_path / filename

        spacer_gen = SpacerGenerator(
            width_mm=self.width_mm,
            depth_mm=self.depth_mm,
            thickness_mm=self.spacer_thickness_mm,
            tolerance_mm=self.tolerance_mm,
            chamfer_mm=self.chamfer_mm,
            show_arrows=self.show_arrows,
            align_features=self.align_features,
        )
        spacer_gen.save_stl(file_path, render_mode="half_set")

        return file_path

    def save_spacer_full_assembly(self, output_dir: str | Path) -> Path:
        """Save spacer full assembly to STEP file.

        Args:
            output_dir: Output directory

        Returns:
            Path to saved file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        filename = generate_assembly_filename(
            width_mm=self.width_mm,
            depth_mm=self.depth_mm,
            tolerance=self.tolerance_mm,
            file_format="step",
        )
        file_path = output_path / filename

        spacer_gen = SpacerGenerator(
            width_mm=self.width_mm,
            depth_mm=self.depth_mm,
            thickness_mm=self.spacer_thickness_mm,
            tolerance_mm=self.tolerance_mm,
            chamfer_mm=self.chamfer_mm,
            show_arrows=self.show_arrows,
            align_features=self.align_features,
        )
        spacer_gen.save_step(file_path, render_mode="full_assembly")

        return file_path

    def save_baseplate_pieces(self, output_dir: str | Path) -> list[Path]:
        """Save baseplate piece(s) to STL files.

        If baseplate needs to be split, generates multiple files with piece counts.

        Args:
            output_dir: Output directory

        Returns:
            List of paths to saved files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        layout = self.get_layout()
        saved_files = []

        # Generate each unique baseplate piece
        for row in layout.grid:
            for piece_config in row:
                # Generate filename for this piece
                filename = generate_baseplate_filename(
                    width_mm=self.width_mm,
                    depth_mm=self.depth_mm,
                    units_width=piece_config.units_width,
                    units_depth=piece_config.units_depth,
                    corner_screws=self.corner_screws,
                    file_format="stl",
                )
                file_path = output_path / filename

                # Generate and save the piece
                baseplate_gen = BaseplateGenerator(
                    units_width=piece_config.units_width,
                    units_depth=piece_config.units_depth,
                    corner_screws=self.corner_screws,
                )
                baseplate_gen.save_stl(file_path)

                saved_files.append(file_path)

        return saved_files

    def save_all(self, output_dir: str | Path) -> dict[str, list[Path]]:
        """Save all components (spacers and baseplates) to output directory.

        Args:
            output_dir: Output directory

        Returns:
            Dictionary with keys "spacers" and "baseplates" containing lists of saved paths
        """
        output_path = Path(output_dir)

        return {
            "spacers": [
                self.save_spacer_half_set(output_path),
                self.save_spacer_full_assembly(output_path),
            ],
            "baseplates": self.save_baseplate_pieces(output_path),
        }
