"""Tests for baseplate generator."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gridfinity_tools.core.baseplate_generator import BaseplateGenerator


class TestBaseplateGeneratorInitialization:
    """Tests for BaseplateGenerator initialization."""

    def test_basic_initialization(self) -> None:
        """Test basic baseplate generator initialization."""
        gen = BaseplateGenerator(7, 8)
        assert gen.units_width == 7
        assert gen.units_depth == 8

    def test_initialization_with_corner_screws(self) -> None:
        """Test initialization with corner screws enabled."""
        gen = BaseplateGenerator(7, 8, corner_screws=True)
        assert gen.corner_screws is True

    def test_initialization_with_defaults(self) -> None:
        """Test all defaults are set correctly."""
        gen = BaseplateGenerator(7, 8)
        assert gen.corner_screws is False
        assert gen.screw_hole_diam_mm == 5.0
        assert gen.countersink_diam_mm == 10.0
        assert gen.countersink_angle_deg == 82
        assert gen.ext_depth_mm == 0.0
        assert gen.straight_bottom is False

    def test_initialization_with_custom_options(self) -> None:
        """Test initialization with custom options."""
        gen = BaseplateGenerator(
            7,
            8,
            corner_screws=True,
            screw_hole_diam_mm=6.0,
            countersink_diam_mm=12.0,
            countersink_angle_deg=90,
            ext_depth_mm=5.0,
            straight_bottom=True,
        )
        assert gen.corner_screws is True
        assert gen.screw_hole_diam_mm == 6.0
        assert gen.countersink_diam_mm == 12.0
        assert gen.countersink_angle_deg == 90
        assert gen.ext_depth_mm == 5.0
        assert gen.straight_bottom is True

    def test_invalid_zero_units_width(self) -> None:
        """Test zero units width fails."""
        with pytest.raises(ValueError):
            BaseplateGenerator(0, 8)

    def test_invalid_zero_units_depth(self) -> None:
        """Test zero units depth fails."""
        with pytest.raises(ValueError):
            BaseplateGenerator(7, 0)

    def test_invalid_negative_units_width(self) -> None:
        """Test negative units width fails."""
        with pytest.raises(ValueError):
            BaseplateGenerator(-5, 8)

    def test_invalid_negative_units_depth(self) -> None:
        """Test negative units depth fails."""
        with pytest.raises(ValueError):
            BaseplateGenerator(7, -5)

    def test_single_unit_baseplate(self) -> None:
        """Test 1x1 baseplate is valid."""
        gen = BaseplateGenerator(1, 1)
        assert gen.units_width == 1
        assert gen.units_depth == 1

    def test_large_baseplate(self) -> None:
        """Test large baseplate is valid."""
        gen = BaseplateGenerator(13, 11)
        assert gen.units_width == 13
        assert gen.units_depth == 11


class TestBaseplateGeneratorLazyInitialization:
    """Tests for lazy initialization of underlying baseplate."""

    def test_baseplate_not_created_on_init(self) -> None:
        """Test that underlying baseplate is not created immediately."""
        gen = BaseplateGenerator(7, 8)
        assert gen._baseplate is None

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_baseplate_created_on_first_use(self, mock_baseplate_class: MagicMock) -> None:
        """Test that underlying baseplate is created on first method call."""
        gen = BaseplateGenerator(7, 8)
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        # Trigger creation
        gen.generate()

        # Verify baseplate was created
        mock_baseplate_class.assert_called_once()

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_baseplate_reused_on_multiple_calls(self, mock_baseplate_class: MagicMock) -> None:
        """Test that underlying baseplate is reused on multiple calls."""
        gen = BaseplateGenerator(7, 8)
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        # Make multiple calls
        gen.generate()
        gen.save_stl("test.stl")

        # Verify baseplate was created only once
        assert mock_baseplate_class.call_count == 1


class TestBaseplateGeneratorGeneration:
    """Tests for baseplate generation methods."""

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_generate(self, mock_baseplate_class: MagicMock) -> None:
        """Test generating baseplate."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        result = gen.generate()

        assert result is not None


class TestBaseplateGeneratorFileOutput:
    """Tests for file output methods."""

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_save_stl(self, mock_baseplate_class: MagicMock) -> None:
        """Test saving STL file."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        gen.save_stl("test.stl")

        mock_instance.save_stl_file.assert_called_once_with("test.stl")

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_save_stl_with_path_object(self, mock_baseplate_class: MagicMock) -> None:
        """Test saving STL with Path object."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        path = Path("output/test.stl")
        gen.save_stl(path)

        mock_instance.save_stl_file.assert_called_once_with(str(path))

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_save_step(self, mock_baseplate_class: MagicMock) -> None:
        """Test saving STEP file."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        gen.save_step("test.step")

        mock_instance.save_step_file.assert_called_once_with("test.step")

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_save_step_with_path_object(self, mock_baseplate_class: MagicMock) -> None:
        """Test saving STEP with Path object."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        path = Path("output/test.step")
        gen.save_step(path)

        mock_instance.save_step_file.assert_called_once_with(str(path))

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_save_svg(self, mock_baseplate_class: MagicMock) -> None:
        """Test saving SVG file."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        gen.save_svg("test.svg")

        mock_instance.save_svg_file.assert_called_once_with("test.svg")

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_save_svg_with_path_object(self, mock_baseplate_class: MagicMock) -> None:
        """Test saving SVG with Path object."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        path = Path("output/test.svg")
        gen.save_svg(path)

        mock_instance.save_svg_file.assert_called_once_with(str(path))


class TestBaseplateGeneratorBaseplateCreationParams:
    """Tests for parameter passing to underlying GridfinityBaseplate."""

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_baseplate_params_default(self, mock_baseplate_class: MagicMock) -> None:
        """Test default parameters passed to GridfinityBaseplate."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        gen.generate()

        # Check that GridfinityBaseplate was called with correct params
        call_kwargs = mock_baseplate_class.call_args[1]
        assert call_kwargs["corner_screws"] is False
        assert call_kwargs["csk_hole"] == 5.0
        assert call_kwargs["csk_diam"] == 10.0
        assert call_kwargs["csk_angle"] == 82
        assert call_kwargs["ext_depth"] == 0.0
        assert call_kwargs["straight_bottom"] is False

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_baseplate_params_custom(self, mock_baseplate_class: MagicMock) -> None:
        """Test custom parameters passed to GridfinityBaseplate."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(
            7,
            8,
            corner_screws=True,
            screw_hole_diam_mm=6.0,
            countersink_diam_mm=12.0,
            countersink_angle_deg=90,
            ext_depth_mm=5.0,
            straight_bottom=True,
        )
        gen.generate()

        # Check that GridfinityBaseplate was called with correct params
        call_kwargs = mock_baseplate_class.call_args[1]
        assert call_kwargs["corner_screws"] is True
        assert call_kwargs["csk_hole"] == 6.0
        assert call_kwargs["csk_diam"] == 12.0
        assert call_kwargs["csk_angle"] == 90
        assert call_kwargs["ext_depth"] == 5.0
        assert call_kwargs["straight_bottom"] is True

    @patch("gridfinity_tools.core.baseplate_generator.GridfinityBaseplate")
    def test_baseplate_units_passed_correctly(self, mock_baseplate_class: MagicMock) -> None:
        """Test that units are passed correctly as positional args."""
        mock_instance = MagicMock()
        mock_baseplate_class.return_value = mock_instance

        gen = BaseplateGenerator(7, 8)
        gen.generate()

        # Check that positional args are correct
        call_args = mock_baseplate_class.call_args[0]
        assert call_args[0] == 7
        assert call_args[1] == 8
