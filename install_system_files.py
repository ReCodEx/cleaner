#!/usr/bin/env python3
"""
Post-installation script for recodex-cleaner.
This handles platform-specific file installation that was previously in
setup.py.
"""

import sys
import os
import shutil
from pathlib import Path


def install_system_files():
    """Install systemd service files and config on non-Windows systems."""
    if sys.platform == "win32":
        print("Windows detected - skipping systemd file installation")
        return

    # Define installation paths
    systemd_dir = Path("/lib/systemd/system")
    config_dir = Path("/etc/recodex/cleaner")

    # Source files
    package_dir = Path(__file__).parent / "cleaner" / "install"
    service_files = [
        package_dir / "recodex-cleaner.service",
        package_dir / "recodex-cleaner.timer"
    ]
    config_file = package_dir / "config.yml"

    try:
        # Install systemd files
        if systemd_dir.exists() or os.access("/lib/systemd", os.W_OK):
            systemd_dir.mkdir(parents=True, exist_ok=True)
            for service_file in service_files:
                if service_file.exists():
                    shutil.copy2(service_file, systemd_dir)
                    print(f"Installed {service_file.name} to {systemd_dir}")

        # Install config file
        if config_file.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(config_file, config_dir)
            print(f"Installed {config_file.name} to {config_dir}")

    except PermissionError:
        print("Warning: Insufficient permissions to install system files.")
        print("You may need to run with elevated privileges or install "
              "files manually:")
        print(f"  - Copy {package_dir}/recodex-cleaner.service to "
              f"/lib/systemd/system/")
        print(f"  - Copy {package_dir}/recodex-cleaner.timer to "
              f"/lib/systemd/system/")
        print(f"  - Copy {package_dir}/config.yml to /etc/recodex/cleaner/")


if __name__ == "__main__":
    install_system_files()
