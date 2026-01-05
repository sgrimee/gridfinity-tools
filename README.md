# Gridfinity Tools

CLI tools for generating custom Gridfinity storage solutions using CadQuery.

## Overview

This project provides command-line tools to generate Gridfinity-compatible storage components for drawers and workspaces. Built on top of [cq-gridfinity](https://github.com/michaelgale/cq-gridfinity), it allows you to create custom drawer spacers, boxes, and baseplates tailored to your specific dimensions.

## Installation

```bash
# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

## Development

```bash
# Install with dev dependencies
uv sync --dev

# Run linting
ruff check .

# Run type checking
mypy src/

# Run tests
pytest
```

## Usage

```bash
# Run the CLI
python -m gridfinity_tools

# Or after installation
gridfinity-tools
```

## Scripts

The `scripts/` directory contains example scripts for generating specific components.

## Documentation

For more information about Gridfinity and the underlying library:
- [cq-gridfinity Documentation](https://github.com/michaelgale/cq-gridfinity/blob/main/README.md)
- [Gridfinity System](https://gridfinity.xyz)

## License

MIT
