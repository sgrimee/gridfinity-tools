"""Tests for main CLI module."""

from click.testing import CliRunner

from gridfinity_tools.cli.main import cli


class TestMainCLI:
    """Tests for main CLI group."""

    def test_cli_help(self) -> None:
        """Test main CLI help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Gridfinity Tools" in result.output
        assert "Commands:" in result.output

    def test_cli_version(self) -> None:
        """Test main CLI version."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_drawer_command_available(self) -> None:
        """Test drawer command is available in CLI group."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert "drawer" in result.output

    def test_cli_baseplate_command_available(self) -> None:
        """Test baseplate command is available in CLI group."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert "baseplate" in result.output

    def test_cli_spacer_command_available(self) -> None:
        """Test spacer command is available in CLI group."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert "spacer" in result.output

    def test_cli_invalid_command(self) -> None:
        """Test CLI with invalid command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["invalid"])

        assert result.exit_code != 0
