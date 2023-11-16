import json
from pathlib import Path
import pickle
import shelve
from model.image_handler import ImageHandler
import tkinter as tk
from tkinter import filedialog


class FileHandler:
    """
    Object to hold file related methods e.g. saving/loading game state test
    """
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent

    # William
    def load_data_from_json(self, filename):
        """
        Load json file from specified filename and return it
        :param filename:
        :return:
        """
        file = open(str(self.root_dir / "data") + "\\" + filename + ".json")
        data = json.load(file)
        file.close()
        return data

    # Junho
    def save_game_with_pickle(self, game, filename):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes("-topmost", True)  # Make the file dialog appear on top

        file_path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=".pkl",
            filetypes=[("Pickle Files", "*.pkl")]
        )

        if file_path:
            with open(file_path, "wb") as file:
                pickle.dump(game, file)

    # William
    def save_game_with_shelve(self, game, filename=""):
        """
        Save game state into a .shelf file
        :param game:
        :param filename:
        :return:
        """
        if filename != "":
            with shelve.open(str(self.root_dir / "saves") + "\\" + filename + ".db", flag='c', protocol=4) as file:
                file["game"] = game
        else:
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)

            file_path = filedialog.asksaveasfilename(
                initialfile=filename,
                defaultextension=".shelf",
                filetypes=[("Shelve Files", "*.shelf"), ("All Files", "*.*")]
            )

            if file_path:
                with shelve.open(file_path, "c") as file:
                    file["game"] = game

    # William
    def load_game_with_shelve(self, filename=""):
        """
        Load game state from a .shelf file
        :param filename:
        :return:
        """
        if filename != "":
            with shelve.open(str(self.root_dir / "saves") + "\\" + filename + ".db") as file:
                game = file["game"]
            return game
        else:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                filetypes=[("Shelve Files", "*.bak"), ("All Files", "*.*")]
            )

            if file_path:
                # Remove extension from filepath
                file_path = file_path[:-4]
                print(file_path)
                with shelve.open(file_path) as file:
                    game = file["game"]
                return game

    # Junho
    def load_game_with_pickle(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        root.attributes("-topmost", True)  # Make the file dialog appear on top

        file_path = filedialog.askopenfilename(
            filetypes=[("Pickle Files", "*.pkl")]
        )

        root.attributes("-topmost", False)

        if file_path:
            with open(file_path, "rb") as file:
                game = pickle.load(file)

            # Restore the image_handler attribute
            game.image_handler = ImageHandler()

            return game


