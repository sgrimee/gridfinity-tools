"""Tests for baseplate CLI command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from gridfinity_tools.cli.baseplate import baseplate_command


class TestBaseplateCommandBasic:
    """Tests for basic baseplate command execution."""

    def test_baseplate_command_help(self) -> None:
        """Test baseplate command help text."""
        runner = CliRunner()
        result = runner.invoke(baseplate_command, ["--help"])

        assert result.exit_code == 0
        assert "Gridfinity baseplate" in result.output

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_basic(self, mock_gen_class: MagicMock, tmp_path: Path) -> None:
        """Test basic baseplate command execution."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(baseplate_command, ["7", "8"])

        assert result.exit_code == 0
        assert "✨ Generation complete!" in result.output
        assert "Baseplate dimensions: 7×8 units (294×336 mm)" in result.output
        mock_instance.save_stl.assert_called_once()

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_step_format(self, mock_gen_class: MagicMock) -> None:
        """Test baseplate command with STEP format."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(baseplate_command, ["7", "8", "-f", "step"])

        assert result.exit_code == 0
        mock_instance.save_step.assert_called_once()

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_svg_format(self, mock_gen_class: MagicMock) -> None:
        """Test baseplate command with SVG format."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(baseplate_command, ["7", "8", "-f", "svg"])

        assert result.exit_code == 0
        mock_instance.save_svg.assert_called_once()

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_with_corner_screws(self, mock_gen_class: MagicMock) -> None:
        """Test baseplate command with corner screws."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(baseplate_command, ["7", "8", "--corner-screws"])

        assert result.exit_code == 0
        # Verify corner_screws was passed
        call_kwargs = mock_gen_class.call_args.kwargs
        assert call_kwargs["corner_screws"] is True


class TestBaseplateCommandOutput:
    """Tests for baseplate command output."""

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_filename_generation(self, mock_gen_class: MagicMock) -> None:
        """Test baseplate command generates correct filenames."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(baseplate_command, ["7", "8", "-f", "stl"])

        assert result.exit_code == 0
        # Verify filename is in output
        assert "drawer" in result.output
        assert ".stl" in result.output

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_custom_output_dir(self, mock_gen_class: MagicMock) -> None:
        """Test baseplate command with custom output directory."""
        mock_instance = MagicMock()
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(baseplate_command, ["7", "8", "-o", "my_output"])

            assert result.exit_code == 0
            assert Path("my_output").exists()


class TestBaseplateCommandErrors:
    """Tests for baseplate command error handling."""

    def test_baseplate_command_missing_arguments(self) -> None:
        """Test baseplate command with missing arguments."""
        runner = CliRunner()
        result = runner.invoke(baseplate_command, [])

        assert result.exit_code != 0

    def test_baseplate_command_invalid_width(self) -> None:
        """Test baseplate command with invalid width."""
        runner = CliRunner()
        result = runner.invoke(baseplate_command, ["invalid", "8"])

        assert result.exit_code != 0

    def test_baseplate_command_zero_width(self) -> None:
        """Test baseplate command with zero width."""
        runner = CliRunner()
        result = runner.invoke(baseplate_command, ["0", "8"])

        assert result.exit_code != 0

    @patch("gridfinity_tools.cli.baseplate.BaseplateGenerator")
    def test_baseplate_command_generation_error(self, mock_gen_class: MagicMock) -> None:
        """Test baseplate command handles generation errors."""
        mock_gen_class.side_effect = ValueError("Invalid dimensions")

        runner = CliRunner()
        result = runner.invoke(baseplate_command, ["7", "8"])

        assert result.exit_code == 1
        assert "❌ Error" in result.output
