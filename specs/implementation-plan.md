# Gridfinity Tools - Implementation Plan

## Project Overview
CLI application for generating Gridfinity baseplates and drawer spacers using the cqgridfinity library.

## Technology Stack
- **Language**: Python 3.12+
- **CLI Framework**: Click 8.1+
- **Logging**: Loguru
- **CAD Library**: cqgridfinity 0.5.7+
- **Testing**: pytest with >90% coverage target
- **Linting**: ruff
- **Type Checking**: mypy

## Architecture

```
src/gridfinity_tools/
├── __init__.py                    # Package exports
├── __main__.py                    # CLI entry point
├── cli/                           # CLI layer (Click commands)
│   ├── __init__.py
│   ├── main.py                    # Main CLI group, global options
│   ├── drawer.py                  # drawer command
│   ├── baseplate.py               # baseplate command  
│   └── spacer.py                  # spacer command
├── core/                          # Business logic
│   ├── __init__.py
│   ├── drawer_generator.py        # DrawerGenerator class
│   ├── baseplate_generator.py     # BaseplateGenerator class
│   ├── spacer_generator.py        # SpacerGenerator class
│   └── printer.py                 # PrinterConfig class
├── utils/                         # Utilities
│   ├── __init__.py
│   ├── units.py                   # Unit conversions
│   ├── validation.py              # Input validation
│   ├── naming.py                  # Filename generation
│   └── splitting.py               # Baseplate split calculations
└── constants.py                   # Global constants

tests/
├── __init__.py
├── cli/                           # CLI tests
├── core/                          # Core logic tests
└── utils/                         # Utility tests
```

## Implementation Phases

### Phase 1: Foundation ✅ COMPLETE
**Goal**: Set up project structure, constants, and utilities

#### Step 1.1: Update Dependencies ✅
- [x] Add Click to pyproject.toml
- [x] Add Loguru to pyproject.toml
- [x] Add pytest-cov to dev dependencies
- [x] Run `uv sync --dev` to install dependencies

#### Step 1.2: Create Directory Structure ✅
- [x] Create `src/gridfinity_tools/cli/` directory
- [x] Create `src/gridfinity_tools/core/` directory
- [x] Create `src/gridfinity_tools/utils/` directory
- [x] Create `tests/cli/` directory
- [x] Create `tests/core/` directory
- [x] Create `tests/utils/` directory
- [x] Create `tests/fixtures/` directory

#### Step 1.3: Implement Constants ✅
- [x] Create `src/gridfinity_tools/constants.py`
  - [x] Define GRIDFINITY_UNIT constant (42mm)
  - [x] Define printer presets dictionary
  - [x] Define default values (tolerance, thickness, etc.)
  - [x] Add docstrings

#### Step 1.4: Implement Utils - Units Module ✅
- [x] Create `src/gridfinity_tools/utils/units.py`
  - [x] Implement `inches_to_mm()` function
  - [x] Implement `mm_to_inches()` function
  - [x] Implement `parse_dimension()` function (handles "330", "11.5in")
  - [x] Add comprehensive docstrings with examples
- [x] Create `tests/utils/test_units.py`
  - [x] Test plain number parsing
  - [x] Test inch conversion
  - [x] Test invalid formats
  - [x] Parametrized tests for various inputs
  - [x] Target: 100% coverage ✅ ACHIEVED

#### Step 1.5: Implement Utils - Splitting Module ✅
- [x] Create `src/gridfinity_tools/utils/splitting.py`
  - [x] Implement `calculate_baseplate_split()` function
  - [x] Implement `calculate_baseplate_units()` function
  - [x] Implement `calculate_split_grid()` function
  - [x] Implement `calculate_total_pieces()` function
  - [x] Add comprehensive docstrings
- [x] Create `tests/utils/test_splitting.py`
  - [x] Test single piece (fits in printer)
  - [x] Test split into 2 pieces
  - [x] Test split into multiple pieces
  - [x] Test edge cases (exact fit, 1 unit over)
  - [x] Target: 100% coverage ✅ ACHIEVED

#### Step 1.6: Implement Utils - Naming Module ✅
- [x] Create `src/gridfinity_tools/utils/naming.py`
  - [x] Implement `generate_spacer_filename()` function
  - [x] Implement `generate_baseplate_filename()` function
  - [x] Implement `generate_assembly_filename()` function
  - [x] Implement `add_path_to_filename()` function
  - [x] Handle optional parameters (tolerance, screws, etc.)
  - [x] Add comprehensive docstrings
