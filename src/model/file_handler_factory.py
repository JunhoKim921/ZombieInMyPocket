# file_handler_factory.py
from model.json_file_handler import JSONFileHandler
from model.pickle_file_handler import PickleFileHandler
from model.shelve_file_handler import ShelveFileHandler


class FileHandlerFactory:
    @staticmethod
    def get_file_handler(handler_type):
        if handler_type == 'json':
            return JSONFileHandler()
        elif handler_type == 'pickle':
            return PickleFileHandler()
        elif handler_type == 'shelve':
            return ShelveFileHandler()
        else:
            raise ValueError("Unknown file handler type")
