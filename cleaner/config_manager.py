#!/usr/bin/env python3

import yaml
import logging
import logging.handlers


class ConfigManager:
    """
    Class to handle all configuration items.
    """
    def __init__(self, config_file=None):
        """
        Init with default values.

        :param config_file: Path to YAML configuration file. If not given, default values are used.
        """

        self._config = dict()
        if config_file:
            try:
                with open(config_file, 'r') as f:
                    self._config = yaml.safe_load(f)
            except FileNotFoundError:
                # using defaults
                pass

    def get_cache_dir(self):
        """
        Get directory in which cache of worker is placed.

        :return: Single string value
        """
        return self._config.get('cache-dir')

    def get_file_age(self):
        """
        Get maximum file age in seconds.

        :return: Single integer value
        """
        return int(self._config['file-age']) if 'file-age' in self._config else 604800

    def get_logger_settings(self):
        """
        Get path to system log file.

        :return: List with 4 items - string path, logging level, integer maximum size
            of logfile and integer number of rotations kept.
        """
        result = ["/tmp/recodex-cleaner.log", logging.INFO, 1024*1024, 3]
        if 'logger' in self._config:
            sect = self._config['logger']
            if 'file' in sect:
                result[0] = sect['file']
            if 'level' in sect:
                result[1] = self._get_loglevel_from_string(sect['level'])
            if 'max-size' in sect:
                try:
                    result[2] = int(sect['max-size'])
                except:
                    pass
            if 'rotations' in sect:
                try:
                    result[3] = int(sect['rotations'])
                except:
                    pass
        return result

    def _get_loglevel_from_string(self, str_level):
        """
        Convert logging level from string to logging module type.

        :param str_level: string representation of logging level
        :return: logging level (defaults to logging.INFO)
        """
        level_mapping = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        if str_level in level_mapping:
            return level_mapping[str_level]
        else:
            return logging.INFO


def init_logger(logfile, level, max_size, rotations):
    """
    Initialize new system logger for cleaner. If arguments are invalid,
    empty logger will be created.

    :param logfile: Path to file with log.
    :param level: Log level as logging.<LEVEL>
    :param max_size: Maximum size of log file.
    :param rotations: Number of log files kept.
    :return: Initialized logger.
    """
    try:
        # create logger
        logger = logging.getLogger('recodex-cleaner')
        logger.setLevel(level)

        # create rotating file handler
        ch = logging.handlers.RotatingFileHandler(logfile, maxBytes=max_size, backupCount=rotations)
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
    except Exception as e:
        # create empty logger
        print("Invalid logger configuration. Creating null logger. Error: {}".format(e))
        logger = logging.getLogger('recodex-cleaner-dummy')
        logging.disable(logging.CRITICAL)

    # print welcome message to log file
    logger.critical("-------------------------")
    logger.critical(" ReCodEx Cleaner started")
    logger.critical("-------------------------")

    # return created logger
    return logger

