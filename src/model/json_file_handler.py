from model.ifile_handler import IFileHandler
import json
from pathlib import Path


class JSONFileHandler(IFileHandler):
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent

    def save_game(self, game, filename):
        pass

    def load_game(self, filename):
        full_path = self.root_dir / "data" / f"{filename}.json"
        with open(full_path, 'r') as file:
            game_data = json.load(file)
        return game_data
