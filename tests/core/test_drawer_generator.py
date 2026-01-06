"""Tests for drawer generator."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gridfinity_tools.core.drawer_generator import (
    BaseplateConfig,
    BaseplateLayout,
    DrawerGenerator,
)
from gridfinity_tools.core.printer import PrinterConfig


class TestDrawerGeneratorInitialization:
    """Tests for DrawerGenerator initialization."""

    def test_basic_initialization(self) -> None:
        """Test basic drawer generator initialization."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        assert gen.width_mm == 330.0
        assert gen.depth_mm == 340.0
        assert gen.tolerance_mm == 1.0

    def test_initialization_with_custom_tolerance(self) -> None:
        """Test initialization with custom tolerance."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer, tolerance_mm=0.5)
        assert gen.tolerance_mm == 0.5

    def test_initialization_with_custom_thickness(self) -> None:
        """Test initialization with custom spacer thickness."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer, spacer_thickness_mm=3.0)
        assert gen.spacer_thickness_mm == 3.0

    def test_initialization_with_corner_screws(self) -> None:
        """Test initialization with corner screws enabled."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer, corner_screws=True)
        assert gen.corner_screws is True

    def test_initialization_with_all_defaults(self) -> None:
        """Test all defaults are set correctly."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        assert gen.spacer_thickness_mm == 5.0
        assert gen.tolerance_mm == 1.0
        assert gen.chamfer_mm == 1.0
        assert gen.show_arrows is True
        assert gen.align_features is True
        assert gen.corner_screws is False

    def test_initialization_with_custom_options(self) -> None:
        """Test initialization with multiple custom options."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(
            330.0,
            340.0,
            printer,
            tolerance_mm=0.75,
            corner_screws=True,
            spacer_thickness_mm=4.0,
            chamfer_mm=0.5,
            show_arrows=False,
            align_features=False,
        )
        assert gen.tolerance_mm == 0.75
        assert gen.corner_screws is True
        assert gen.spacer_thickness_mm == 4.0
        assert gen.chamfer_mm == 0.5
        assert gen.show_arrows is False
        assert gen.align_features is False

    def test_invalid_width_dimension(self) -> None:
        """Test invalid width dimension fails."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        with pytest.raises(ValueError):
            DrawerGenerator(0.0, 340.0, printer)

    def test_invalid_depth_dimension(self) -> None:
        """Test invalid depth dimension fails."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        with pytest.raises(ValueError):
            DrawerGenerator(330.0, 0.0, printer)

    def test_too_small_dimensions(self) -> None:
        """Test dimensions smaller than 42mm fail."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        with pytest.raises(ValueError):
            DrawerGenerator(30.0, 340.0, printer)

    def test_fractional_dimensions(self) -> None:
        """Test fractional dimensions are accepted."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(292.1, 520.7, printer)
        assert gen.width_mm == 292.1
        assert gen.depth_mm == 520.7

    def test_baseplate_units_calculated_on_init(self) -> None:
        """Test baseplate units are calculated during initialization."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        # 330mm / 42mm per unit = 7 units
        # 340mm / 42mm per unit = 8 units
        assert gen.baseplate_width_units == 7
        assert gen.baseplate_depth_units == 8


class TestDrawerGeneratorLayout:
    """Tests for baseplate layout calculation."""

    def test_layout_no_split_small_drawer(self) -> None:
        """Test layout for small drawer that fits in one piece."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(200.0, 200.0, printer)
        layout = gen.get_layout()

        assert layout.is_split is False
        assert layout.total_pieces == 1
        assert len(layout.width_units_list) == 1
        assert len(layout.depth_units_list) == 1

    def test_layout_grid_structure(self) -> None:
        """Test layout grid structure is correct."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        layout = gen.get_layout()

        # Grid should be 2D array
        assert len(layout.grid) > 0
        assert all(isinstance(row, list) for row in layout.grid)
        assert all(isinstance(piece, BaseplateConfig) for row in layout.grid for piece in row)

    def test_layout_lazy_initialization(self) -> None:
        """Test layout is lazily initialized."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        assert gen._layout is None
        layout1 = gen.get_layout()
        assert gen._layout is not None
        layout2 = gen.get_layout()
        assert layout1 is layout2  # Same object, not recreated

    def test_layout_pieces_have_coordinates(self) -> None:
        """Test layout pieces have position coordinates."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        layout = gen.get_layout()

        for y, row in enumerate(layout.grid):
            for x, piece in enumerate(row):
                assert piece.position_x == x
                assert piece.position_y == y

    def test_layout_with_custom_printer(self) -> None:
        """Test layout with custom printer constraints."""
        printer = PrinterConfig.from_custom("Custom", 200, 200)
        gen = DrawerGenerator(400.0, 400.0, printer)
        layout = gen.get_layout()

        # Should be split due to small printer
        assert layout.is_split is True
        assert layout.total_pieces > 1


