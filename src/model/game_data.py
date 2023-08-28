import random

from model.dev_card import DevCard
from model.item import Item
from model.file_handler import FileHandler
from model.tile import Tile


class GameData:
    """
    Game data object that holds all the Tile and Card objects and related methods
    """
    def __init__(self):
        self.map = [[0] * 9 for i in range(9)]
        self.prev_tile = None
        self.indoor_tiles = []
        self.outdoor_tiles = []
        self.dev_cards = []
        self.items = []
        self.file_handler = FileHandler()
        self.setup_game_data()

    def setup_game_data(self):
        self.import_tiles()
        self.import_dev_cards()
        self.import_items()

    def import_tiles(self):
        json_data = self.file_handler.load_data_from_json("tiles")

        for tile in json_data:
            data = dict(tile)
            new_tile = Tile(
                data["name"],
                data["action"],
                data["type"],
                data["src"],
                data["north"],
                data["east"],
                data["south"],
                data["west"],
            )

            if new_tile.room_type == "Indoor":
                self.indoor_tiles.append(new_tile)
            else:
                self.outdoor_tiles.append(new_tile)

    def import_dev_cards(self):
        json_data = self.file_handler.load_data_from_json("devcard")

        for card in json_data:
            data = dict(card)
            item = data["item"]
            nine_effect = data["effect"]["9"]
            ten_effect = data["effect"]["10"]
            eleven_effect = data["effect"]["11"]

            dev_card = DevCard(
                item,
                nine_effect["message"],
                nine_effect["action"],
                ten_effect["message"],
                ten_effect["action"],
                eleven_effect["message"],
                eleven_effect["action"],
                nine_effect["action_amount"],
                ten_effect["action_amount"],
                eleven_effect["action_amount"],
            )

            self.dev_cards.append(dev_card)

    def import_items(self):
        json_data = self.file_handler.load_data_from_json("items")

        for item in json_data:
            data = dict(item)
            new_item = Item(
                data["name"],
                data["action"],
                data["uses"],
                data["combinable"],
                data["combines-with"],
                data["makes"],
                data["action_amount"]
            )

            self.items.append(new_item)

    def get_tile_by_name(self, name):
        for tile in self.indoor_tiles:
            if tile.name == name:
                return tile

        for tile in self.outdoor_tiles:
            if tile.name == name:
                return tile

    def remove_tile_from_deck_by_name(self, name):
        if len(self.indoor_tiles) > 0:
            for index, tile in enumerate(self.indoor_tiles):
                if tile.name == name:
                    self.indoor_tiles.pop(index)

        if len(self.outdoor_tiles) > 0:
            for index, tile in enumerate(self.outdoor_tiles):
                if tile.name == name:
                    self.outdoor_tiles.pop(index)

    # Junho
    def shuffle_devcard_deck(self):
        random.shuffle(self.dev_cards)

    def shuffle_tiles_deck(self):
        random.shuffle(self.indoor_tiles)
        random.shuffle(self.outdoor_tiles)

    def shuffle_tile_cards(self):
        random.shuffle(self.indoor_tiles)
        random.shuffle(self.outdoor_tiles)

    def remove_two_devcards(self):
        self.dev_cards.pop()
        self.dev_cards.pop()
