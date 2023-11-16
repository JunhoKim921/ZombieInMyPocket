"""
Module providing the FileHandlerFactory class.

This module defines a factory class for creating file handler objects.
based on a specified type, including JSON, Pickle, and Shelve file handlers.
"""

from model.json_file_handler import JSONFileHandler
from model.pickle_file_handler import PickleFileHandler
from model.shelve_file_handler import ShelveFileHandler


class FileHandlerFactory:
    """
    Factory for creating file handler objects based on a specified type.

    Factory creates instances of JSON, Pickle, and Shelve file handlers.
    """

    @staticmethod
    def get_file_handler(handler_type):
        """
        Get a file handler instance based on the specified handler type.

        :param handler_type: Type handler.
        :return: An instance of a file handler.
        :raises ValueError: If an unknown handler type is specified.
        """
        if handler_type == 'json':
            return JSONFileHandler()
        elif handler_type == 'pickle':
            return PickleFileHandler()
        elif handler_type == 'shelve':
            return ShelveFileHandler()
        else:
            raise ValueError("Unknown file handler type")
