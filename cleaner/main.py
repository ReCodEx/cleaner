#!/usr/bin/env python3

from .config_manager import ConfigManager, init_logger
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
        logger = init_logger(*config.get_logger_settings())
        cleaner = Cleaner(config, logger)
        cleaner.clean()
        logger.info("Cleaning finished, quiting")
    except Exception as ex:
        error_text = "Exception occured: {}".format(str(ex))
        logger.warning(error_text)
        print(error_text, file=sys.stderr)

if __name__ == "__main__":
    main()
