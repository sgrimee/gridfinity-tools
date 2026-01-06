"""CLI entry point for gridfinity-tools."""

import sys

from gridfinity_tools.cli.main import cli


def main() -> int:
    """Main CLI entry point."""
    try:
        cli()
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1


if __name__ == "__main__":
    sys.exit(main())
