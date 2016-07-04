#!/usr/bin/env python3

from .config_manager import ConfigManager
from .cleaner import Cleaner
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help="Path to configuration file", default=None)


def main():
    """
    Main function which have to be called in order to execute cleaner properly.

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
