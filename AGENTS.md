# AGENTS.md - Development Guidelines for Gridfinity Tools

## Project Overview

**gridfinity-tools** is a Python CLI application for generating custom Gridfinity storage solutions using CadQuery. The project is built on top of [cq-gridfinity](https://github.com/michaelgale/cq-gridfinity) and provides tools to create drawer spacers, boxes, baseplates, and other modular organization components.

- **Language**: Python 3.12+
- **Package Manager**: uv (fast Python package installer)
- **CAD Framework**: CadQuery 2.6.1+
- **Core Library**: cqgridfinity 0.5.7+
- **Project Layout**: src-layout (PEP 420 compliant)

## Quick Reference

### Development Commands

```bash
# Setup environment
uv sync --dev                    # Install all dependencies including dev tools

# Code quality
ruff check .                     # Lint code
ruff check --fix .               # Auto-fix linting issues
ruff format .                    # Format code
mypy src/                        # Type check source code

# Testing
pytest                           # Run all tests
pytest tests/test_file.py        # Run specific test file
pytest -k test_name              # Run specific test by name
pytest -v                        # Verbose output

# Running the CLI
python -m gridfinity_tools       # Run as module
gridfinity-tools                 # Run installed CLI command

# Build
uv build                         # Build distribution packages
```

### Project Structure

```
gridfinity-tools/
├── src/
│   └── gridfinity_tools/        # Main package (src-layout)
│       ├── __init__.py          # Package initialization
│       └── __main__.py          # CLI entry point
├── scripts/                     # Example/utility scripts
├── tests/                       # Test directory
├── pyproject.toml               # Project config and dependencies
├── README.md                    # Project documentation
├── AGENTS.md                    # This file
└── .gitignore                   # Git ignore patterns
```

## Code Style Guidelines

### Imports

Follow this import order (enforced by ruff's isort):
1. Standard library imports
2. Third-party imports (cadquery, cqgridfinity, etc.)
3. Local application imports

```python
# Standard library
import sys
from pathlib import Path
from typing import Any

# Third-party
import cadquery as cq
from cqgridfinity import GridfinityBox, GridfinityDrawerSpacer
from cqkit import HasZCoordinateSelector

# Local
from gridfinity_tools.utils import calculate_dimensions
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `GridfinityBox`, `DrawerSpacerGenerator`)
- **Functions/Methods**: snake_case (e.g., `generate_spacer`, `save_stl_file`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `GRIDFINITY_UNIT`, `DEFAULT_TOLERANCE`)
- **Private attributes**: Leading underscore (e.g., `_internal_state`, `_compute_dimensions`)
- **Type variables**: PascalCase with T suffix (e.g., `ModelT`, `DimensionT`)

### Type Hints

**Always use type hints** for function signatures and class attributes.

```python
from typing import Any

def generate_spacer(
    width: float,
    depth: float,
    thickness: float = 5.0,
    verbose: bool = False,
) -> GridfinityDrawerSpacer:
    """Generate a drawer spacer with specified dimensions.
    
    Args:
        width: Drawer width in millimeters
        depth: Drawer depth in millimeters
        thickness: Spacer thickness in millimeters (default: 5.0)
        verbose: Enable verbose output (default: False)
        
    Returns:
        Configured GridfinityDrawerSpacer object
    """
    spacer = GridfinityDrawerSpacer(width, depth, thickness=thickness, verbose=verbose)
    return spacer


class DrawerConfig:
    """Configuration for drawer spacer generation."""
    
    def __init__(self, width: float, depth: float) -> None:
        self.width: float = width
        self.depth: float = depth
```

### Formatting

- **Line length**: 100 characters (configured in ruff)
- **Indentation**: 4 spaces (no tabs)
- **String quotes**: Use double quotes `"` for strings (ruff default)
- **Trailing commas**: Use in multi-line structures
- **Blank lines**: Two blank lines between top-level definitions, one within classes

### Docstrings

Use Google-style docstrings for all public functions and classes:

```python
def create_box(
    length: int,
    width: int,
    height: int,
    holes: bool = False,
) -> GridfinityBox:
    """Create a Gridfinity box with specified dimensions.
    
    Args:
        length: Box length in Gridfinity units (1U = 42mm)
        width: Box width in Gridfinity units
        height: Box height in Gridfinity units (1U = 7mm)
        holes: Add magnet holes to bottom (default: False)
        
    Returns:
        Configured GridfinityBox object ready to render
        
    Raises:
        ValueError: If dimensions are less than minimum (1x1x1)
        
    Example:
        >>> box = create_box(3, 2, 5, holes=True)
        >>> box.save_stl_file("my_box.stl")
    """
    if length < 1 or width < 1 or height < 1:
        raise ValueError("Dimensions must be at least 1x1x1")
    return GridfinityBox(length, width, height, holes=holes)
```

### Error Handling

- Use specific exception types
- Provide clear, actionable error messages
- Don't catch exceptions unless you can handle them meaningfully

```python
def save_model(model: Any, filename: str, format_type: str = "stl") -> None:
    """Save CAD model to file.
    
    Args:
        model: CadQuery model object
        filename: Output filename
        format_type: File format ("stl", "step", or "svg")
        
    Raises:
        ValueError: If format_type is not supported
        IOError: If file cannot be written
    """
    valid_formats = {"stl", "step", "svg"}
    if format_type.lower() not in valid_formats:
        raise ValueError(
            f"Unsupported format '{format_type}'. "
            f"Must be one of: {', '.join(valid_formats)}"
        )
    
    try:
        # Save logic here
        pass
    except OSError as e:
        raise IOError(f"Failed to write file '{filename}': {e}") from e
```

## CadQuery-Specific Guidelines

### Working with CadQuery Objects

```python
import cadquery as cq

# Type hint CadQuery objects with cq.Workplane
def create_base_shape(size: float) -> cq.Workplane:
    """Create a basic shape."""
    return cq.Workplane("XY").box(size, size, size)

# Chain operations clearly
box = (
    cq.Workplane("XY")
    .box(42, 42, 7)
    .edges("|Z")
    .fillet(2)
)
```

### File Export Best Practices

```python
from pathlib import Path

# Use Path for file operations
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Export with meaningful names
def export_model(model: cq.Workplane, name: str, output_dir: Path) -> None:
    """Export model in multiple formats."""
    base_path = output_dir / name
    
    cq.exporters.export(model, str(base_path.with_suffix(".step")))
    cq.exporters.export(model, str(base_path.with_suffix(".stl")))
```

## Testing Guidelines

### Test Structure

```python
"""Test drawer spacer generation."""

import pytest
from gridfinity_tools.spacer import generate_spacer


class TestDrawerSpacer:
    """Tests for drawer spacer generation."""
    
    def test_spacer_basic_dimensions(self) -> None:
        """Test spacer with basic dimensions."""
        spacer = generate_spacer(220, 425)
        assert spacer.width == 220
        assert spacer.depth == 425
    
    def test_spacer_invalid_dimensions(self) -> None:
        """Test spacer with invalid dimensions."""
        with pytest.raises(ValueError, match="must be positive"):
            generate_spacer(-10, 425)
    
    @pytest.mark.parametrize("width,depth", [
        (220, 425),
        (300, 400),
        (582, 481),
    ])
    def test_spacer_various_sizes(self, width: float, depth: float) -> None:
        """Test spacer generation with various sizes."""
        spacer = generate_spacer(width, depth)
        assert spacer is not None
```

### Test Files

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Mirror the source structure (e.g., `tests/test_spacer.py` for `src/gridfinity_tools/spacer.py`)

## Git Workflow

### Commit Messages

Use conventional commit format:

```
type(scope): brief description

Longer description if needed

- Bullet points for details
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(spacer): add support for custom tolerance values
fix(export): handle missing output directory
docs(readme): update installation instructions
```

### Branch Strategy

- `main`: Stable release branch
- `develop`: Development branch
- `feature/name`: New features
- `fix/name`: Bug fixes

## Dependencies

### Core Dependencies

- `cadquery>=2.6.1` - Parametric 3D CAD modeling (requires 2.6.1+ for ARM macOS support)
- `cqgridfinity>=0.5.7` - Gridfinity component library
- `cqkit>=0.5.6` - CadQuery helper utilities

### Development Dependencies

- `ruff>=0.8.0` - Fast Python linter and formatter
- `mypy>=1.13.0` - Static type checker
- `pytest>=8.0.0` - Testing framework

## Resources

### Documentation

- [cq-gridfinity Documentation](https://github.com/michaelgale/cq-gridfinity/blob/main/README.md)
- [CadQuery Documentation](https://cadquery.readthedocs.io/)
- [Gridfinity System](https://gridfinity.xyz)
- [Gridfinity Unofficial Wiki](https://gridfinity.xyz)

### Tools

- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)

## Common Patterns

### Creating Gridfinity Components

```python
from cqgridfinity import GridfinityBox, GridfinityBaseplate, GridfinityDrawerSpacer

# Create a simple box
box = GridfinityBox(3, 2, 5, holes=True, scoops=True, labels=True)
box.save_stl_file("output/box.stl")

# Create a baseplate
baseplate = GridfinityBaseplate(4, 3, corner_screws=True)
baseplate.save_step_file("output/baseplate.step")

# Create drawer spacers
spacer = GridfinityDrawerSpacer(220, 425, verbose=True)
spacer.render_half_set()
spacer.save_stl_file("output/spacer_half_set.stl")
```

### Unit Conversions

```python
# Gridfinity uses millimeters
GRIDFINITY_BASE_UNIT = 42  # 1U = 42mm
GRIDFINITY_HEIGHT_UNIT = 7  # 1U height = 7mm

def inches_to_mm(inches: float) -> float:
    """Convert inches to millimeters."""
    return inches * 25.4

# Example: IKEA ALEX drawer
drawer_width = inches_to_mm(11.5)  # 292.1mm
drawer_depth = inches_to_mm(20.5)  # 520.7mm
```

## Notes for AI Coding Agents

- Never include "Generated with" or "Co-authored by" OpenCode/AI in commits or PRs
- Always run `ruff check` and `mypy` before committing
- Use type hints for all new code
- Write tests for new functionality
- Update README.md if adding new features or commands
- Export CAD files (STL, STEP, SVG) are gitignored - don't commit them
- The cqgridfinity library has some type inconsistencies - ignore missing imports for it in mypy
