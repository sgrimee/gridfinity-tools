"""Tests for filename generation utilities."""

from pathlib import Path

import pytest

from gridfinity_tools.utils.naming import (
    add_path_to_filename,
    generate_assembly_filename,
    generate_baseplate_filename,
    generate_spacer_filename,
)


class TestGenerateSpacerFilename:
    """Tests for generate_spacer_filename function."""

    def test_default_tolerance(self) -> None:
        """Test spacer filename with default tolerance."""
        result = generate_spacer_filename(330.0, 340.0, 1.0, "half_set", "stl")
        assert result == "drawer_330x340_spacer_half_set.stl"

    def test_custom_tolerance(self) -> None:
        """Test spacer filename with custom tolerance."""
        result = generate_spacer_filename(330.0, 340.0, 0.5, "half_set", "stl")
        assert result == "drawer_330x340_tol0.5_spacer_half_set.stl"

    def test_full_set_step_format(self) -> None:
        """Test spacer filename with full_set and STEP format."""
        result = generate_spacer_filename(330.0, 340.0, 1.0, "full_set", "step")
        assert result == "drawer_330x340_spacer_full_set.step"

    def test_full_with_baseplate_step_format(self) -> None:
        """Test spacer filename with full_with_baseplate mode."""
        result = generate_spacer_filename(330.0, 340.0, 1.0, "full_with_baseplate", "step")
        assert result == "drawer_330x340_spacer_full_with_baseplate.step"

    def test_fractional_dimensions_truncated(self) -> None:
        """Test that fractional dimensions are truncated to int."""
        result = generate_spacer_filename(292.1, 520.7, 1.0, "half_set", "stl")
        assert result == "drawer_292x520_spacer_half_set.stl"

    def test_tolerance_precision(self) -> None:
        """Test tolerance value precision in filename."""
        result = generate_spacer_filename(330.0, 340.0, 0.75, "half_set", "stl")
        assert result == "drawer_330x340_tol0.75_spacer_half_set.stl"

    @pytest.mark.parametrize(
        "width,depth,tol,mode,fmt,expected",
        [
            (330.0, 340.0, 1.0, "half_set", "stl", "drawer_330x340_spacer_half_set.stl"),
            (330.0, 340.0, 0.5, "half_set", "stl", "drawer_330x340_tol0.5_spacer_half_set.stl"),
            (582.0, 481.0, 1.0, "full_set", "step", "drawer_582x481_spacer_full_set.step"),
            (292.1, 520.7, 1.0, "half_set", "stl", "drawer_292x520_spacer_half_set.stl"),
        ],
    )
    def test_various_spacer_filenames(
        self,
        width: float,
        depth: float,
        tol: float,
        mode: str,
        fmt: str,
        expected: str,
    ) -> None:
        """Test various spacer filename combinations."""
        result = generate_spacer_filename(width, depth, tol, mode, fmt)
        assert result == expected


class TestGenerateBaseplateFilename:
    """Tests for generate_baseplate_filename function."""

    def test_without_corner_screws(self) -> None:
        """Test baseplate filename without corner screws."""
        result = generate_baseplate_filename(330.0, 340.0, 7, 8, False, "stl")
        assert result == "drawer_330x340_baseplate_7x8.stl"

    def test_with_corner_screws(self) -> None:
        """Test baseplate filename with corner screws."""
        result = generate_baseplate_filename(330.0, 340.0, 7, 8, True, "stl")
        assert result == "drawer_330x340_screws_baseplate_7x8.stl"

    def test_split_piece_naming(self) -> None:
        """Test naming for split baseplate pieces."""
        result = generate_baseplate_filename(330.0, 340.0, 4, 4, False, "stl")
        assert result == "drawer_330x340_baseplate_4x4.stl"

    def test_step_format(self) -> None:
        """Test baseplate filename with STEP format."""
        result = generate_baseplate_filename(330.0, 340.0, 7, 8, False, "step")
        assert result == "drawer_330x340_baseplate_7x8.step"

    def test_fractional_dimensions_truncated(self) -> None:
        """Test that fractional dimensions are truncated to int."""
        result = generate_baseplate_filename(292.1, 520.7, 7, 12, False, "stl")
        assert result == "drawer_292x520_baseplate_7x12.stl"

    def test_screws_with_fractional_dimensions(self) -> None:
        """Test screws flag with fractional dimensions."""
        result = generate_baseplate_filename(292.1, 520.7, 7, 12, True, "stl")
        assert result == "drawer_292x520_screws_baseplate_7x12.stl"

    @pytest.mark.parametrize(
        "width,depth,units_w,units_d,screws,fmt,expected",
        [
            (330.0, 340.0, 7, 8, False, "stl", "drawer_330x340_baseplate_7x8.stl"),
            (330.0, 340.0, 7, 8, True, "stl", "drawer_330x340_screws_baseplate_7x8.stl"),
            (330.0, 340.0, 4, 4, False, "stl", "drawer_330x340_baseplate_4x4.stl"),
            (330.0, 340.0, 3, 4, True, "step", "drawer_330x340_screws_baseplate_3x4.step"),
        ],
    )
    def test_various_baseplate_filenames(
        self,
        width: float,
        depth: float,
        units_w: int,
        units_d: int,
        screws: bool,
        fmt: str,
        expected: str,
    ) -> None:
        """Test various baseplate filename combinations."""
        result = generate_baseplate_filename(width, depth, units_w, units_d, screws, fmt)
        assert result == expected