class TestDrawerGeneratorSolution:
    """Tests for drawer solution generation."""

    def test_solution_lazy_initialization(self) -> None:
        """Test solution is lazily initialized."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        assert gen._solution is None
        solution1 = gen.get_solution()
        assert gen._solution is not None
        solution2 = gen.get_solution()
        assert solution1 is solution2  # Same object, not recreated

    def test_solution_contains_drawer_dimensions(self) -> None:
        """Test solution contains drawer dimensions."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        solution = gen.get_solution()

        assert solution.drawer_width_mm == 330.0
        assert solution.drawer_depth_mm == 340.0

    def test_solution_contains_baseplate_units(self) -> None:
        """Test solution contains baseplate units."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        solution = gen.get_solution()

        assert solution.baseplate_width_units == 7
        assert solution.baseplate_depth_units == 8

    def test_solution_contains_layout(self) -> None:
        """Test solution contains baseplate layout."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        solution = gen.get_solution()

        assert isinstance(solution.baseplate_layout, BaseplateLayout)
        assert solution.baseplate_layout.total_pieces > 0

    def test_solution_contains_spacer_config(self) -> None:
        """Test solution contains spacer configuration."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer, tolerance_mm=0.5)
        solution = gen.get_solution()

        assert solution.spacer_config["width_mm"] == 330.0
        assert solution.spacer_config["depth_mm"] == 340.0
        assert solution.spacer_config["tolerance_mm"] == 0.5
        assert solution.spacer_config["thickness_mm"] == 5.0

    def test_solution_contains_baseplate_config(self) -> None:
        """Test solution contains baseplate configuration."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer, corner_screws=True)
        solution = gen.get_solution()

        assert solution.baseplate_config["corner_screws"] is True


class TestDrawerGeneratorGeneration:
    """Tests for spacer and baseplate generation methods."""

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_generate_spacer_half_set(self, mock_spacer_class: MagicMock) -> None:
        """Test generating spacer half set."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        gen.generate_spacer(render_mode="half_set")

        mock_spacer_class.assert_called_once()
        mock_instance.generate_half_set.assert_called_once()

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_generate_spacer_full_set(self, mock_spacer_class: MagicMock) -> None:
        """Test generating spacer full set."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        gen.generate_spacer(render_mode="full_set")

        mock_instance.generate_full_set.assert_called_once()

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_generate_spacer_full_assembly(self, mock_spacer_class: MagicMock) -> None:
        """Test generating spacer full assembly."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        gen.generate_spacer(render_mode="full_assembly")

        mock_instance.generate_full_assembly.assert_called_once_with(include_baseplate=False)

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_generate_spacer_invalid_mode(self, mock_spacer_class: MagicMock) -> None:
        """Test generating spacer with invalid mode fails."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)

        with pytest.raises(ValueError, match="Invalid render_mode"):
            gen.generate_spacer(render_mode="invalid")

    @patch("gridfinity_tools.core.drawer_generator.BaseplateGenerator")
    def test_generate_baseplate_piece(self, mock_baseplate_class: MagicMock) -> None:
        """Test generating a single baseplate piece."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)

        piece_config = BaseplateConfig(
            units_width=7, units_depth=8, position_x=0, position_y=0, print_count=1
        )
        gen.generate_baseplate_piece(piece_config)

        mock_baseplate_class.assert_called_once()
        mock_instance.generate.assert_called_once()


class TestDrawerGeneratorSave:
    """Tests for saving generated components to files."""

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_save_spacer_half_set(self, mock_spacer_class: MagicMock, tmp_path: Path) -> None:
        """Test saving spacer half set."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        result = gen.save_spacer_half_set(tmp_path)

        assert result.parent == tmp_path
        assert "330x340" in result.name
        assert "spacer" in result.name
        assert result.suffix == ".stl"
        mock_instance.save_stl.assert_called_once()

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_save_spacer_full_assembly(self, mock_spacer_class: MagicMock, tmp_path: Path) -> None:
        """Test saving spacer full assembly."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        result = gen.save_spacer_full_assembly(tmp_path)

        assert result.parent == tmp_path
        assert "330x340" in result.name
        assert "full_assembly" in result.name
        assert result.suffix == ".step"
        mock_instance.save_step.assert_called_once()

    @patch("gridfinity_tools.core.drawer_generator.BaseplateGenerator")
    def test_save_baseplate_pieces(self, mock_baseplate_class: MagicMock, tmp_path: Path) -> None:
        """Test saving baseplate pieces."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        results = gen.save_baseplate_pieces(tmp_path)

        assert len(results) > 0
        assert all(result.parent == tmp_path for result in results)
        assert all("baseplate" in result.name for result in results)
        assert all(result.suffix == ".stl" for result in results)

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    @patch("gridfinity_tools.core.drawer_generator.BaseplateGenerator")
    def test_save_all(
        self, mock_baseplate_class: MagicMock, mock_spacer_class: MagicMock, tmp_path: Path
    ) -> None:
        """Test saving all components."""
        mock_spacer_instance = MagicMock()
        mock_baseplate_instance = MagicMock()
        mock_spacer_class.return_value = mock_spacer_instance
        mock_baseplate_class.return_value = mock_baseplate_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)
        results = gen.save_all(tmp_path)

        assert "spacers" in results
        assert "baseplates" in results
        assert len(results["spacers"]) == 2  # half_set and full_assembly
        assert len(results["baseplates"]) > 0

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    @patch("gridfinity_tools.core.drawer_generator.BaseplateGenerator")
    def test_save_creates_output_directory(
        self, mock_baseplate_class: MagicMock, mock_spacer_class: MagicMock, tmp_path: Path
    ) -> None:
        """Test that save methods create output directory if it doesn't exist."""
        mock_spacer_instance = MagicMock()
        mock_baseplate_instance = MagicMock()
        mock_spacer_class.return_value = mock_spacer_instance
        mock_baseplate_class.return_value = mock_baseplate_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer)

        nested_output = tmp_path / "output" / "subfolder"
        gen.save_spacer_half_set(nested_output)

        assert nested_output.exists()


