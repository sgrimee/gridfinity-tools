"""Tests for spacer generator."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gridfinity_tools.core.spacer_generator import SpacerGenerator


class TestSpacerGeneratorInitialization:
    """Tests for SpacerGenerator initialization."""

    def test_basic_initialization(self) -> None:
        """Test basic spacer generator initialization."""
        gen = SpacerGenerator(330.0, 340.0)
        assert gen.width_mm == 330.0
        assert gen.depth_mm == 340.0

    def test_initialization_with_custom_tolerance(self) -> None:
        """Test initialization with custom tolerance."""
        gen = SpacerGenerator(330.0, 340.0, tolerance_mm=0.5)
        assert gen.tolerance_mm == 0.5

    def test_initialization_with_custom_thickness(self) -> None:
        """Test initialization with custom thickness."""
        gen = SpacerGenerator(330.0, 340.0, thickness_mm=3.0)
        assert gen.thickness_mm == 3.0

    def test_initialization_with_defaults(self) -> None:
        """Test all defaults are set correctly."""
        gen = SpacerGenerator(330.0, 340.0)
        assert gen.thickness_mm == 5.0
        assert gen.tolerance_mm == 1.0
        assert gen.chamfer_mm == 1.0
        assert gen.show_arrows is True
        assert gen.align_features is True
        assert gen.verbose is False

    def test_initialization_with_custom_options(self) -> None:
        """Test initialization with custom options."""
        gen = SpacerGenerator(
            330.0,
            340.0,
            thickness_mm=4.0,
            tolerance_mm=0.75,
            chamfer_mm=0.5,
            show_arrows=False,
            align_features=False,
            verbose=True,
        )
        assert gen.thickness_mm == 4.0
        assert gen.tolerance_mm == 0.75
        assert gen.chamfer_mm == 0.5
        assert gen.show_arrows is False
        assert gen.align_features is False
        assert gen.verbose is True

    def test_invalid_width_dimension(self) -> None:
        """Test invalid width dimension fails."""
        with pytest.raises(ValueError):
            SpacerGenerator(0.0, 340.0)

    def test_invalid_depth_dimension(self) -> None:
        """Test invalid depth dimension fails."""
        with pytest.raises(ValueError):
            SpacerGenerator(330.0, 0.0)

    def test_too_small_dimensions(self) -> None:
        """Test dimensions smaller than 42mm fail."""
        with pytest.raises(ValueError):
            SpacerGenerator(30.0, 340.0)

    def test_fractional_dimensions(self) -> None:
        """Test fractional dimensions are accepted."""
        gen = SpacerGenerator(292.1, 520.7)
        assert gen.width_mm == 292.1
        assert gen.depth_mm == 520.7


class TestSpacerGeneratorLazyInitialization:
    """Tests for lazy initialization of underlying spacer."""

    def test_spacer_not_created_on_init(self) -> None:
        """Test that underlying spacer is not created immediately."""
        gen = SpacerGenerator(330.0, 340.0)
        assert gen._spacer is None

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_spacer_created_on_first_use(self, mock_spacer_class: MagicMock) -> None:
        """Test that underlying spacer is created on first method call."""
        gen = SpacerGenerator(330.0, 340.0)
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        # Trigger creation
        gen.generate_half_set()

        # Verify spacer was created
        mock_spacer_class.assert_called_once()

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_spacer_reused_on_multiple_calls(self, mock_spacer_class: MagicMock) -> None:
        """Test that underlying spacer is reused on multiple calls."""
        gen = SpacerGenerator(330.0, 340.0)
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        # Make multiple calls
        gen.generate_half_set()
        gen.generate_full_set()

        # Verify spacer was created only once
        assert mock_spacer_class.call_count == 1


class TestSpacerGeneratorGeneration:
    """Tests for spacer generation methods."""

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_generate_half_set(self, mock_spacer_class: MagicMock) -> None:
        """Test generating half set."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        result = gen.generate_half_set()

        mock_instance.render_half_set.assert_called_once()
        assert result is not None

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_generate_full_set(self, mock_spacer_class: MagicMock) -> None:
        """Test generating full set."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        result = gen.generate_full_set()

        mock_instance.render_full_set.assert_called_once_with()
        assert result is not None

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_generate_full_assembly_with_baseplate(self, mock_spacer_class: MagicMock) -> None:
        """Test generating full assembly with baseplate."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        result = gen.generate_full_assembly(include_baseplate=True)

        mock_instance.render_full_set.assert_called_once_with(include_baseplate=True)
        assert result is not None

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_generate_full_assembly_without_baseplate(self, mock_spacer_class: MagicMock) -> None:
        """Test generating full assembly without baseplate."""
        mock_instance = MagicMock()
        mock_instance.cq_obj = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        result = gen.generate_full_assembly(include_baseplate=False)

        mock_instance.render_full_set.assert_called_once_with(include_baseplate=False)
        assert result is not None


