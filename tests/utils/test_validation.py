"""Tests for input validation utilities."""

import pytest

from gridfinity_tools.utils.validation import (
    validate_baseplate_units,
    validate_drawer_dimensions,
    validate_file_format,
    validate_positive,
    validate_printer_dimensions,
    validate_tolerance,
)


class TestValidatePositive:
    """Tests for validate_positive function."""

    def test_positive_integer(self) -> None:
        """Test validation of positive integer."""
        validate_positive(100.0, "test_param")

    def test_positive_float(self) -> None:
        """Test validation of positive float."""
        validate_positive(100.5, "test_param")

    def test_small_positive(self) -> None:
        """Test validation of very small positive."""
        validate_positive(0.001, "test_param")

    def test_zero_fails(self) -> None:
        """Test that zero fails validation."""
        with pytest.raises(ValueError, match="must be positive"):
            validate_positive(0.0, "test_param")

    def test_negative_fails(self) -> None:
        """Test that negative value fails validation."""
        with pytest.raises(ValueError, match="must be positive"):
            validate_positive(-10.0, "test_param")

    def test_error_message_includes_name(self) -> None:
        """Test that error message includes parameter name."""
        with pytest.raises(ValueError, match="my_param"):
            validate_positive(-5.0, "my_param")

    def test_error_message_includes_value(self) -> None:
        """Test that error message includes the invalid value."""
        with pytest.raises(ValueError, match="-5.0"):
            validate_positive(-5.0, "my_param")


class TestValidateDrawerDimensions:
    """Tests for validate_drawer_dimensions function."""

    def test_valid_dimensions(self) -> None:
        """Test valid drawer dimensions."""
        validate_drawer_dimensions(330.0, 340.0)

    def test_large_dimensions(self) -> None:
        """Test large drawer dimensions."""
        validate_drawer_dimensions(582.0, 481.0)

    def test_minimum_dimensions(self) -> None:
        """Test minimum valid dimensions (42mm per unit)."""
        validate_drawer_dimensions(42.0, 42.0)

    def test_fractional_dimensions(self) -> None:
        """Test fractional dimensions."""
        validate_drawer_dimensions(292.1, 520.7)

    def test_zero_width(self) -> None:
        """Test zero width fails."""
        with pytest.raises(ValueError, match="width"):
            validate_drawer_dimensions(0.0, 340.0)

    def test_zero_depth(self) -> None:
        """Test zero depth fails."""
        with pytest.raises(ValueError, match="depth"):
            validate_drawer_dimensions(330.0, 0.0)

    def test_negative_width(self) -> None:
        """Test negative width fails."""
        with pytest.raises(ValueError, match="width"):
            validate_drawer_dimensions(-10.0, 340.0)

    def test_negative_depth(self) -> None:
        """Test negative depth fails."""
        with pytest.raises(ValueError, match="depth"):
            validate_drawer_dimensions(330.0, -10.0)

    def test_too_small_width(self) -> None:
        """Test width less than 42mm fails."""
        with pytest.raises(ValueError, match="42mm"):
            validate_drawer_dimensions(30.0, 340.0)

    def test_too_small_depth(self) -> None:
        """Test depth less than 42mm fails."""
        with pytest.raises(ValueError, match="42mm"):
            validate_drawer_dimensions(330.0, 30.0)


class TestValidateBaseplateUnits:
    """Tests for validate_baseplate_units function."""

    def test_valid_units(self) -> None:
        """Test valid baseplate units."""
        validate_baseplate_units(7, 8)

    def test_single_unit(self) -> None:
        """Test single unit baseplate."""
        validate_baseplate_units(1, 1)

    def test_large_units(self) -> None:
        """Test large baseplate units."""
        validate_baseplate_units(13, 11)

    def test_zero_width(self) -> None:
        """Test zero width fails."""
        with pytest.raises(ValueError, match="width"):
            validate_baseplate_units(0, 8)

    def test_zero_depth(self) -> None:
        """Test zero depth fails."""
        with pytest.raises(ValueError, match="depth"):
            validate_baseplate_units(7, 0)

    def test_negative_width(self) -> None:
        """Test negative width fails."""
        with pytest.raises(ValueError, match="width"):
            validate_baseplate_units(-5, 8)

    def test_negative_depth(self) -> None:
        """Test negative depth fails."""
        with pytest.raises(ValueError, match="depth"):
            validate_baseplate_units(7, -5)

    @pytest.mark.parametrize("units_w,units_d", [(1, 1), (5, 6), (10, 15)])
    def test_various_valid_units(self, units_w: int, units_d: int) -> None:
        """Test various valid unit combinations."""
        validate_baseplate_units(units_w, units_d)


