"""Printer configuration management."""

from dataclasses import dataclass

from gridfinity_tools.constants import PRINTER_PRESETS


@dataclass
class PrinterConfig:
    """Printer build volume configuration.

    Attributes:
        name: Printer model name
        max_width_mm: Maximum print width in millimeters
        max_depth_mm: Maximum print depth in millimeters
    """

    name: str
    max_width_mm: float
    max_depth_mm: float

    @classmethod
    def from_preset(cls, preset: str) -> "PrinterConfig":
        """Create printer config from preset name.

        Args:
            preset: Preset name (e.g., "bambu-x1c", "prusa-mk4")

        Returns:
            PrinterConfig instance

        Raises:
            ValueError: If preset name is not recognized

        Examples:
            >>> config = PrinterConfig.from_preset("bambu-x1c")
            >>> config.name
            'Bambu Lab X1C'
            >>> config.max_width_mm
            256
        """
        if preset not in PRINTER_PRESETS:
            valid = ", ".join(sorted(PRINTER_PRESETS.keys()))
            raise ValueError(f"Unknown printer preset '{preset}', must be one of: {valid}")

        name, width, depth = PRINTER_PRESETS[preset]
        return cls(name=name, max_width_mm=width, max_depth_mm=depth)

    @classmethod
    def from_custom(cls, name: str, max_width_mm: float, max_depth_mm: float) -> "PrinterConfig":
        """Create custom printer config.

        Args:
            name: Printer model name
            max_width_mm: Maximum print width in millimeters
            max_depth_mm: Maximum print depth in millimeters

        Returns:
            PrinterConfig instance

        Examples:
            >>> config = PrinterConfig.from_custom("My Printer", 300, 300)
            >>> config.name
            'My Printer'
        """
        return cls(name=name, max_width_mm=max_width_mm, max_depth_mm=max_depth_mm)

    def __str__(self) -> str:
        """Return user-friendly string representation.

        Returns:
            Formatted string with printer info

        Examples:
            >>> config = PrinterConfig.from_preset("bambu-x1c")
            >>> str(config)
            'Bambu Lab X1C (256mm × 256mm)'
        """
        return f"{self.name} ({self.max_width_mm}mm × {self.max_depth_mm}mm)"
