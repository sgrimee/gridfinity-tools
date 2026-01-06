"""Tests for spacer CLI command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from gridfinity_tools.cli.spacer import spacer_command


class TestSpacerCommandBasic:
    """Tests for basic spacer command execution."""

    def test_spacer_command_help(self) -> None:
        """Test spacer command help text."""
        runner = CliRunner()
        result = runner.invoke(spacer_command, ["--help"])

        assert result.exit_code == 0
        assert "drawer spacer" in result.output

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_basic(self, mock_gen_class: MagicMock) -> None:
        """Test basic spacer command execution."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340"])

        assert result.exit_code == 0
        assert "✨ Generation complete!" in result.output
        assert "Spacer dimensions: 330.0 × 340.0 mm" in result.output
        assert "Print this file twice" in result.output
        mock_instance.save_stl.assert_called_once()

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_full_set_mode(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with full_set mode."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340", "-m", "full_set"])

        assert result.exit_code == 0
        mock_instance.save_stl.assert_called_once()
        # Verify render_mode was passed
        call_args = mock_instance.save_stl.call_args
        assert call_args.kwargs["render_mode"] == "full_set"

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_step_format(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with STEP format."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340", "-f", "step"])

        assert result.exit_code == 0
        mock_instance.save_step.assert_called_once()

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_with_custom_tolerance(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with custom tolerance."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340", "-t", "0.5"])

        assert result.exit_code == 0
        # Verify tolerance was passed
        call_kwargs = mock_gen_class.call_args.kwargs
        assert call_kwargs["tolerance_mm"] == 0.5

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_with_options(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with multiple options."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                spacer_command,
                ["330", "340", "-m", "full_assembly", "-f", "step", "--no-arrows", "--no-align"],
            )

        assert result.exit_code == 0
        # Verify options were passed
        call_kwargs = mock_gen_class.call_args.kwargs
        assert call_kwargs["show_arrows"] is False
        assert call_kwargs["align_features"] is False


class TestSpacerCommandDimensions:
    """Tests for spacer command dimension handling."""

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_inches_input(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with inches input."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["11.5in", "20.5in"])

        assert result.exit_code == 0
        # Verify inches were converted to mm
        call_args = mock_gen_class.call_args
        assert abs(call_args.kwargs["width_mm"] - 292.1) < 0.2
        assert abs(call_args.kwargs["depth_mm"] - 520.7) < 0.2

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_fractional_dimensions(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with fractional dimensions."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["292.1", "520.7"])

        assert result.exit_code == 0
        # Verify dimensions were parsed correctly
        call_args = mock_gen_class.call_args
        assert call_args.kwargs["width_mm"] == 292.1
        assert call_args.kwargs["depth_mm"] == 520.7


class TestSpacerCommandOutput:
    """Tests for spacer command output."""

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_half_set_message(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command shows half_set message."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340", "-m", "half_set"])

        assert result.exit_code == 0
        assert "Print this file twice" in result.output

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_full_set_no_message(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command doesn't show half_set message for full_set."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340", "-m", "full_set"])

        assert result.exit_code == 0
        assert "Print this file twice" not in result.output

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_custom_output_dir(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command with custom output directory."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(spacer_command, ["330", "340", "-o", "my_spacers"])

            assert result.exit_code == 0
            assert Path("my_spacers").exists()


class TestSpacerCommandErrors:
    """Tests for spacer command error handling."""

    def test_spacer_command_missing_arguments(self) -> None:
        """Test spacer command with missing arguments."""
        runner = CliRunner()
        result = runner.invoke(spacer_command, [])

        assert result.exit_code != 0

    def test_spacer_command_invalid_width(self) -> None:
        """Test spacer command with invalid width."""
        runner = CliRunner()
        result = runner.invoke(spacer_command, ["invalid", "340"])

        assert result.exit_code != 0

    def test_spacer_command_zero_dimensions(self) -> None:
        """Test spacer command with zero dimensions."""
        runner = CliRunner()
        result = runner.invoke(spacer_command, ["0", "340"])

        assert result.exit_code != 0

    @patch("gridfinity_tools.cli.spacer.SpacerGenerator")
    def test_spacer_command_generation_error(self, mock_gen_class: MagicMock) -> None:
        """Test spacer command handles generation errors."""
        mock_gen_class.side_effect = ValueError("Invalid dimensions")

        runner = CliRunner()
        result = runner.invoke(spacer_command, ["330", "340"])

        assert result.exit_code == 1
        assert "❌ Error" in result.output