class TestValidateTolerance:
    """Tests for validate_tolerance function."""

    def test_default_tolerance(self) -> None:
        """Test default tolerance value."""
        validate_tolerance(1.0)

    def test_tight_tolerance(self) -> None:
        """Test tight tolerance."""
        validate_tolerance(0.1)

    def test_loose_tolerance(self) -> None:
        """Test loose tolerance."""
        validate_tolerance(2.0)

    def test_zero_fails(self) -> None:
        """Test zero tolerance fails."""
        with pytest.raises(ValueError, match="must be positive"):
            validate_tolerance(0.0)

    def test_negative_fails(self) -> None:
        """Test negative tolerance fails."""
        with pytest.raises(ValueError, match="must be positive"):
            validate_tolerance(-0.5)

    def test_excessive_tolerance_fails(self) -> None:
        """Test excessive tolerance value fails."""
        with pytest.raises(ValueError, match="should be reasonable"):
            validate_tolerance(10.0)

    def test_extreme_tolerance_fails(self) -> None:
        """Test extreme tolerance value fails."""
        with pytest.raises(ValueError, match="should be reasonable"):
            validate_tolerance(100.0)

    @pytest.mark.parametrize("tol", [0.1, 0.5, 1.0, 1.5, 2.0])
    def test_various_valid_tolerances(self, tol: float) -> None:
        """Test various valid tolerance values."""
        validate_tolerance(tol)


class TestValidatePrinterDimensions:
    """Tests for validate_printer_dimensions function."""

    def test_valid_bambu_dimensions(self) -> None:
        """Test valid Bambu Lab X1C dimensions."""
        validate_printer_dimensions(256.0, 256.0)

    def test_valid_prusa_dimensions(self) -> None:
        """Test valid Prusa MK4 dimensions."""
        validate_printer_dimensions(250.0, 210.0)

    def test_valid_ender3_dimensions(self) -> None:
        """Test valid Ender3 dimensions."""
        validate_printer_dimensions(220.0, 220.0)

    def test_minimum_dimensions(self) -> None:
        """Test minimum valid dimensions (42mm for one unit)."""
        validate_printer_dimensions(42.0, 42.0)

    def test_width_too_small(self) -> None:
        """Test width less than 42mm fails."""
        with pytest.raises(ValueError, match="max_width"):
            validate_printer_dimensions(30.0, 256.0)

    def test_depth_too_small(self) -> None:
        """Test depth less than 42mm fails."""
        with pytest.raises(ValueError, match="max_depth"):
            validate_printer_dimensions(256.0, 30.0)

    def test_both_dimensions_too_small(self) -> None:
        """Test both dimensions too small fails."""
        with pytest.raises(ValueError, match="max_width"):
            validate_printer_dimensions(30.0, 30.0)

    def test_large_dimensions(self) -> None:
        """Test very large printer dimensions."""
        validate_printer_dimensions(500.0, 500.0)


class TestValidateFileFormat:
    """Tests for validate_file_format function."""

    def test_valid_stl_format(self) -> None:
        """Test valid STL format."""
        validate_file_format("stl", {"stl", "step", "svg"})

    def test_valid_step_format(self) -> None:
        """Test valid STEP format."""
        validate_file_format("step", {"stl", "step", "svg"})

    def test_valid_svg_format(self) -> None:
        """Test valid SVG format."""
        validate_file_format("svg", {"stl", "step", "svg"})

    def test_case_insensitive(self) -> None:
        """Test that format validation is case insensitive."""
        validate_file_format("STL", {"stl", "step", "svg"})
        validate_file_format("STEP", {"stl", "step", "svg"})

    def test_invalid_format(self) -> None:
        """Test invalid format fails."""
        with pytest.raises(ValueError, match="unsupported"):
            validate_file_format("obj", {"stl", "step", "svg"})

    def test_empty_format(self) -> None:
        """Test empty format fails."""
        with pytest.raises(ValueError, match="unsupported"):
            validate_file_format("", {"stl", "step", "svg"})

    def test_error_message_includes_options(self) -> None:
        """Test that error message includes valid options."""
        with pytest.raises(ValueError, match="stl"):
            validate_file_format("obj", {"stl", "step"})

    def test_custom_formats(self) -> None:
        """Test with custom format set."""
        validate_file_format("xyz", {"xyz", "abc"})
        with pytest.raises(ValueError):
            validate_file_format("obj", {"xyz", "abc"})
