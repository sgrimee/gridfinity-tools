"""Tests for __main__ module."""

from unittest.mock import patch

from gridfinity_tools.__main__ import main


class TestMainEntry:
    """Tests for main entry point."""

    @patch("gridfinity_tools.__main__.cli")
    def test_main_calls_cli(self, mock_cli: object) -> None:
        """Test that main calls the CLI."""
        result = main()

        assert result == 0
        # Verify cli was called
        assert callable(mock_cli)

    @patch("gridfinity_tools.__main__.cli")
    def test_main_with_cli_error(self, mock_cli: object) -> None:
        """Test that main handles SystemExit from CLI."""
        with patch("gridfinity_tools.__main__.cli") as mock_cli_func:
            mock_cli_func.side_effect = SystemExit(1)
            result = main()

            assert result == 1

    @patch("gridfinity_tools.__main__.cli")
    def test_main_with_non_int_exit_code(self, mock_cli: object) -> None:
        """Test that main handles non-int SystemExit codes."""
        with patch("gridfinity_tools.__main__.cli") as mock_cli_func:
            mock_cli_func.side_effect = SystemExit("error")
            result = main()

            assert result == 1