class TestDrawerGeneratorConfiguration:
    """Tests for configuration propagation to generators."""

    @patch("gridfinity_tools.core.drawer_generator.SpacerGenerator")
    def test_spacer_config_propagation(self, mock_spacer_class: MagicMock) -> None:
        """Test spacer configuration is propagated correctly."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(
            330.0,
            340.0,
            printer,
            tolerance_mm=0.5,
            spacer_thickness_mm=3.0,
            chamfer_mm=0.8,
            show_arrows=False,
            align_features=False,
        )
        gen.generate_spacer()

        # Verify SpacerGenerator was called with correct parameters
        call_kwargs = mock_spacer_class.call_args.kwargs
        assert call_kwargs["tolerance_mm"] == 0.5
        assert call_kwargs["thickness_mm"] == 3.0
        assert call_kwargs["chamfer_mm"] == 0.8
        assert call_kwargs["show_arrows"] is False
        assert call_kwargs["align_features"] is False

    @patch("gridfinity_tools.core.drawer_generator.BaseplateGenerator")
    def test_baseplate_config_propagation(self, mock_baseplate_class: MagicMock) -> None:
        """Test baseplate configuration is propagated correctly."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(330.0, 340.0, printer, corner_screws=True)

        piece_config = BaseplateConfig(
            units_width=7, units_depth=8, position_x=0, position_y=0, print_count=1
        )
        gen.generate_baseplate_piece(piece_config)

        # Verify BaseplateGenerator was called with correct parameters
        call_kwargs = mock_baseplate_class.call_args.kwargs
        assert call_kwargs["corner_screws"] is True


class TestDrawerGeneratorIntegration:
    """Integration tests for complete workflows."""

    def test_small_drawer_no_split_workflow(self) -> None:
        """Test workflow for drawer that doesn't need splitting."""
        printer = PrinterConfig.from_preset("bambu-x1c")
        gen = DrawerGenerator(200.0, 200.0, printer)

        layout = gen.get_layout()
        solution = gen.get_solution()

        assert layout.is_split is False
        assert layout.total_pieces == 1
        assert solution.baseplate_layout.total_pieces == 1

    def test_large_drawer_with_split_workflow(self) -> None:
        """Test workflow for drawer requiring splitting."""
        printer = PrinterConfig.from_custom("Small Printer", 200, 200)
        gen = DrawerGenerator(500.0, 500.0, printer)

        layout = gen.get_layout()
        solution = gen.get_solution()

        assert layout.is_split is True
        assert layout.total_pieces > 1
        assert solution.baseplate_layout.total_pieces > 1

    def test_multiple_drawer_configs(self) -> None:
        """Test creating multiple drawer configurations."""
        printer = PrinterConfig.from_preset("bambu-x1c")

        gen1 = DrawerGenerator(300.0, 300.0, printer)
        gen2 = DrawerGenerator(250.0, 250.0, printer)
        gen3 = DrawerGenerator(400.0, 400.0, printer)

        solution1 = gen1.get_solution()
        solution2 = gen2.get_solution()
        solution3 = gen3.get_solution()

        assert solution1.baseplate_width_units == 7
        assert solution2.baseplate_width_units == 5
        assert solution3.baseplate_width_units == 9
