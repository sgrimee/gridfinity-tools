# Scripts Directory

This directory contains example scripts for generating Gridfinity components.

## Available Scripts

### `generate_drawer_spacer.py`

Generates drawer spacers for a 220mm x 425mm drawer.

**Usage:**
```bash
.venv/bin/python scripts/generate_drawer_spacer.py
```

**Output:**
- `output/drawer_220x425_spacer_half_set.stl` - Print this twice for a complete set
- `output/drawer_220x425_spacer_full_set.step` - Full assembly for reference

**Customization:**

To generate spacers for different drawer dimensions, edit the script and modify these values:

```python
drawer_width = 220.0   # Change to your drawer width in mm
drawer_depth = 425.0   # Change to your drawer depth in mm
```

You can also adjust:
- `thickness` - Spacer thickness (default: 5.0mm)
- `tolerance` - Gap tolerance (default: 0.5mm)
- `show_arrows` - Display orientation arrows (default: True)
- `align_features` - Add jigsaw interlocking (default: True)

## Creating Your Own Scripts

Use the existing script as a template. The general pattern is:

```python
from cqgridfinity import GridfinityBox, GridfinityBaseplate, GridfinityDrawerSpacer

# Create component
component = GridfinityBox(3, 2, 5, holes=True)

# Render
component.save_stl_file("output/my_box.stl")
```

See [AGENTS.md](../AGENTS.md) for more examples and best practices.
