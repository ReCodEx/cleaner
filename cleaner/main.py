#!/usr/bin/env python3
"""
"""

from .config_manager import ConfigManager
import argparse
import sys
import os


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help="Path to configuration file", default=None)


class Cleaner:

    def __init__(self, config):
        self._cache_dir = config.get_cache_dir()
        self._file_age = config.get_file_age()

        self.check_cache_dir()
        self.check_file_age()

    def check_cache_dir(self):
        if self._cache_dir is None:
            raise Exception("Cache directory not specified!")

        if not os.path.isdir(self._cache_dir):
            raise Exception("Cache directory is not a directory")

    def check_file_age(self):
        if self._file_age is None:
            raise Exception("File age not specified!")

        if not self._file_age.isdigit():
            raise Exception("File age is not a number!")

    def clean(self):
        print("Cleaning directory: " + self._cache_dir)
        print("Maximum file age: " + self._file_age)


def main():
    """
    :return: Nothing
    """
    args = parser.parse_args()

    try:
        # get configuration
        config = ConfigManager(args.config)
        cleaner = Cleaner(config)
        cleaner.clean()
    except Exception as ex:
        print("Exception occured: " + str(ex), file=sys.stderr)

if __name__ == "__main__":
    main()
