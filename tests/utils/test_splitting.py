"""Tests for baseplate splitting utilities."""

import pytest

from gridfinity_tools.utils.splitting import (
    calculate_baseplate_split,
    calculate_baseplate_units,
    calculate_split_grid,
    calculate_total_pieces,
)


class TestCalculateBaseplateUnits:
    """Tests for calculate_baseplate_units function."""

    def test_330mm_drawer(self) -> None:
        """Test 330mm drawer (IKEA ALEX narrow width)."""
        assert calculate_baseplate_units(330.0) == 7

    def test_340mm_drawer(self) -> None:
        """Test 340mm drawer."""
        assert calculate_baseplate_units(340.0) == 8

    def test_exact_unit_boundary(self) -> None:
        """Test dimension exactly on unit boundary."""
        assert calculate_baseplate_units(42.0) == 1
        assert calculate_baseplate_units(84.0) == 2
        assert calculate_baseplate_units(294.0) == 7

    def test_under_one_unit(self) -> None:
        """Test dimension under one unit."""
        assert calculate_baseplate_units(41.0) == 0
        assert calculate_baseplate_units(30.0) == 0

    def test_fractional_dimensions(self) -> None:
        """Test fractional dimensions."""
        assert calculate_baseplate_units(292.1) == 6
        assert calculate_baseplate_units(520.7) == 12

    @pytest.mark.parametrize(
        "drawer_mm,expected_units",
        [
            (330.0, 7),
            (340.0, 8),
            (582.0, 13),
            (481.0, 11),
            (292.1, 6),
            (520.7, 12),
            (42.0, 1),
            (84.0, 2),
        ],
    )
    def test_various_dimensions(self, drawer_mm: float, expected_units: int) -> None:
        """Test various drawer dimensions."""
        assert calculate_baseplate_units(drawer_mm) == expected_units


class TestCalculateBaseplateSplit:
    """Tests for calculate_baseplate_split function."""

    def test_single_piece_fits(self) -> None:
        """Test baseplate that fits in one piece."""
        result = calculate_baseplate_split(5, 256)
        assert result == [5]
        assert len(result) == 1

    def test_single_piece_at_boundary(self) -> None:
        """Test baseplate exactly at max dimension."""
        # 6 units = 252mm, which is <= 256mm
        result = calculate_baseplate_split(6, 256)
        assert result == [6]

    def test_split_into_two_pieces(self) -> None:
        """Test baseplate that needs to split into 2 pieces."""
        # 7 units = 294mm, max 256mm needs 2 pieces
        result = calculate_baseplate_split(7, 256)
        assert len(result) == 2
        assert sum(result) == 7

    def test_split_distribution_even(self) -> None:
        """Test that units are distributed evenly."""
        # 8 units split at 256mm should give [4, 4]
        result = calculate_baseplate_split(8, 200)
        assert sum(result) == 8
        # All pieces should be roughly equal size
        assert max(result) - min(result) <= 1

    def test_split_distribution_uneven(self) -> None:
        """Test that extra units go to first pieces."""
        # 7 units at 250mm (6*42=252) should split into [4, 3]
        result = calculate_baseplate_split(7, 250)
        assert len(result) == 2
        assert sum(result) == 7
        # Extra unit should go to first piece
        assert result[0] >= result[1]

    def test_craftsman_drawer_width(self) -> None:
        """Test large Craftsman drawer width (582mm)."""
        # 13 units = 546mm, won't fit in 256mm
        result = calculate_baseplate_split(13, 256)
        assert len(result) > 1
        assert sum(result) == 13

    def test_craftsman_drawer_depth(self) -> None:
        """Test large Craftsman drawer depth (481mm)."""
        # 11 units = 462mm, won't fit in 256mm
        result = calculate_baseplate_split(11, 256)
        assert len(result) > 1
        assert sum(result) == 11

    def test_invalid_zero_units(self) -> None:
        """Test zero units raises ValueError."""
        with pytest.raises(ValueError, match="must be at least 1"):
            calculate_baseplate_split(0, 256)

    def test_invalid_negative_units(self) -> None:
        """Test negative units raises ValueError."""
        with pytest.raises(ValueError, match="must be at least 1"):
            calculate_baseplate_split(-5, 256)

    def test_invalid_small_max_dimension(self) -> None:
        """Test max dimension less than GRIDFINITY_UNIT raises ValueError."""
        with pytest.raises(ValueError, match="must be at least"):
            calculate_baseplate_split(5, 30)

    def test_invalid_zero_max_dimension(self) -> None:
        """Test zero max dimension raises ValueError."""
        with pytest.raises(ValueError, match="must be at least"):
            calculate_baseplate_split(5, 0)

    @pytest.mark.parametrize(
        "total_units,max_mm,expected",
        [
            (5, 256, [5]),  # Fits in one
            (6, 256, [6]),  # Exactly at boundary
            (7, 256, [4, 3]),  # Needs split (7 * 42 = 294mm)
            (13, 256, [5, 4, 4]),  # Large split (13 * 42 = 546mm needs 3)
            (11, 256, [6, 5]),  # Another large split (11 * 42 = 462mm needs 2)
        ],
    )
    def test_various_splits(self, total_units: int, max_mm: int, expected: list[int]) -> None:
        """Test various splitting scenarios."""
        result = calculate_baseplate_split(total_units, max_mm)
        assert result == expected


