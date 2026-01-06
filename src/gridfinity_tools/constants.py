"""Global constants for gridfinity-tools."""

# Gridfinity specification constants
GRIDFINITY_UNIT = 42  # 1 Gridfinity unit = 42mm
GRIDFINITY_HEIGHT_UNIT = 7  # 1 height unit = 7mm

# Unit conversion constants
MM_PER_INCH = 25.4

# Default values for generation
DEFAULT_TOLERANCE = 1.0  # mm
DEFAULT_SPACER_THICKNESS = 5.0  # mm
DEFAULT_SPACER_CHAMFER = 1.0  # mm
DEFAULT_BASEPLATE_DEPTH = 0.0  # mm (no extended depth)
DEFAULT_SCREW_HOLE_DIAM = 5.0  # mm
DEFAULT_COUNTERSINK_DIAM = 10.0  # mm
DEFAULT_COUNTERSINK_ANGLE = 82  # degrees
DEFAULT_OUTPUT_DIR = "output"

# Spacer defaults
DEFAULT_SHOW_ARROWS = True
DEFAULT_ALIGN_FEATURES = True
DEFAULT_ALIGN_TOLERANCE = 0.15  # mm
DEFAULT_MIN_MARGIN = 4.0  # mm

# File format options
VALID_FORMATS = {"stl", "step", "svg"}
DEFAULT_FORMAT_SPACER = "stl"
DEFAULT_FORMAT_BASEPLATE = "stl"
DEFAULT_FORMAT_ASSEMBLY = "step"

# Printer presets - name: (max_width_mm, max_depth_mm)
PRINTER_PRESETS = {
    "bambu-x1c": ("Bambu Lab X1C", 256, 256),
    "bambu-p1p": ("Bambu Lab P1P", 256, 256),
    "prusa-mk4": ("Prusa MK4", 250, 210),
    "prusa-mini": ("Prusa Mini", 180, 180),
    "ender3": ("Ender 3", 220, 220),
}

DEFAULT_PRINTER = "bambu-x1c"
