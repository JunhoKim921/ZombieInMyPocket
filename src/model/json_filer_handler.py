from model.ifile_handler import IFileHandler
import json


class JSONFileHandler(IFileHandler):
    def save_game(self, game, filename):
        # As specified, no implementation needed for saving in JSON format
        pass

    def load_game(self, filename):
        with open(filename, 'r') as file:
            game_data = json.load(file)
        return game_data
