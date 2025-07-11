#!/usr/bin/env python3
"""
Test script to validate the pyproject.toml migration.
"""

import sys
import tomllib
from pathlib import Path


def test_pyproject_toml():
    """Test that pyproject.toml is valid and contains expected configuration."""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return False

    try:
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        print("✅ pyproject.toml syntax is valid")
    except Exception as e:
        print(f"❌ pyproject.toml syntax error: {e}")
        return False

    # Check required sections
    required_sections = ["build-system", "project"]
    for section in required_sections:
        if section not in config:
            print(f"❌ Missing required section: {section}")
            return False
        print(f"✅ Found section: {section}")

    # Check project metadata
    project = config["project"]
    required_fields = ["name", "description", "authors"]
    for field in required_fields:
        if field not in project:
            print(f"❌ Missing required field: project.{field}")
            return False
        print(f"✅ Found field: project.{field}")

    # Check build system
    build_system = config["build-system"]
    setuptools_found = any("setuptools" in req for req in build_system.get("requires", []))
    if not setuptools_found:
        print("❌ setuptools not in build requirements")
        return False
    print("✅ setuptools in build requirements")

    return True


def test_version_import():
    """Test that version can be imported from package."""
    try:
        from cleaner import __version__
        print(f"✅ Version imported successfully: {__version__}")
        return True
    except ImportError as e:
        print(f"❌ Cannot import version: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing pyproject.toml migration...")
    print("=" * 40)

    tests = [
        test_pyproject_toml,
        test_version_import,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 Migration successful!")
        print("\nNext steps:")
        print("1. Test installation: pip install .")
        print("2. Run system file installer: python install_system_files.py")
        print("3. Test building: python -m build")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        sys.exit(1)


if __name__ == "__main__":
    main()
