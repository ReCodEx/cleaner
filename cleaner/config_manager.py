#!/usr/bin/env python3

import yaml


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

        :return: Single textual value
        """
        return self._config.get('file-age')

