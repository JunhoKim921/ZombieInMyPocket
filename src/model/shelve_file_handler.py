from model.ifile_handler import IFileHandler
import shelve
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


class ShelveFileHandler(IFileHandler):

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent

    def save_game(self, game, filename=None):
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
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            initialdir=filename,  # Use filename as initial directory if provided
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
