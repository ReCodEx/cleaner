#!/usr/bin/env python3

from .config_manager import ConfigManager
import os
import time


class Cleaner:
    """
    Cleaner class handles cleaning of given cache folder.
    Files are cleaned based on last modification time, which have to be in interval given in configuration.
    """

    def __init__(self, config, logger):
        """
        Constructor which takes configuration of cleaner.

        :param config: have to be instance of ConfigManager class
        :param logger: System logger instance
        :raises Exception: if values from configuration are not valid
        """
        self._cache_dir = config.get_cache_dir()
        self._file_age = config.get_file_age()
        self._logger = logger

        self.check_cache_dir()
        self.check_file_age()

    def check_cache_dir(self):
        """
        Check if cache directory is valid.

        :return: Nothing
        :raises Exception: if cache directory is not valid
        """
        if self._cache_dir is None:
            raise Exception("Cache directory not specified!")

        if not os.path.isdir(self._cache_dir):
            raise Exception("Cache directory is not a directory")

    def check_file_age(self):
        """
        Check if file age value is valid.

        :return: Nothing
        :raises Exception: if file age is not valid
        """
        if self._file_age is None:
            raise Exception("File age not specified!")

        if self._file_age <= 0:
            raise Exception("File age is not positive number!")

    def clean(self):
        """
        Cleaning itself. Cleans cache folder from files or folders which are older than interval given in configuration.

        :return: Nothing
        """

        # some general debug information about this time execution
        now = round(time.time())
        self._logger.info("Cleaning files from \"{}\"".format(self._cache_dir))
        self._logger.info("Maximum file age: {} seconds".format(self._file_age))

        def process_file(root, file):
            """
            Process given file. If modification timestamp is too old, the file will be removed.

            :param root: path to root directory, used as base
            :param file: name of file itself, root is used as base and joined with this
            :return: Nothing
            """

            full_path = os.path.join(root, file)
            last_modification = round(os.stat(full_path).st_mtime)
            difference = now - last_modification

            self._logger.debug("last modification: {}".format(last_modification))
            self._logger.debug("age from now: {} seconds".format(difference))

            if difference > self._file_age:
                self._logger.debug("file \"{}\" marked for deletion".format(full_path))
                try:
                    os.remove(full_path)
                    self._logger.info("file \"{}\" removed".format(full_path))
                except Exception as ex:
                    self._logger.warning("removing file \"{}\" failed: {}".format(full_path, ex))
            else:
                self._logger.debug("file \"{}\" will be kept".format(full_path))

        def process_directory(root, dir):
            """
            Process given directory. If it is empty, the directory will be removed.

            :param root: path to root directory, used as base
            :param file: name of directory itself, root is used as base and joined with this
            :return: Nothing
            """

            full_path = os.path.join(root, dir)
            if not os.listdir(full_path):
                self._logger.debug("directory \"{}\" is empty".format(full_path))
                try:
                    os.rmdir(full_path)
                    self._logger.info("directory \"{}\" removed".format(full_path))
                except Exception as ex:
                    self._logger.warning("removing directory \"{}\" failed: {}".format(full_path, ex))
           else:
               self._logger.debug("directory \"{}\" is not empty and will be kept".format(full_path))

        # iterate recursively through given directory (in DFS order)
        for root, dirs, files in os.walk(self._cache_dir, topdown=False):
            for file in files:
                self._logger.info("Processing file: {}".format(file))
                process_file(root, file)
            for dir in dirs:
                self._logger.info("Processing directory: {}".format(dir))
                process_directory(root, dir)

