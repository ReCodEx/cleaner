#!/usr/bin/env python3
"""
Test script to validate RPM spec file changes for pyproject.toml migration.
"""

import re
from pathlib import Path


def test_spec_file():
    """Test that the spec file has been updated for modern Python packaging."""
    spec_path = Path("recodex-cleaner.spec")

    if not spec_path.exists():
        print("❌ recodex-cleaner.spec not found")
        return False

    with open(spec_path, 'r') as f:
        content = f.read()

    # Check for modern build requirements
    if "python3dist(build)" not in content:
        print("❌ Missing python3dist(build) build requirement")
        return False
    print("✅ Found python3dist(build) build requirement")

    if "python3dist(setuptools) >= 61.0" not in content:
        print("❌ Missing modern setuptools requirement")
        return False
    print("✅ Found modern setuptools requirement")

    # Check for modern build command
    if "%{python3} -m build --wheel" not in content:
        print("❌ Missing modern build command")
        return False
    print("✅ Found modern build command")

    # Check for wheel installation
    if "%{python3} -m pip install" not in content:
        print("❌ Missing pip install command")
        return False
    print("✅ Found pip install command")

    # Check for manual system file installation
    if "install -m 644 cleaner/install/" not in content:
        print("❌ Missing manual system file installation")
        return False
    print("✅ Found manual system file installation")

    # Check for .dist-info instead of .egg-info
    if ".dist-info/" not in content:
        print("❌ Missing .dist-info pattern (still using .egg-info?)")
        return False
    print("✅ Found .dist-info pattern")

    if ".egg-info/" in content:
        print("❌ Still contains .egg-info pattern (should be .dist-info)")
        return False
    print("✅ No legacy .egg-info pattern found")

    # Check that %py3_build and %py3_install are not used
    if "%py3_build" in content:
        print("❌ Still using legacy %py3_build macro")
        return False
    print("✅ Not using legacy %py3_build macro")

    if "%py3_install" in content:
        print("❌ Still using legacy %py3_install macro")
        return False
    print("✅ Not using legacy %py3_install macro")

    print("✅ All spec file checks passed!")
    return True


def test_spec_syntax():
    """Basic syntax validation for RPM spec file."""
    spec_path = Path("recodex-cleaner.spec")

    with open(spec_path, 'r') as f:
        content = f.read()

    # Check for required sections
    required_sections = ["%prep", "%build", "%install", "%files"]
    for section in required_sections:
        if section not in content:
            print(f"❌ Missing required section: {section}")
            return False
        print(f"✅ Found section: {section}")

    # Check for proper macro usage
    if content.count("%{") != content.count("}"):
        print("❌ Unmatched macro braces")
        return False
    print("✅ Macro syntax looks good")

    return True


def main():
    """Run all tests."""
    print("Testing RPM spec file migration...")
    print("=" * 40)

    tests = [
        test_spec_syntax,
        test_spec_file,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 RPM spec file migration successful!")
        print("\nNext steps:")
        print("1. Test RPM build: rpmbuild -ba recodex-cleaner.spec")
        print("2. Verify system file installation in the built RPM")
        print("3. Test package installation and service setup")
    else:
        print("❌ Some tests failed. Please check the spec file.")


if __name__ == "__main__":
    main()