- [x] Create `tests/utils/test_naming.py`
  - [x] Test spacer filename with default params
  - [x] Test spacer filename with custom tolerance
  - [x] Test baseplate filename with/without screws
  - [x] Test assembly filename
  - [x] Target: 100% coverage ✅ ACHIEVED

#### Step 1.7: Implement Utils - Validation Module ✅
- [x] Create `src/gridfinity_tools/utils/validation.py`
  - [x] Implement `validate_positive()` function
  - [x] Implement `validate_drawer_dimensions()` function
  - [x] Implement `validate_baseplate_units()` function
  - [x] Implement `validate_tolerance()` function
  - [x] Implement `validate_printer_dimensions()` function
  - [x] Implement `validate_file_format()` function
  - [x] Add comprehensive docstrings
- [x] Create `tests/utils/test_validation.py`
  - [x] Test positive validation
  - [x] Test drawer dimension validation
  - [x] Test baseplate units validation
  - [x] Test tolerance validation
  - [x] Test printer dimensions validation
  - [x] Test file format validation
  - [x] Target: 100% coverage ✅ ACHIEVED

**Phase 1 Completion Criteria**:
- ✅ All utils modules implemented (5 modules)
- ✅ All utils tests passing (173 tests)
- ✅ 100% coverage on utils layer
- ✅ Type hints validated by mypy
- ✅ Code formatted by ruff
- ✅ Ready for Phase 2

---

### Phase 2: Core Business Logic ✅ COMPLETE
**Goal**: Implement generator classes with business logic

#### Step 2.1: Implement Printer Configuration ✅
- [x] Create `src/gridfinity_tools/core/printer.py`
  - [x] Define `PrinterConfig` dataclass
  - [x] Implement `from_preset()` class method
  - [x] Implement `from_custom()` class method
  - [x] Export PRINTER_PRESETS
  - [x] Add comprehensive docstrings
- [x] Create `tests/core/test_printer.py`
  - [x] Test preset loading (all presets)
  - [x] Test custom printer creation
  - [x] Test invalid preset name
  - [x] Target: 100% coverage ✅ ACHIEVED

#### Step 2.2: Implement Baseplate Generator ✅
- [x] Create `src/gridfinity_tools/core/baseplate_generator.py`
  - [x] Define `BaseplateGenerator` class
  - [x] Implement `__init__()` method
  - [x] Implement `generate()` method
  - [x] Implement `save_stl()`, `save_step()`, `save_svg()` methods
  - [x] Add comprehensive docstrings
- [x] Create `tests/core/test_baseplate_generator.py`
  - [x] Test basic generation
  - [x] Test with corner screws
  - [x] Test with extended depth
  - [x] Test file output (mocked)
  - [x] Target: 100% coverage ✅ ACHIEVED

#### Step 2.3: Implement Spacer Generator ✅
- [x] Create `src/gridfinity_tools/core/spacer_generator.py`
  - [x] Define `SpacerGenerator` class
  - [x] Implement `__init__()` method
  - [x] Implement `generate_half_set()` method
  - [x] Implement `generate_full_assembly()` method
  - [x] Implement `save_stl()` and `save_step()` methods
  - [x] Add comprehensive docstrings
- [x] Create `tests/core/test_spacer_generator.py`
  - [x] Test half set generation
  - [x] Test full assembly generation
  - [x] Test with various options
  - [x] Test file output (mocked)
  - [x] Target: 100% coverage ✅ ACHIEVED

#### Step 2.4: Implement Drawer Generator ⏳
- [ ] Create `src/gridfinity_tools/core/drawer_generator.py`
  - [ ] Define `DrawerGenerator` class
  - [ ] Implement `__init__()` method
  - [ ] Implement `calculate_baseplate_size()` method
  - [ ] Implement `generate_spacers()` method
  - [ ] Implement `generate_baseplates()` method
  - [ ] Implement `generate_all()` method
  - [ ] Add comprehensive docstrings
- [ ] Create `tests/core/test_drawer_generator.py`
  - [ ] Test baseplate size calculation
  - [ ] Test spacer generation
  - [ ] Test baseplate generation (single piece)
  - [ ] Test baseplate generation (split)
  - [ ] Test complete generation
  - [ ] Test file output (mocked)
  - [ ] Target: >90% coverage

**Phase 2 Status**:
- ✅ 3 of 4 core modules implemented
- ✅ 73 core tests passing with 100% coverage
- ✅ Integration with cqgridfinity library working
- ✅ Type hints validated by mypy
- ✅ Code formatted by ruff
- ⏳ Awaiting DrawerGenerator implementation

---