class TestCalculateSplitGrid:
    """Tests for calculate_split_grid function."""

    def test_single_piece_grid(self) -> None:
        """Test grid that fits in one piece."""
        width_pieces, depth_pieces = calculate_split_grid(5, 6, 256, 256)
        assert width_pieces == [5]
        assert depth_pieces == [6]

    def test_two_piece_grid(self) -> None:
        """Test 2D grid that needs splitting in both dimensions."""
        # 7 units = 294mm (over 256), 8 units = 336mm (over 256)
        width_pieces, depth_pieces = calculate_split_grid(7, 8, 256, 256)
        assert sum(width_pieces) == 7
        assert sum(depth_pieces) == 8
        assert len(width_pieces) > 1
        assert len(depth_pieces) > 1

    def test_large_drawer_grid(self) -> None:
        """Test large Craftsman drawer splits both dimensions."""
        width_pieces, depth_pieces = calculate_split_grid(13, 11, 256, 256)
        assert len(width_pieces) > 1
        assert len(depth_pieces) > 1
        assert sum(width_pieces) == 13
        assert sum(depth_pieces) == 11

    def test_asymmetric_split(self) -> None:
        """Test grid that splits more in one dimension."""
        width_pieces, depth_pieces = calculate_split_grid(13, 6, 256, 256)
        assert len(width_pieces) > 1
        assert len(depth_pieces) == 1
        assert sum(width_pieces) == 13
        assert sum(depth_pieces) == 6

    @pytest.mark.parametrize(
        "width_u,depth_u,max_w,max_d",
        [
            (5, 6, 256, 256),
            (7, 8, 256, 256),
            (13, 11, 256, 256),
            (13, 6, 256, 256),
        ],
    )
    def test_various_grids(self, width_u: int, depth_u: int, max_w: int, max_d: int) -> None:
        """Test various 2D grid splits."""
        width_pieces, depth_pieces = calculate_split_grid(width_u, depth_u, max_w, max_d)
        assert sum(width_pieces) == width_u
        assert sum(depth_pieces) == depth_u


class TestCalculateTotalPieces:
    """Tests for calculate_total_pieces function."""

    def test_single_piece(self) -> None:
        """Test baseplate that is single piece."""
        result = calculate_total_pieces(5, 6, 256, 256)
        assert result == 1

    def test_two_by_two_grid(self) -> None:
        """Test 2D split (6 pieces total for 13x11 units)."""
        # 13 units = 546mm (needs 3 pieces in width)
        # 11 units = 462mm (needs 2 pieces in depth)
        # 3 * 2 = 6 pieces total
        result = calculate_total_pieces(13, 11, 256, 256)
        assert result == 6

    def test_three_by_one_grid(self) -> None:
        """Test 3x1 split (3 pieces total)."""
        result = calculate_total_pieces(13, 6, 256, 256)
        assert result == 3

    def test_one_by_three_grid(self) -> None:
        """Test 1x3 split (3 pieces total)."""
        result = calculate_total_pieces(6, 13, 256, 256)
        assert result == 3

    @pytest.mark.parametrize(
        "width_u,depth_u,total",
        [
            (5, 6, 1),  # 210mm x 252mm - fits in one
            (7, 8, 4),  # 294mm x 336mm - needs 2x2 = 4 pieces
            (13, 11, 6),  # 546mm x 462mm - needs 3x2 = 6 pieces
            (13, 6, 3),  # 546mm x 252mm - needs 3x1 = 3 pieces
            (6, 13, 3),  # 252mm x 546mm - needs 1x3 = 3 pieces
        ],
    )
    def test_various_total_pieces(self, width_u: int, depth_u: int, total: int) -> None:
        """Test various total piece calculations."""
        result = calculate_total_pieces(width_u, depth_u, 256, 256)
        assert result == total
