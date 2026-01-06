"""Tests for drawer CLI command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from gridfinity_tools.cli.drawer import drawer_command


class TestDrawerCommandBasic:
    """Tests for basic drawer command execution."""

    def test_drawer_command_help(self) -> None:
        """Test drawer command help text."""
        runner = CliRunner()
        result = runner.invoke(drawer_command, ["--help"])

        assert result.exit_code == 0
        assert "Generate a complete drawer solution" in result.output

    @patch("gridfinity_tools.cli.drawer.DrawerGenerator")
    def test_drawer_command_basic(self, mock_gen_class: MagicMock, tmp_path: Path) -> None:
        """Test basic drawer command execution."""
        mock_instance = MagicMock()
        mock_instance.get_solution.return_value = MagicMock(
            baseplate_layout=MagicMock(is_split=False, total_pieces=1)
        )
        mock_instance.save_all.return_value = {
            "spacers": [tmp_path / "spacer1.stl", tmp_path / "spacer2.step"],
            "baseplates": [tmp_path / "baseplate.stl"],
        }
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(drawer_command, ["330", "340"])

        assert result.exit_code == 0
        assert "✨ Generation complete!" in result.output
        assert "Drawer dimensions: 330.0 × 340.0 mm" in result.output

    @patch("gridfinity_tools.cli.drawer.DrawerGenerator")
    def test_drawer_command_with_options(self, mock_gen_class: MagicMock, tmp_path: Path) -> None:
        """Test drawer command with custom options."""
        mock_instance = MagicMock()
        mock_instance.get_solution.return_value = MagicMock(
            baseplate_layout=MagicMock(is_split=False, total_pieces=1)
        )
        mock_instance.save_all.return_value = {"spacers": [], "baseplates": []}
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                drawer_command,
                [
                    "330",
                    "340",
                    "-p",
                    "prusa-mk4",
                    "-t",
                    "0.5",
                    "--corner-screws",
                    "--no-arrows",
                ],
            )

        assert result.exit_code == 0
        # Verify options were passed to DrawerGenerator
        call_kwargs = mock_gen_class.call_args.kwargs
        assert call_kwargs["tolerance_mm"] == 0.5
        assert call_kwargs["corner_screws"] is True
        assert call_kwargs["show_arrows"] is False

    def test_drawer_command_invalid_width(self) -> None:
        """Test drawer command with invalid width."""
        runner = CliRunner()
        result = runner.invoke(drawer_command, ["invalid", "340"])

        assert result.exit_code != 0

    def test_drawer_command_dimension_inches(self) -> None:
        """Test drawer command with inches input."""
        runner = CliRunner()
        with (
            runner.isolated_filesystem(),
            patch("gridfinity_tools.cli.drawer.DrawerGenerator") as mock_gen,
        ):
            mock_instance = MagicMock()
            mock_instance.get_solution.return_value = MagicMock(
                baseplate_layout=MagicMock(is_split=False, total_pieces=1)
            )
            mock_instance.save_all.return_value = {"spacers": [], "baseplates": []}
            mock_gen.return_value = mock_instance

            result = runner.invoke(drawer_command, ["11.5in", "20.5in"])

            assert result.exit_code == 0
            # Verify inches were converted to mm (11.5in ≈ 291.1mm, 20.5in ≈ 520.7mm)
            call_args = mock_gen.call_args
            assert abs(call_args.kwargs["width_mm"] - 292.1) < 0.2
            assert abs(call_args.kwargs["depth_mm"] - 520.7) < 0.2


class TestDrawerCommandOutput:
    """Tests for drawer command output formatting."""

    @patch("gridfinity_tools.cli.drawer.DrawerGenerator")
    def test_drawer_command_split_warning(self, mock_gen_class: MagicMock) -> None:
        """Test drawer command shows split warning."""
        mock_instance = MagicMock()
        mock_instance.get_solution.return_value = MagicMock(
            baseplate_layout=MagicMock(is_split=True, total_pieces=4)
        )
        mock_instance.save_all.return_value = {"spacers": [], "baseplates": []}
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(drawer_command, ["500", "500"])

        assert result.exit_code == 0
        assert "will be split into 4 pieces" in result.output

    @patch("gridfinity_tools.cli.drawer.DrawerGenerator")
    def test_drawer_command_output_directory_creation(self, mock_gen_class: MagicMock) -> None:
        """Test drawer command creates output directory."""
        mock_instance = MagicMock()
        mock_instance.get_solution.return_value = MagicMock(
            baseplate_layout=MagicMock(is_split=False, total_pieces=1)
        )
        mock_instance.save_all.return_value = {"spacers": [], "baseplates": []}
        mock_gen_class.return_value = mock_instance

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(drawer_command, ["330", "340", "-o", "my_output"])

            assert result.exit_code == 0
            assert Path("my_output").exists()


class TestDrawerCommandErrors:
    """Tests for drawer command error handling."""

    def test_drawer_command_zero_dimensions(self) -> None:
        """Test drawer command with zero dimensions."""
        runner = CliRunner()
        result = runner.invoke(drawer_command, ["0", "340"])

        assert result.exit_code != 0
        assert "❌ Error" in result.output

    def test_drawer_command_negative_dimensions(self) -> None:
        """Test drawer command with negative dimensions."""
        runner = CliRunner()
        result = runner.invoke(drawer_command, ["-330", "340"])

        assert result.exit_code != 0

    def test_drawer_command_invalid_printer(self) -> None:
        """Test drawer command with invalid printer preset."""
        runner = CliRunner()
        result = runner.invoke(drawer_command, ["330", "340", "-p", "nonexistent"])

        assert result.exit_code != 0

    @patch("gridfinity_tools.cli.drawer.DrawerGenerator")
    def test_drawer_command_generation_error(self, mock_gen_class: MagicMock) -> None:
        """Test drawer command handles generation errors."""
        mock_gen_class.side_effect = ValueError("Test error")

        runner = CliRunner()
        result = runner.invoke(drawer_command, ["330", "340"])

        assert result.exit_code == 1
        assert "❌ Error" in result.output
        assert "Test error" in result.output