class TestGenerateAssemblyFilename:
    """Tests for generate_assembly_filename function."""

    def test_default_tolerance(self) -> None:
        """Test assembly filename with default tolerance."""
        result = generate_assembly_filename(330.0, 340.0, 1.0, "step")
        assert result == "drawer_330x340_full_assembly.step"

    def test_custom_tolerance(self) -> None:
        """Test assembly filename with custom tolerance."""
        result = generate_assembly_filename(330.0, 340.0, 0.5, "step")
        assert result == "drawer_330x340_tol0.5_full_assembly.step"

    def test_svg_format(self) -> None:
        """Test assembly filename with SVG format."""
        result = generate_assembly_filename(330.0, 340.0, 1.0, "svg")
        assert result == "drawer_330x340_full_assembly.svg"

    def test_fractional_dimensions_truncated(self) -> None:
        """Test that fractional dimensions are truncated to int."""
        result = generate_assembly_filename(292.1, 520.7, 1.0, "step")
        assert result == "drawer_292x520_full_assembly.step"

    def test_custom_tolerance_with_fractional_dimensions(self) -> None:
        """Test custom tolerance with fractional dimensions."""
        result = generate_assembly_filename(292.1, 520.7, 0.75, "step")
        assert result == "drawer_292x520_tol0.75_full_assembly.step"

    @pytest.mark.parametrize(
        "width,depth,tol,fmt,expected",
        [
            (330.0, 340.0, 1.0, "step", "drawer_330x340_full_assembly.step"),
            (330.0, 340.0, 0.5, "step", "drawer_330x340_tol0.5_full_assembly.step"),
            (582.0, 481.0, 1.0, "svg", "drawer_582x481_full_assembly.svg"),
            (292.1, 520.7, 1.0, "step", "drawer_292x520_full_assembly.step"),
        ],
    )
    def test_various_assembly_filenames(
        self,
        width: float,
        depth: float,
        tol: float,
        fmt: str,
        expected: str,
    ) -> None:
        """Test various assembly filename combinations."""
        result = generate_assembly_filename(width, depth, tol, fmt)
        assert result == expected


class TestAddPathToFilename:
    """Tests for add_path_to_filename function."""

    def test_with_string_path(self, tmp_path: Path) -> None:
        """Test combining filename with string path."""
        result = add_path_to_filename("test.stl", str(tmp_path))
        assert result == tmp_path / "test.stl"

    def test_with_path_object(self, tmp_path: Path) -> None:
        """Test combining filename with Path object."""
        result = add_path_to_filename("test.stl", tmp_path)
        assert result == tmp_path / "test.stl"

    def test_with_relative_path(self) -> None:
        """Test combining filename with relative path."""
        result = add_path_to_filename("test.stl", "output")
        assert result == Path("output") / "test.stl"

    def test_returns_path_object(self) -> None:
        """Test that result is a Path object."""
        result = add_path_to_filename("test.stl", "output")
        assert isinstance(result, Path)

    def test_preserves_filename_extension(self) -> None:
        """Test that filename extension is preserved."""
        result = add_path_to_filename("drawer_330x340_baseplate_7x8.stl", "output")
        assert result.suffix == ".stl"
        assert result.name == "drawer_330x340_baseplate_7x8.stl"

    @pytest.mark.parametrize(
        "filename,path",
        [
            ("test.stl", "output"),
            ("drawer_330x340_spacer_half_set.stl", "output"),
            ("drawer_330x340_baseplate_7x8.step", "models/baseplates"),
            ("assembly.step", "."),
        ],
    )
    def test_various_paths(self, filename: str, path: str) -> None:
        """Test combining various filenames with paths."""
        result = add_path_to_filename(filename, path)
        assert result == Path(path) / filename