class TestSpacerGeneratorFileOutput:
    """Tests for file output methods."""

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_save_stl_half_set(self, mock_spacer_class: MagicMock) -> None:
        """Test saving STL half set."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        gen.save_stl("test.stl", render_mode="half_set")

        mock_instance.render_half_set.assert_called_once()
        mock_instance.save_stl_file.assert_called_once_with("test.stl")

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_save_stl_full_set(self, mock_spacer_class: MagicMock) -> None:
        """Test saving STL full set."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        gen.save_stl("test.stl", render_mode="full_set")

        mock_instance.render_full_set.assert_called_once()
        mock_instance.save_stl_file.assert_called_once_with("test.stl")

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_save_stl_with_path_object(self, mock_spacer_class: MagicMock) -> None:
        """Test saving STL with Path object."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        path = Path("output/test.stl")
        gen.save_stl(path)

        mock_instance.save_stl_file.assert_called_once_with(str(path))

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_save_step_full_assembly(self, mock_spacer_class: MagicMock) -> None:
        """Test saving STEP full assembly."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        gen.save_step("test.step", render_mode="full_assembly")

        mock_instance.render_full_set.assert_called_once_with(include_baseplate=True)
        mock_instance.save_step_file.assert_called_once_with("test.step")

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_save_step_full_set(self, mock_spacer_class: MagicMock) -> None:
        """Test saving STEP full set."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        gen.save_step("test.step", render_mode="full_set")

        mock_instance.render_full_set.assert_called_once_with()
        mock_instance.save_step_file.assert_called_once_with("test.step")

    def test_save_stl_invalid_render_mode(self) -> None:
        """Test saving STL with invalid render mode."""
        gen = SpacerGenerator(330.0, 340.0)
        with pytest.raises(ValueError, match="Invalid render_mode"):
            gen.save_stl("test.stl", render_mode="invalid")

    def test_save_step_invalid_render_mode(self) -> None:
        """Test saving STEP with invalid render mode."""
        gen = SpacerGenerator(330.0, 340.0)
        with pytest.raises(ValueError, match="Invalid render_mode"):
            gen.save_step("test.step", render_mode="invalid")


class TestSpacerGeneratorSpacerCreationParams:
    """Tests for parameter passing to underlying GridfinityDrawerSpacer."""

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_spacer_params_default(self, mock_spacer_class: MagicMock) -> None:
        """Test default parameters passed to GridfinityDrawerSpacer."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(330.0, 340.0)
        gen.generate_half_set()

        # Check that GridfinityDrawerSpacer was called with correct params
        call_kwargs = mock_spacer_class.call_args[1]
        assert call_kwargs["thickness"] == 5.0
        assert call_kwargs["tolerance"] == 1.0
        assert call_kwargs["chamf_rad"] == 1.0
        assert call_kwargs["show_arrows"] is True
        assert call_kwargs["align_features"] is True

    @patch("gridfinity_tools.core.spacer_generator.GridfinityDrawerSpacer")
    def test_spacer_params_custom(self, mock_spacer_class: MagicMock) -> None:
        """Test custom parameters passed to GridfinityDrawerSpacer."""
        mock_instance = MagicMock()
        mock_spacer_class.return_value = mock_instance

        gen = SpacerGenerator(
            330.0,
            340.0,
            thickness_mm=3.0,
            tolerance_mm=0.5,
            chamfer_mm=0.8,
            show_arrows=False,
            align_features=False,
            verbose=True,
        )
        gen.generate_half_set()

        # Check that GridfinityDrawerSpacer was called with correct params
        call_kwargs = mock_spacer_class.call_args[1]
        assert call_kwargs["thickness"] == 3.0
        assert call_kwargs["tolerance"] == 0.5
        assert call_kwargs["chamf_rad"] == 0.8
        assert call_kwargs["show_arrows"] is False
        assert call_kwargs["align_features"] is False
        assert call_kwargs["verbose"] is True
