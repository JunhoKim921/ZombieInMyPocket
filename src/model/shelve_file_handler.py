from model.ifile_handler import IFileHandler
import shelve


class ShelveFileHandler(IFileHandler):
    def save_game(self, game, filename):
        with shelve.open(filename, flag='c', protocol=4) as file:
            file["game"] = game

    def load_game(self, filename):
        with shelve.open(filename) as file:
            game_data = file["game"]
        return game_data
