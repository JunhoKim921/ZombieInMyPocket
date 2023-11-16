from model.ifile_handler import IFileHandler
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

class PickleFileHandler(IFileHandler):

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent

    def save_game(self, game, filename):
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
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            initialdir=filename,  # Use filename as initial directory if provided
            filetypes=[("Pickle Files", "*.pkl")]
        )

        root.destroy()

        if file_path:
            with open(file_path, "rb") as file:
                game = pickle.load(file)
                return game
