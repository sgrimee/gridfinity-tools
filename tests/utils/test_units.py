"""Tests for unit conversion utilities."""

import pytest

from gridfinity_tools.utils.units import inches_to_mm, mm_to_inches, parse_dimension


class TestInchesToMm:
    """Tests for inches_to_mm function."""

    def test_one_inch(self) -> None:
        """Test converting 1 inch to mm."""
        assert inches_to_mm(1.0) == pytest.approx(25.4)

    def test_fractional_inches(self) -> None:
        """Test converting fractional inches."""
        assert inches_to_mm(11.5) == pytest.approx(292.1)

    def test_zero_inches(self) -> None:
        """Test converting zero inches."""
        assert inches_to_mm(0.0) == 0.0

    @pytest.mark.parametrize(
        "inches,expected_mm",
        [
            (1.0, 25.4),
            (10.0, 254.0),
            (11.5, 292.1),
            (20.5, 520.7),
            (0.5, 12.7),
        ],
    )
    def test_various_conversions(self, inches: float, expected_mm: float) -> None:
        """Test various inch to mm conversions."""
        assert inches_to_mm(inches) == pytest.approx(expected_mm)


class TestMmToInches:
    """Tests for mm_to_inches function."""

    def test_one_inch_mm(self) -> None:
        """Test converting 25.4mm to inches."""
        assert mm_to_inches(25.4) == pytest.approx(1.0)

    def test_fractional_result(self) -> None:
        """Test conversion resulting in fractional inches."""
        assert mm_to_inches(292.1) == pytest.approx(11.5)

    def test_zero_mm(self) -> None:
        """Test converting zero mm."""
        assert mm_to_inches(0.0) == 0.0

    @pytest.mark.parametrize(
        "mm,expected_inches",
        [
            (25.4, 1.0),
            (254.0, 10.0),
            (292.1, 11.5),
            (520.7, 20.5),
            (12.7, 0.5),
        ],
    )
    def test_various_conversions(self, mm: float, expected_inches: float) -> None:
        """Test various mm to inch conversions."""
        assert mm_to_inches(mm) == pytest.approx(expected_inches)


class TestParseDimension:
    """Tests for parse_dimension function."""

    def test_parse_plain_number(self) -> None:
        """Test parsing plain numeric string as mm."""
        assert parse_dimension("330") == 330.0

    def test_parse_plain_float(self) -> None:
        """Test parsing plain float string as mm."""
        assert parse_dimension("330.5") == 330.5

    def test_parse_inches(self) -> None:
        """Test parsing inches with 'in' suffix."""
        assert parse_dimension("11.5in") == pytest.approx(292.1)

    def test_parse_inches_case_insensitive(self) -> None:
        """Test parsing inches is case insensitive."""
        assert parse_dimension("11.5IN") == pytest.approx(292.1)
        assert parse_dimension("11.5In") == pytest.approx(292.1)

    def test_parse_inches_with_spaces(self) -> None:
        """Test parsing inches with leading/trailing spaces."""
        assert parse_dimension("  11.5in  ") == pytest.approx(292.1)

    def test_parse_invalid_format(self) -> None:
        """Test parsing invalid format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid dimension format"):
            parse_dimension("abc")

    def test_parse_invalid_inch_format(self) -> None:
        """Test parsing invalid inch format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid inch dimension format"):
            parse_dimension("abcin")

    def test_parse_negative_mm(self) -> None:
        """Test parsing negative mm raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            parse_dimension("-330")

    def test_parse_negative_inches(self) -> None:
        """Test parsing negative inches raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            parse_dimension("-11.5in")

    def test_parse_zero_mm(self) -> None:
        """Test parsing zero mm raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            parse_dimension("0")

    def test_parse_zero_inches(self) -> None:
        """Test parsing zero inches raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            parse_dimension("0in")

    @pytest.mark.parametrize(
        "input_str,expected_mm",
        [
            ("330", 330.0),
            ("340", 340.0),
            ("11.5in", 292.1),
            ("20.5in", 520.7),
            ("1.0in", 25.4),
            ("582", 582.0),
            ("481", 481.0),
        ],
    )
    def test_parse_various_formats(self, input_str: str, expected_mm: float) -> None:
        """Test parsing various dimension formats."""
        assert parse_dimension(input_str) == pytest.approx(expected_mm)