### Phase 3: CLI Layer ⏳
**Goal**: Implement Click-based CLI commands

#### Step 3.1: Setup Logging ⏳
- [ ] Update `src/gridfinity_tools/__init__.py`
  - [ ] Configure loguru logger
  - [ ] Set up log levels
  - [ ] Export version info

#### Step 3.2: Implement Main CLI Group ⏳
- [ ] Create `src/gridfinity_tools/cli/main.py`
  - [ ] Define main CLI group with Click
  - [ ] Add global options (--verbose, --version)
  - [ ] Set up loguru based on verbosity
  - [ ] Add command imports
  - [ ] Add comprehensive help text
- [ ] Update `src/gridfinity_tools/__main__.py`
  - [ ] Import and call main CLI group
  - [ ] Handle exceptions gracefully

#### Step 3.3: Implement Drawer Command ⏳
- [ ] Create `src/gridfinity_tools/cli/drawer.py`
  - [ ] Define `drawer` command with Click
  - [ ] Add all arguments and options
  - [ ] Implement command logic using DrawerGenerator
  - [ ] Add comprehensive help text and examples
  - [ ] Use loguru for output
  - [ ] Handle errors gracefully
- [ ] Create `tests/cli/test_drawer.py`
  - [ ] Test basic invocation
  - [ ] Test with inch dimensions
  - [ ] Test with custom printer
  - [ ] Test with various options
  - [ ] Test error handling
  - [ ] Use Click's CliRunner
  - [ ] Target: >90% coverage

#### Step 3.4: Implement Baseplate Command ⏳
- [ ] Create `src/gridfinity_tools/cli/baseplate.py`
  - [ ] Define `baseplate` command with Click
  - [ ] Add all arguments and options
  - [ ] Implement command logic using BaseplateGenerator
  - [ ] Add comprehensive help text
  - [ ] Use loguru for output
  - [ ] Handle errors gracefully
- [ ] Create `tests/cli/test_baseplate.py`
  - [ ] Test basic invocation
  - [ ] Test with various options
  - [ ] Test error handling
  - [ ] Use Click's CliRunner
  - [ ] Target: >90% coverage

#### Step 3.5: Implement Spacer Command ⏳
- [ ] Create `src/gridfinity_tools/cli/spacer.py`
  - [ ] Define `spacer` command with Click
  - [ ] Add all arguments and options
  - [ ] Implement command logic using SpacerGenerator
  - [ ] Add comprehensive help text
  - [ ] Use loguru for output
  - [ ] Handle errors gracefully
- [ ] Create `tests/cli/test_spacer.py`
  - [ ] Test basic invocation
  - [ ] Test with various render modes
  - [ ] Test error handling
  - [ ] Use Click's CliRunner
  - [ ] Target: >90% coverage

**Phase 3 Completion Criteria**:
- ✅ All CLI commands implemented
- ✅ All CLI tests passing
- ✅ >90% coverage on CLI layer
- ✅ Help text is clear and comprehensive
- ✅ Error messages are user-friendly
- ✅ Loguru integration working
- ✅ Type hints validated by mypy
- ✅ Code formatted by ruff

---

### Phase 4: Integration & Polish ⏳
**Goal**: End-to-end testing, documentation, and final polish

#### Step 4.1: Integration Tests ⏳
- [ ] Create `tests/integration/test_end_to_end.py`
  - [ ] Test complete drawer generation workflow
  - [ ] Test complete baseplate generation workflow
  - [ ] Test complete spacer generation workflow
  - [ ] Verify actual file outputs
  - [ ] Test file naming with different parameters
  - [ ] Use tmp_path fixtures

#### Step 4.2: Coverage Analysis ⏳
- [ ] Run pytest with coverage report
- [ ] Identify gaps below 90% threshold
- [ ] Add missing tests
- [ ] Verify >90% overall coverage

#### Step 4.3: Quality Checks ⏳
- [ ] Run `ruff check .` - fix all issues
- [ ] Run `ruff format .` - format all code
- [ ] Run `mypy src/` - fix all type errors
- [ ] Run `pytest` - all tests passing

#### Step 4.4: Documentation ⏳
- [ ] Update README.md with:
  - [ ] Installation instructions
  - [ ] Quick start examples
  - [ ] Command reference
  - [ ] Example outputs
- [ ] Update AGENTS.md if needed
- [ ] Add docstrings to any missing functions

#### Step 4.5: Final Testing ⏳
- [ ] Manual test: drawer command with IKEA ALEX dimensions
- [ ] Manual test: drawer command with large drawer (split baseplates)
- [ ] Manual test: baseplate command
- [ ] Manual test: spacer command
- [ ] Verify all generated STL files
- [ ] Verify all generated STEP files

