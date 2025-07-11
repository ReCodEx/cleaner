# Migration to pyproject.toml

This project has been migrated from the legacy `setup.py` to the modern `pyproject.toml` build system following PEP 518/621 standards.

## Installation

### For users:

```bash
# Install the package
pip install .

# Install system files (Linux/Unix only)
python install_system_files.py
```

### For developers:

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]
```

## What changed:

1. **`setup.py`** is now deprecated in favor of **`pyproject.toml`**
2. **`install_system_files.py`** handles platform-specific file installation
3. Modern build backend using setuptools with declarative configuration
4. Dynamic version resolution from `cleaner.__version__`

## Build and Distribution

```bash
# Build source and wheel distributions
pip install build
python -m build

# Install from wheel
pip install dist/recodex_cleaner-*.whl
```

The migration maintains backward compatibility while providing a cleaner, more standard Python packaging experience.
