"""
Module providing Shelve file handling functionality.

Interface for handling files using shelve serialization.
"""

from model.ifile_handler import IFileHandler
import shelve
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


class ShelveFileHandler(IFileHandler):
    """
    Handler for Shelve file operations.

    Provides methods to save and load game states using shelve serialization.
    """

    def __init__(self):
        """Initialize the ShelveFileHandler with the root directory path."""
        self.root_dir = Path(__file__).parent.parent

    def save_game(self, game, filename=None):
        """
        Save a game state to a Shelve file.

        Opens a file dialog to select a file path and saves the game.
        If no filename is provided, prompts the user to choose a file path.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=".shelf",
            filetypes=[("Shelve Files", "*.shelf"), ("All Files", "*.*")]
        )

        root.destroy()

        if file_path:
            with shelve.open(file_path, "c") as file:
                file["game"] = game

    def load_game(self, filename=None):
        """
        Load a game state from a Shelve file.

        Opens a file dialog to select a file path and loads the game.
        If no filename is provided, prompts the user to choose a file path.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            initialdir=filename,
            filetypes=[("Shelve Files", "*.bak"), ("All Files", "*.*")]
        )

        root.destroy()

        if file_path:
            # Remove extension from filepath if needed
            if file_path.endswith('.bak'):
                file_path = file_path[:-4]

            with shelve.open(file_path) as file:
                game = file["game"]
                return game
