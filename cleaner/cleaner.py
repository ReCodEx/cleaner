#!/usr/bin/env python3

from .config_manager import ConfigManager
import os
import time


class Cleaner:
    """
    Cleaner class handles cleaning of given cache folder.
    Files are cleaned based on last access time, which have to be in interval given in configuration.
    """

    def __init__(self, config):
        """
        Constructor which takes configuration of cleaner.

        :param config: have to be instance of ConfigManager class
        :raises Exception: if values from configuration are not valid
        """
        self._cache_dir = config.get_cache_dir()
        self._file_age = config.get_file_age()

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

        if not self._file_age.isdigit():
            raise Exception("File age is not a number!")

        self._file_age = int(self._file_age)

    def clean(self):
        """
        Cleaning itself. Cleans cache folder from files or folders which are older than interval given in configuration.

        :return: Nothing
        """

        # some general debug information about this time execution
        now = round(time.time())
        print("****************************************")
        print("Cleaning files from \"" + self._cache_dir + "\"")
        print("With maximum file age: " + str(self._file_age) + " seconds")
        print("Timestamp now: " + str(now) + " seconds")
        print("****************************************")

        def process_path(root, file, action):
            """
            Process given path, path can be file or directory.
            Given action is executed on constructed full path

            :param root: path to root directory, used as base
            :param file: name of file itself, root is used as base and joined with this
            :param action: action which will be performed if access timestamp is older than given interval
            :return: Nothing
            """
            full_path = os.path.join(root, file)
            last_access = round(os.stat(full_path).st_atime)
            difference = now - last_access

            print(full_path)
            print("    last access: " + str(last_access))
            print("    difference: " + str(difference))

            if difference > self._file_age:
                try:
                    action(full_path)
                    print("    >>> REMOVED <<<")
                except Exception as ex:
                    print("    >>> Exception occured: " + str(ex))

        # iterate recursively through given directory
        for root, dirs, files in os.walk(self._cache_dir):
            for file in files:
                process_path(root, file, os.remove)
            for dir in dirs:
                process_path(root, dir, os.rmdir)
