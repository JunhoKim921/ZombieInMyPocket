"""
Module providing Pickle file handling functionality.

IFileHandler interface for handling files using pickle serialization.
"""

from model.ifile_handler import IFileHandler
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


class PickleFileHandler(IFileHandler):
    """
    Handler for Pickle file operations.

    Provides methods to save and load game states using pickle serialization.
    """

    def __init__(self):
        """Initialize the PickleFileHandler with the root directory path."""
        self.root_dir = Path(__file__).parent.parent

    def save_game(self, game, filename):
        """
        Save a game state to a Pickle file.

        Opens a file dialog to select a file path and saves the game.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=".pkl",
            filetypes=[("Pickle Files", "*.pkl")]
        )

        root.destroy()

        if file_path:
            with open(file_path, "wb") as file:
                pickle.dump(game, file)

    def load_game(self, filename=None):
        """
        Load a game state from a Pickle file.

        Opens a file dialog to select a file path and loads the game.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            initialdir=filename,
            filetypes=[("Pickle Files", "*.pkl")]
        )

        root.destroy()

        if file_path:
            with open(file_path, "rb") as file:
                game = pickle.load(file)
                return game
