"""
Module providing JSON file handling functionality.

Implements the IFileHandler interface for handling files in JSON format.
"""

from model.ifile_handler import IFileHandler
import json
from pathlib import Path


class JSONFileHandler(IFileHandler):
    """
    Handler for JSON file operations.

    Provides methods to load game states from JSON files.
    """

    def __init__(self):
        """Initialize the JSONFileHandler with the root directory path."""
        self.root_dir = Path(__file__).parent.parent

    def save_game(self, game, filename):
        """
        Save a game state to a JSON file.

        Currently not implemented for JSON.
        """
        pass

    def load_game(self, filename):
        """
        Load a game state from a JSON file.

        :param filename: The name of the file to load the game from.
        :return: The loaded game object.
        """
        full_path = self.root_dir / "data" / f"{filename}.json"
        with open(full_path, 'r') as file:
            game_data = json.load(file)
        return game_data
