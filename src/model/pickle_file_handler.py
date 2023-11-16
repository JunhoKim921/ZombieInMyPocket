from model.ifile_handler import IFileHandler
import pickle
from pathlib import Path


class PickleFileHandler(IFileHandler):
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
    def save_game(self, game, filename):
        with open(filename, 'wb') as file:
            pickle.dump(game, file)

    def load_game(self, filename):
        with open(filename, 'rb') as file:
            game_data = pickle.load(file)
        return game_data
