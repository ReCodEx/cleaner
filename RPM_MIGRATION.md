# RPM Packaging Migration Guide

This document describes the migration of the RPM spec file from legacy `setup.py` to modern `pyproject.toml` build system.

## Changes Made

### Build Requirements
- **Added**: `python3dist(build)` - Modern Python build tool
- **Added**: `python3dist(setuptools) >= 61.0` - Modern setuptools version
- **Added**: `python3-pip python3-wheel` - Required for wheel installation

### Build Process
- **Old**: `%py3_build` (legacy setuptools)
- **New**: `%{python3} -m build --wheel --no-isolation` (PEP 517 build)

### Installation Process
- **Old**: `%py3_install` (legacy setuptools)
- **New**: `%{python3} -m pip install --no-deps --no-index --find-links dist/` (wheel-based)

### File Patterns
- **Old**: `recodex_cleaner-%{version}-py?.?.egg-info/` (egg format)
- **New**: `recodex_cleaner-%{version}.dist-info/` (wheel format)

### System Files Installation
- **Old**: Handled automatically by `setup.py` `data_files`
- **New**: Manual installation using `install` commands in `%install` section

## Building RPM Packages

### Prerequisites
```bash
# Install build dependencies
dnf install rpm-build python3-build python3-pip python3-wheel

# For RHEL/CentOS
yum install rpm-build python3-build python3-pip python3-wheel
```

### Build Process
```bash
# Create build directories
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy spec file
cp recodex-cleaner.spec ~/rpmbuild/SPECS/

# Download/prepare source
# (adjust URL and version as needed)
cd ~/rpmbuild/SOURCES
wget https://github.com/ReCodEx/cleaner/archive/SOURCE_COMMIT.tar.gz

# Build RPM
rpmbuild -ba ~/rpmbuild/SPECS/recodex-cleaner.spec
```

### Verification
After building, verify the RPM contains:
- Modern wheel-based Python package installation
- Correct `.dist-info` metadata directory
- System service files in `/lib/systemd/system/`
- Configuration file in `/etc/recodex/cleaner/`
- Executable script in `/usr/bin/recodex-cleaner`

## Benefits of Migration

1. **Standards Compliance**: Uses modern Python packaging standards
2. **Better Isolation**: Build process is more isolated and reproducible
3. **Wheel Format**: More efficient installation and better metadata
4. **Future-Proof**: Compatible with modern Python tooling
5. **Consistent**: Same build system used for pip and RPM packages

## Compatibility Notes

- The RPM package behavior remains the same for end users
- systemd service installation and configuration unchanged
- All file locations and permissions preserved
- No changes required for existing deployments
