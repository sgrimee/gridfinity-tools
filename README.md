# Gridfinity Tools

[![CI](https://github.com/sgrimee/gridfinity-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/sgrimee/gridfinity-tools/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

CLI tools for generating custom Gridfinity storage solutions using CadQuery.

## Overview

This project provides command-line tools to generate Gridfinity-compatible storage components for drawers and workspaces. Built on top of [cq-gridfinity](https://github.com/michaelgale/cq-gridfinity), it allows you to create custom drawer spacers and baseplates tailored to your specific dimensions.

## Installation

```bash
# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Usage

```bash
# Show available commands
gridfinity-tools --help
```

### Generate a Complete Drawer Solution

The `drawer` command creates spacers and baseplate(s) optimized for your drawer and printer:

```bash
# 330x340mm drawer with default Bambu X1C printer
gridfinity-tools drawer 330 340

# IKEA ALEX drawer (supports inches)
gridfinity-tools drawer 11.5in 20.5in

# Custom printer and options
gridfinity-tools drawer 330 340 -p prusa-mk4 --corner-screws
```

### Generate Individual Components

```bash
# Baseplate (dimensions in Gridfinity units, 1U = 42mm)
gridfinity-tools baseplate 7 8

# Spacers only
gridfinity-tools spacer 330 340 -m full_set
```

### Supported Printers

- `bambu-x1c` (default)
- `bambu-p1p`
- `prusa-mk4`
- `prusa-mini`
- `ender3`

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

## Documentation

- [cq-gridfinity](https://github.com/michaelgale/cq-gridfinity) - Underlying CAD library
- [Gridfinity](https://gridfinity.xyz) - The modular storage system

## License

[MIT](LICENSE)