**Phase 4 Completion Criteria**:
- ✅ All integration tests passing
- ✅ >90% overall test coverage
- ✅ All quality checks passing
- ✅ Documentation complete
- ✅ Manual testing verified
- ✅ Ready for use

---

## Test Coverage Targets

| Layer | Target | Notes |
|-------|--------|-------|
| Utils | >95% | Pure functions, easy to test |
| Core | >90% | Business logic, mock file I/O |
| CLI | >90% | Use CliRunner, integration style |
| Overall | >90% | Project-wide coverage |

---

## File Naming Conventions

### Spacers
- Pattern: `drawer_{width}x{depth}[_tol{tolerance}]_spacer_{mode}.{ext}`
- Examples:
  - `drawer_330x340_tol1.0_spacer_half_set.stl`
  - `drawer_330x340_spacer_half_set.stl` (default tolerance)
  - `drawer_292x520_tol0.5_spacer_half_set.stl`

### Baseplates
- Pattern: `drawer_{width}x{depth}[_screws]_baseplate_{units_w}x{units_d}.{ext}`
- Examples:
  - `drawer_330x340_baseplate_7x8.stl`
  - `drawer_330x340_screws_baseplate_7x8.stl`
  - `drawer_330x340_baseplate_4x4.stl` (split piece)

### Assembly
- Pattern: `drawer_{width}x{depth}[_tol{tolerance}]_full_assembly.step`
- Examples:
  - `drawer_330x340_full_assembly.step`
  - `drawer_330x340_tol1.0_full_assembly.step`

---

## Printer Presets

| Preset | Name | Max Width | Max Depth |
|--------|------|-----------|-----------|
| `bambu-x1c` | Bambu Lab X1C | 256mm | 256mm |
| `bambu-p1p` | Bambu Lab P1P | 256mm | 256mm |
| `prusa-mk4` | Prusa MK4 | 250mm | 210mm |
| `prusa-mini` | Prusa Mini | 180mm | 180mm |
| `ender3` | Ender 3 | 220mm | 220mm |
| `custom` | Custom | User defined | User defined |

---

## Default Values

| Parameter | Default | Notes |
|-----------|---------|-------|
| Tolerance | 1.0mm | Spacer fit tolerance |
| Thickness | 5.0mm | Spacer thickness |
| Chamfer | 1.0mm | Spacer edge chamfer |
| Printer | bambu-x1c | Default printer preset |
| Output Dir | ./output | Output directory |
| Corner Screws | False | Baseplate corner screws |
| Show Arrows | True | Spacer orientation arrows |
| Align Features | True | Spacer jigsaw features |

---

## Progress Tracking

### Current Phase: Phase 2 - Core Business Logic (3 of 4 steps complete)
### Current Step: 2.4 - Implement Drawer Generator
### Status: ⏳ In Progress

### Completed Phases & Steps
- ✅ Phase 1: Foundation (173 tests, 100% coverage)
  - ✅ Step 1.1-1.7: All utilities implemented and tested
- ⏳ Phase 2: Core Business Logic (partial)
  - ✅ Step 2.1: Printer Configuration (25 tests, 100% coverage)
  - ✅ Step 2.2: Baseplate Generator (23 tests, 100% coverage)
  - ✅ Step 2.3: Spacer Generator (25 tests, 100% coverage)
  - ⏳ Step 2.4: Drawer Generator (pending)

### Overall Progress
- **Total Tests Written**: 246
- **Total Coverage**: 100%
- **Code Quality**: All checks passing (ruff, mypy)

**Legend**:
- ✅ Complete
- ⏳ In Progress
- ❌ Blocked/Issue
- ⬜ Not Started

---

## Notes & Decisions

### 2026-01-06
- **Architecture Decision**: Using modular 3-layer architecture (CLI/Core/Utils)
- **Library Choices**: Click for CLI, Loguru for logging
- **Coverage Target**: 90% overall, >95% for utils
- **File Naming Strategy**: Include parameters to avoid conflicts
- **Default Behavior**: Generate both STL (for printing) and STEP (for reference)

---

## Known Issues & Blockers

None currently.

---

## Future Enhancements (Out of Scope)

- Support for GridfinityBox generation
- Batch generation from config files
- Interactive mode for parameter selection
- Configuration file support (~/.gridfinity-tools.toml)
- Progress indicators for long operations
- Preview/visualization before export
- Web UI for parameter selection
