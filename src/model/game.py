from model.direction import Direction
from model.game_data import GameData
from model.image_handler_strategy import ImageHandler
from model.rotate_image_strategy import RotateImageStrategy
from model.player import Player
from model.state import State
from colorama import Fore, Style
from model.graph import Graph


class Game:
    """
    Main game object that holds everything else
    """
    def __init__(self):
        self.health_turn_graph = Graph()
        self.game_data = GameData()
        self.player = Player(self.game_data, self)
        self.current_direction = None
        rotate_strategy = RotateImageStrategy()
        self.image_handler = ImageHandler(rotate_strategy)
        self.current_zombie_count = 0
        self.state = State.STOPPED
        self.time = 0
        self.devcard_draw_count = 0

    def generate_health_turn_graph(self):
        self.health_turn_graph.generate_health_turn_graph()

    def create_game(self):
        """
        Setup new game and prepare map/items/cards
        :return:
        """
        print(Fore.YELLOW)
        print(
            "The dead walk the earth. You must search the house for the Evil Temple, and find the zombie totem."
        )
        print(
            "Then take the totem outside, and bury it in the Graveyard, all before the clock strikes midnight."
        )
        print(Style.RESET_ALL)
        self.time = 9
        self.game_data.shuffle_devcard_deck()
        self.game_data.shuffle_tiles_deck()
        self.game_data.remove_two_devcards()
        self.game_data.map[self.player.y][
            self.player.x
        ] = self.game_data.get_tile_by_name("Foyer")
        self.game_data.remove_tile_from_deck_by_name("Foyer")
        self.image_handler.create_map_image(self.game_data.map, self.player)
        self.state = State.MOVING

    # Junho
    def get_game_status(self):
        """
        Print out current game statistics
        :return:
        """
        current_tile = self.get_current_tile()
        current_doors = self.get_doors_string(current_tile)

        # Out of time lose condition
        if self.time == 12:
            self.health_turn_graph.increase_turn()
            self.health_turn_graph.add_health(self.player.health)
            print(
                Fore.RED
                + "Sorry time has run out for you! You lose."
                + Style.RESET_ALL
            )
            self.health_turn_graph.generate_health_turn_graph()
            exit()

        if self.state == State.WON:
            self.health_turn_graph.increase_turn()
            self.health_turn_graph.add_health(self.player.health)
            print(
                Fore.GREEN + "Congratulations you have won the game!" + Style.RESET_ALL
            )
            self.health_turn_graph.generate_health_turn_graph()
            exit()

        state = Fore.BLUE + ""
        state_message = Fore.GREEN + ""
        current_tile_name = Fore.BLUE + current_tile.name + Style.RESET_ALL
        doors = Fore.CYAN + current_doors + Style.RESET_ALL

        match self.state:
            case State.MOVING:
                state += "Moving"
                state_message += (
                    "You can move direction by typing move_n, move_e, move_s, move_w or cower"
                )
            case State.ROTATING:
                state += "Rotating"
                state_message += (
                    "Type 'rotate' to rotate the tile until a door matches the current tile. Then type "
                    "'place' to place the tile."
                )
            case State.DRAWING:
                state += "Draw Card"
                state_message += "Type 'draw' to draw a random card."

            case State.COWERING:
                state += "Cowering"
                state_message += (
                    "You are cowering in fear. You will stay in the current tile for this turn."
                )
            case State.BATTLE:
                state += "Battle"
                state_message += "Use 'attack' to fight or 'run' to run away."

        state += Style.RESET_ALL
        state_message += Style.RESET_ALL

        print(
            f"Your current tile is {current_tile_name}, current doors available are: {doors}"
        )
        print(f"Your current state is: {state}")
        print(state_message)

    def move_player(self, direction):
        """
        Move player in direction with logic checking
        :param direction:
        :return:
        """
        current_tile = self.get_current_tile()
        place_patio = False
        next_tile = None
        next_location = None

        if current_tile.room_type == "Indoor":
            if len(self.game_data.indoor_tiles) > 0:
                next_tile = self.game_data.indoor_tiles[0]
            else:
                print(Fore.RED + "There are no more indoor tiles" + Style.RESET_ALL)
                print(
                    Fore.CYAN
                    + "Your next tile placed will move you outside to the Patio"
                    + Style.RESET_ALL
                )
                place_patio = True
        else:
            if len(self.game_data.outdoor_tiles) > 0:
                next_tile = self.game_data.outdoor_tiles[0]
            else:
                print(Fore.RED + "There are no more outdoor tiles" + Style.RESET_ALL)

        self.game_data.prev_tile = current_tile

        match direction:
            case Direction.NORTH:
                if current_tile.door_n:
                    self.current_direction = Direction.NORTH
                    self.player.y -= 1
                    next_location = self.game_data.map[self.player.y][self.player.x]
                else:
                    print(Fore.RED + "There is no path this way" + Style.RESET_ALL)
                    return

            case Direction.SOUTH:
                if current_tile.door_s:
                    self.current_direction = Direction.SOUTH
                    self.player.y += 1
                    next_location = self.game_data.map[self.player.y][self.player.x]
                else:
                    print(Fore.RED + "There is no path this way" + Style.RESET_ALL)
                    return

            case Direction.EAST:
                if current_tile.door_e:
                    self.current_direction = Direction.EAST
                    self.player.x += 1
                    next_location = self.game_data.map[self.player.y][self.player.x]
                else:
                    print(Fore.RED + "There is no path this way" + Style.RESET_ALL)
                    return

            case Direction.WEST:
                if current_tile.door_w:
                    self.current_direction = Direction.WEST
                    self.player.x -= 1
                    next_location = self.game_data.map[self.player.y][self.player.x]
                else:
                    print(Fore.RED + "There is no path this way" + Style.RESET_ALL)
                    return

        if next_location == 0:
            if place_patio:
                patio = [
                    tile
                    for tile in self.game_data.outdoor_tiles
                    if tile.name == "Patio"
                ]
                print(patio[0])
                next_tile = patio[0]

            self.game_data.map[self.player.y][self.player.x] = next_tile
            self.state = State.ROTATING

            if next_tile.action:
                self.check_tile_action(next_tile)

            self.game_data.remove_tile_from_deck_by_name(next_tile.name)
        else:
            self.state = State.MOVING

        self.devcard_draw_count = 0
        self.image_handler.create_map_image(self.game_data.map, self.player)
        self.get_game_status()

    def cower(self):
        """
        Execute cower command with error checking
        :return:
        """
        if self.state == State.MOVING:
            self.state = State.COWERING
            self.player.set_health(3)
            self.discard_devcard()
            print(
                Fore.MAGENTA
                + f"You cower in fear and gain 3 health. You now have {self.player.health} health"
                + Style.RESET_ALL
            )
            print(
                Fore.RED
                + f"You discard 1 dev card and have {len(self.game_data.dev_cards)} left in the pile."
                + Style.RESET_ALL
            )
        else:
            print(Fore.RED + "You can only cower when you are allowed to move." + Style.RESET_ALL)
        self.state = State.MOVING
        self.get_game_status()

    def check_tile_action(self, tile):
        """
        Check if tile has an action and do appropriate action
        :param tile:
        :return:
        """
        if tile.action == "add_health":
            self.player.set_health(3)

        if tile.action == "find_item":
            # TODO
            print(Fore.MAGENTA + "TODO: You have found an item!" + Style.RESET_ALL)

        if tile.action == "find_totem":
            print(
                Fore.MAGENTA
                + "The totem must be around here somewhere, type 'search' to find it!"
                + Style.RESET_ALL
            )

        if tile.action == "bury_item":
            print(
                Fore.MAGENTA
                + "You made it to the graveyard, bury the totem if you have it!"
                + Style.RESET_ALL
            )

    def rotate_tile(self, tile):
        """
        Rotate the tile 90 degrees clockwise and update
        :param tile:
        :return:
        """
        if tile.name == "Patio":
            tile.rotate_factor = (tile.rotate_factor + 2) % 4
            temp = tile.door_n
            tile.door_n = tile.door_s
            tile.door_s = temp
            tile.door_e = False  # Patio tile doesn't have an east-facing door
        else:
            if tile.rotate_factor == 3:
                tile.rotate_factor = 0
            else:
                tile.rotate_factor += 1

            temp = tile.door_w
            tile.door_w = tile.door_s
            tile.door_s = tile.door_e
            tile.door_e = tile.door_n
            tile.door_n = temp

        self.image_handler.create_map_image(self.game_data.map, self.player)

    def place_tile(self):
        """
        Place tile with current rotation if meets requirements, or return error
        :return:
        """
        current_tile = self.get_current_tile()

        match self.current_direction:
            case Direction.NORTH:
                if current_tile.door_s:
                    self.state = State.DRAWING
            case Direction.EAST:
                if current_tile.door_w:
                    self.state = State.DRAWING
            case Direction.SOUTH:
                if current_tile.door_n:
                    self.state = State.DRAWING
            case Direction.WEST:
                if current_tile.door_e:
                    self.state = State.DRAWING

        if self.state == State.DRAWING:
            self.get_game_status()
        else:
            print(
                Fore.RED
                + "Sorry the doors to not match up, try rotating and matching the doors."
                + Style.RESET_ALL
            )
            return

        if current_tile.name == "Dining Room":
            patio_tile = next((tile for tile in self.game_data.outdoor_tiles if tile.name == "Patio"), None)
            if patio_tile:
                self.game_data.map[self.player.y - 1][self.player.x] = patio_tile
                self.rotate_tile(patio_tile)  # Rotate the Patio tile by 180 degrees
                self.game_data.outdoor_tiles.remove(patio_tile)
                self.image_handler.create_map_image(self.game_data.map, self.player)
                self.state = State.MOVING  # Set the state to MOVING
                self.move_player(Direction.NORTH)  # Move player to the newly placed Patio tile
                self.get_game_status()
            else:
                print(Fore.RED + "Patio tile not found in outdoor tiles!" + Style.RESET_ALL)
                return

    def get_current_tile(self):
        """
        Get tile object at x,y co-ordinates
        :return:
        """
        return self.game_data.map[self.player.y][self.player.x]

    def search_tile(self):
        current_tile = self.get_current_tile()
        if current_tile.name == "Evil Temple":
            if self.devcard_draw_count != 2:
                print(Fore.RED + "You must draw at least 2 dev cards to obtain the totem." + Style.RESET_ALL)
            else:
                self.player.hold_totem = True
                print(
                    Fore.MAGENTA
                    + "You have found the totem and quickly grab it, now go and bury it in the graveyard!"
                    + Style.RESET_ALL
                )
        else:
            print(
                Fore.CYAN + "Nope, nothing to be found around here!" + Style.RESET_ALL
            )

    def bury_totem(self):
        """
        Bury totem if requirements are met otherwise return message
        :return:
        """
        current_tile = self.get_current_tile()
        if current_tile.name == "Graveyard" and self.player.hold_totem:
            self.state = State.WON
        elif not self.player.hold_totem:
            print(Fore.RED + "You do not currently hold the totem" + Style.RESET_ALL)
        elif self.devcard_draw_count != 2:
            print(Fore.RED + "You must draw at least 2 dev cards to bury the totem." + Style.RESET_ALL)
        else:
            print(Fore.RED + "You are not currently at the Graveyard" + Style.RESET_ALL)
        self.get_game_status()

    @staticmethod
    def get_doors_string(tile):
        doors = ""
        if tile.door_n:
            doors += "NORTH "
        if tile.door_e:
            doors += "EAST "
        if tile.door_s:
            doors += "SOUTH "
        if tile.door_w:
            doors += "WEST "
        return doors

    def get_player_stats(self):
        """
        Print out current player statistics
        :return:
        """
        print(f"The current time is: {self.time}pm")
        print(f"Your current health is: {self.player.health}")
        print(f"Your current attack is: {self.player.attack}")
        print(f"Currently hold totem: {self.player.hold_totem}")
        print(f"You currently have the following items: {self.player.items}")

    # Junho
    def discard_devcard(self):
        """
        Remove dev card from hand, recreate deck and shuffle if no more left
        :return:
        """
        self.health_turn_graph.increase_turn()
        self.health_turn_graph.add_health(self.player.health)
        if len(self.game_data.dev_cards) <= 1:
            self.time += 1
            self.game_data.dev_cards = []
            self.game_data.import_dev_cards()
            self.game_data.shuffle_devcard_deck()
            self.game_data.remove_two_devcards()
            print(
                Fore.CYAN
                + "You have drawn all the cards available. Resetting deck."
                + Style.RESET_ALL
            )
            print(Fore.GREEN + f"It is now {self.time} pm" + Style.RESET_ALL)
        else:
            self.game_data.dev_cards.pop()

    def draw_devcard(self):
        """
        Draw a new devcard to hand, recreate and shuffle deck if no more left
        :return:
        """
        if len(self.game_data.dev_cards) <= 1:
            # All Dev cards have been drawn, reset the deck and increment time
            self.time += 1
            self.game_data.dev_cards = []
            self.game_data.import_dev_cards()
            self.game_data.shuffle_devcard_deck()
            self.game_data.remove_two_devcards()

            print(
                Fore.CYAN
                + "You have drawn all the cards available. Resetting deck."
                + Style.RESET_ALL
            )
            print(Fore.GREEN + f"It is now {self.time} pm" + Style.RESET_ALL)

        print(
            Fore.YELLOW
            + "Drawing a card from the pile..."
            + Style.RESET_ALL
        )

        self.health_turn_graph.increase_turn()
        self.health_turn_graph.add_health(self.player.health)

        drawn_card = self.game_data.dev_cards.pop(0)
        self.do_devcard_effect(drawn_card)
        self.devcard_draw_count += 1
        if self.state != State.BATTLE:
            self.state = State.MOVING
        self.get_game_status()

    def do_devcard_effect(self, devcard):
        """
        Take a devcard and perform action or display message
        :param devcard:
        :return:
        """
        match self.time:
            case 9:
                if devcard.nine_message:
                    print(
                        Fore.YELLOW
                        + f"{devcard.nine_message}"
                        + Style.RESET_ALL
                    )
                if devcard.nine_action:
                    if devcard.nine_action == "set_health":
                        self.player.set_health(devcard.nine_action_amount)
                    if devcard.nine_action == "add_zombies":
                        self.add_zombies(devcard.nine_action_amount)
                    if devcard.nine_action == "add_item":
                        confirm = input(
                            Fore.MAGENTA
                            + "Item! Do you wish to draw another card to find out what it is? (y/n): "
                            + Style.RESET_ALL
                        )
                        if confirm.strip() == "y":
                            next_card = self.game_data.dev_cards.pop(0)
                            self.player.add_item(next_card.item)

            case 10:
                if devcard.ten_message:
                    print(
                        Fore.YELLOW
                        + f"{devcard.ten_message}"
                        + Style.RESET_ALL
                    )
                if devcard.ten_action:
                    if devcard.ten_action == "set_health":
                        self.player.set_health(devcard.ten_action_amount)
                    if devcard.ten_action == "add_zombies":
                        self.add_zombies(devcard.ten_action_amount)
                    if devcard.ten_action == "add_item":
                        confirm = input(
                            Fore.MAGENTA
                            + "Item! Do you wish to draw another card to find out what it is? (y/n): "
                            + Style.RESET_ALL
                        )
                        if confirm.strip() == "y":
                            next_card = self.game_data.dev_cards.pop(0)
                            self.player.add_item(next_card.item)

            case 11:
                if devcard.eleven_message:
                    print(
                        Fore.YELLOW
                        + f"{devcard.eleven_message}"
                        + Style.RESET_ALL
                    )
                if devcard.eleven_action:
                    if devcard.eleven_action == "set_health":
                        self.player.set_health(devcard.eleven_action_amount)
                    if devcard.eleven_action == "add_zombies":
                        self.add_zombies(devcard.eleven_action_amount)
                    if devcard.eleven_action == "add_item":
                        confirm = input(
                            Fore.MAGENTA
                            + "Item! Do you wish to draw another card to find out what it is? (y/n): "
                            + Style.RESET_ALL
                        )
                        if confirm.strip() == "y":
                            next_card = self.game_data.dev_cards.pop(0)
                            self.player.add_item(next_card.item)

    def add_zombies(self, amount):
        """
        Add zombies to the current count
        :param amount:
        :return:
        """
        self.current_zombie_count += amount
        self.state = State.BATTLE
        print(
            Fore.RED
            + f"{amount} Zombies have appeared."
            + Style.RESET_ALL
        )
