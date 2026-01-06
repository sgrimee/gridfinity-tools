"""Tests for printer configuration."""

import pytest

from gridfinity_tools.core.printer import PrinterConfig


class TestPrinterConfigFromPreset:
    """Tests for PrinterConfig.from_preset class method."""

    def test_bambu_x1c_preset(self) -> None:
        """Test loading Bambu Lab X1C preset."""
        config = PrinterConfig.from_preset("bambu-x1c")
        assert config.name == "Bambu Lab X1C"
        assert config.max_width_mm == 256
        assert config.max_depth_mm == 256

    def test_bambu_p1p_preset(self) -> None:
        """Test loading Bambu Lab P1P preset."""
        config = PrinterConfig.from_preset("bambu-p1p")
        assert config.name == "Bambu Lab P1P"
        assert config.max_width_mm == 256
        assert config.max_depth_mm == 256

    def test_prusa_mk4_preset(self) -> None:
        """Test loading Prusa MK4 preset."""
        config = PrinterConfig.from_preset("prusa-mk4")
        assert config.name == "Prusa MK4"
        assert config.max_width_mm == 250
        assert config.max_depth_mm == 210

    def test_prusa_mini_preset(self) -> None:
        """Test loading Prusa Mini preset."""
        config = PrinterConfig.from_preset("prusa-mini")
        assert config.name == "Prusa Mini"
        assert config.max_width_mm == 180
        assert config.max_depth_mm == 180

    def test_ender3_preset(self) -> None:
        """Test loading Ender 3 preset."""
        config = PrinterConfig.from_preset("ender3")
        assert config.name == "Ender 3"
        assert config.max_width_mm == 220
        assert config.max_depth_mm == 220

    def test_invalid_preset_name(self) -> None:
        """Test invalid preset name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown printer preset"):
            PrinterConfig.from_preset("invalid-printer")

    def test_error_message_includes_valid_options(self) -> None:
        """Test error message includes list of valid presets."""
        with pytest.raises(ValueError, match="bambu-x1c"):
            PrinterConfig.from_preset("unknown")

    @pytest.mark.parametrize(
        "preset",
        ["bambu-x1c", "bambu-p1p", "prusa-mk4", "prusa-mini", "ender3"],
    )
    def test_all_presets_loadable(self, preset: str) -> None:
        """Test that all known presets can be loaded."""
        config = PrinterConfig.from_preset(preset)
        assert config.name
        assert config.max_width_mm > 0
        assert config.max_depth_mm > 0


class TestPrinterConfigFromCustom:
    """Tests for PrinterConfig.from_custom class method."""

    def test_create_custom_config(self) -> None:
        """Test creating custom printer config."""
        config = PrinterConfig.from_custom("My Printer", 300.0, 250.0)
        assert config.name == "My Printer"
        assert config.max_width_mm == 300.0
        assert config.max_depth_mm == 250.0

    def test_custom_config_with_large_dimensions(self) -> None:
        """Test custom config with large dimensions."""
        config = PrinterConfig.from_custom("Large Printer", 500.0, 500.0)
        assert config.max_width_mm == 500.0
        assert config.max_depth_mm == 500.0

    def test_custom_config_with_min_dimensions(self) -> None:
        """Test custom config with minimum dimensions."""
        config = PrinterConfig.from_custom("Small Printer", 42.0, 42.0)
        assert config.max_width_mm == 42.0
        assert config.max_depth_mm == 42.0

    def test_custom_config_with_fractional_dimensions(self) -> None:
        """Test custom config with fractional dimensions."""
        config = PrinterConfig.from_custom("Precise Printer", 256.5, 210.3)
        assert config.max_width_mm == 256.5
        assert config.max_depth_mm == 210.3


class TestPrinterConfigDataclass:
    """Tests for PrinterConfig dataclass properties."""

    def test_direct_instantiation(self) -> None:
        """Test direct instantiation of PrinterConfig."""
        config = PrinterConfig(name="Test Printer", max_width_mm=250.0, max_depth_mm=210.0)
        assert config.name == "Test Printer"
        assert config.max_width_mm == 250.0
        assert config.max_depth_mm == 210.0

    def test_equality(self) -> None:
        """Test equality comparison of configs."""
        config1 = PrinterConfig(name="Printer", max_width_mm=256.0, max_depth_mm=256.0)
        config2 = PrinterConfig(name="Printer", max_width_mm=256.0, max_depth_mm=256.0)
        assert config1 == config2

    def test_inequality(self) -> None:
        """Test inequality comparison of configs."""
        config1 = PrinterConfig(name="Printer1", max_width_mm=256.0, max_depth_mm=256.0)
        config2 = PrinterConfig(name="Printer2", max_width_mm=256.0, max_depth_mm=256.0)
        assert config1 != config2

    def test_repr(self) -> None:
        """Test repr includes all attributes."""
        config = PrinterConfig(name="Test", max_width_mm=256.0, max_depth_mm=256.0)
        repr_str = repr(config)
        assert "Test" in repr_str
        assert "256" in repr_str


class TestPrinterConfigString:
    """Tests for PrinterConfig.__str__ method."""

    def test_string_representation_bambu(self) -> None:
        """Test string representation for Bambu X1C."""
        config = PrinterConfig.from_preset("bambu-x1c")
        result = str(config)
        assert "Bambu Lab X1C" in result
        assert "256mm" in result

    def test_string_representation_prusa(self) -> None:
        """Test string representation for Prusa MK4."""
        config = PrinterConfig.from_preset("prusa-mk4")
        result = str(config)
        assert "Prusa MK4" in result
        assert "250mm" in result
        assert "210mm" in result

    def test_string_representation_custom(self) -> None:
        """Test string representation for custom printer."""
        config = PrinterConfig.from_custom("Custom Printer", 300.0, 250.0)
        result = str(config)
        assert "Custom Printer" in result
        assert "300" in result
        assert "250" in result
        assert "mm" in result

    def test_string_format_includes_dimensions_marker(self) -> None:
        """Test that string uses dimension marker (×)."""
        config = PrinterConfig.from_preset("bambu-x1c")
        result = str(config)
        assert "×" in result

    def test_string_format_includes_parentheses(self) -> None:
        """Test that dimensions are in parentheses."""
        config = PrinterConfig.from_preset("ender3")
        result = str(config)
        assert "(" in result
        assert ")" in result
