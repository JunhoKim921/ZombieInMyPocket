import cmd
from colorama import Fore, Style

from model.database_handler import DatabaseHandler
from model.direction import Direction
from model.game import Game
from model.state import State
from model.file_handler_factory import FileHandlerFactory


class Commands(cmd.Cmd):
    intro = "Welcome to Zombies in my Pocket!"

    # Junho & William
    def __init__(self, args=""):
        cmd.Cmd.__init__(self)
        self.prompt = ">> "
        self.game = Game()
        self.database_handler = DatabaseHandler()
        self.args = args
        self.command_methods = {
            "start": self.do_start,
            "help": self.do_help,
            "exit": self.do_exit,
            "save": self.do_save_help,
            "help_all": self.do_help_all
        }

        if len(args) > 1:
            self.check_args(args)

    # Junho & William
    def check_args(self, args):
        for command in args:
            if command in self.command_methods:
                self.command_methods[command](command)
            else:
                print(f"Unknown command: {command}")

    # William
    def do_start(self, line):
        """
        Starts a new game of Zombies in my Pocket
        """
        if self.game.state == State.STOPPED:
            self.game.create_game()
            self.game.get_game_status()
        else:
            print(
                Fore.RED
                + "You are already currently playing the game."
                + Style.RESET_ALL
            )

    # William
    def do_move_n(self, line):
        """
        Moves player to a NORTH tile
        :return:
        """
        if self.game.state == State.MOVING:
            self.game.move_player(Direction.NORTH)
        else:
            print(
                Fore.RED
                + "You are currently not in the moving state."
                + Style.RESET_ALL
            )

    # William
    def do_move_e(self, line):
        """
        Moves player to a EAST tile
        :return:
        """
        if self.game.state == State.MOVING:
            self.game.move_player(Direction.EAST)
        else:
            print(
                Fore.RED
                + "You are currently not in the moving state."
                + Style.RESET_ALL
            )

    # William
    def do_move_s(self, line):
        """
        Moves player to a SOUTH tile
        :return:
        """
        if self.game.state == State.MOVING:
            self.game.move_player(Direction.SOUTH)
        else:
            print(
                Fore.RED
                + "You are currently not in the moving state."
                + Style.RESET_ALL
            )

    # William
    def do_move_w(self, line):
        """
        Moves player to a WEST tile
        :return:
        """
        if self.game.state == State.MOVING:
            self.game.move_player(Direction.WEST)
        else:
            print(
                Fore.RED
                + "You are currently not in the moving state."
                + Style.RESET_ALL
            )

    # Junho
    def do_cower(self, line):
        """
        Player cowers in their current tile
        Gains 3 Health
        """
        if self.game.state == State.MOVING:
            self.game.cower()
        else:
            print(
                Fore.RED
                + "You can not cower right now"
                + Style.RESET_ALL
            )

    # Junho
    def do_rotate(self, line):
        """
        Rotates the current tile 90 degrees clockwise
        """
        if self.game.state == State.ROTATING:
            current_tile = self.game.get_current_tile()
            self.game.rotate_tile(current_tile)
            self.game.get_game_status()
        else:
            print(Fore.RED + "You are currently not in the rotating state" + Style.RESET_ALL)

    # William
    def do_place(self, line):
        """
        Places tile at current location and rotation
        """
        if self.game.state == State.ROTATING:
            self.game.place_tile()
        else:
            print(Fore.RED + "You are currently not in the rotating state" + Style.RESET_ALL)

    # William
    def do_draw(self, line):
        """
        Draws a new dev card from the pile
        """
        if self.game.state != State.STOPPED and self.game.state != State.BATTLE:
            self.game.draw_devcard()
        else:
            print(Fore.RED + "You cannot currently draw a card." + Style.RESET_ALL)

    # Junho
    def do_use_item(self, index):
        """
        Use an item from the players inventory based on the index e.g. use_item 1
        :param index:
        :return:
        """
        try:
            if self.game.state != State.STOPPED:
                self.game.player.use_item(index)
            else:
                print(
                    Fore.RED + "You can't currently use an item at the moment" + Style.RESET_ALL
                )
        except Exception as e:
            print(Fore.RED + f"An error occurred while using the item, make sure you're entering a number: {e}" +
                  Style.RESET_ALL)

    # William
    def do_search(self, line):
        """
        Searches the current tile to see if the Totem is around
        """
        if self.game.state != State.STOPPED and self.game.state != State.BATTLE:
            self.game.search_tile()
        else:
            print(
                Fore.RED + "You can't currently search at the moment" + Style.RESET_ALL
            )

    # William
    def do_bury(self, line):
        """
        Bury the totem at the Graveyard
        """
        if self.game.state != State.STOPPED and self.game.state != State.BATTLE:
            self.game.bury_totem()
        else:
            print(
                Fore.RED
                + "You can't currently use this command at the moment"
                + Style.RESET_ALL
            )

    # Junho
    def do_attack(self, line):
        """
        Attacks zombies when they appear
        """
        if self.game.state == State.BATTLE:
            self.game.player.do_attack()
        else:
            print(
                Fore.RED
                + "You can't attack when there are no zombies around."
                + Style.RESET_ALL
            )

    # Junho
    def do_run(self, line):
        """
        Run away from a zombie attack
        You lose 1 health.
        """
        if self.game.state == State.BATTLE:
            self.game.player.do_run()
        else:
            print(
                Fore.RED
                + "You can't run when there are no zombies around."
                + Style.RESET_ALL
            )

    # William
    def do_get_inventory(self, line):
        """
        Displays items that you currently hold in inventory and charges left.
        """
        if self.game.state != State.STOPPED:
            self.game.player.get_items()
        else:
            print(
                Fore.RED
                + "You can't currently use this command at the moment"
                + Style.RESET_ALL
            )

    # William

    def do_exit(self, line):
        """
        Quit Zombies in my Pocket
        """
        print(
            Fore.GREEN + "Thank you for playing Zombies in my Pocket!" + Style.RESET_ALL
        )
        self.game.generate_health_turn_graph()

        return True

    # William
    def do_restart(self, line):
        """
        Restarts the current game. Does not save any progress.
        """
        print(Fore.RED + "Restarting game..." + Style.RESET_ALL)
        del self.game
        self.game = Game()
        self.game.create_game()
        self.game.get_game_status()

    # William
    def do_get_status(self, line):
        """
        Returns players status of current player
        """
        if self.game.state != State.STOPPED:
            self.game.get_player_stats()
        else:
            print(
                Fore.RED
                + "You are currently not playing a game, use 'start' to start a new game."
                + Style.RESET_ALL
            )

    # Junho
    def do_save(self, line):
        """
        Save the current game to a file
        """
        params = line.split()

        if len(params) < 1:
            print(Fore.RED + "Usage: save <method> <filename = optional> " + Style.RESET_ALL)
            return

        method = params[0]
        filename = None

        if len(params) > 1:
            filename = params[1]

        if self.game.state != State.STOPPED:
            try:
                if method == "pickle":
                    pickle_handler = FileHandlerFactory.get_file_handler('pickle')
                    pickle_handler.save_game(self.game, filename)
                    print(Fore.GREEN + f"Game saved as '{filename}.pkl' using pickle" + Style.RESET_ALL)
                # William
                elif method == "shelf":
                    if filename:
                        shelve_handler = FileHandlerFactory.get_file_handler('shelve')
                        shelve_handler.save_game(self.game, filename)
                        print(Fore.GREEN + f"Game saved as '{filename}.shelf' using shelf" + Style.RESET_ALL)
                    else:
                        shelve_handler = FileHandlerFactory.get_file_handler('shelve')
                        shelve_handler.save_game(self.game)
                        print(Fore.GREEN + f"Game saved using shelf." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid save method. Use 'pickle' or 'shelf'." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"An error occurred while saving the game: {e}" + Style.RESET_ALL)
        else:
            print(
                Fore.RED
                + "You are currently not playing a game. Use 'start' to start a new game."
                + Style.RESET_ALL
            )

    # William
    def do_save_db(self, line):
        """
        Save current game state to database.
        """
        if self.game.state != State.STOPPED:
            try:
                self.database_handler.save_to_sqlite(self.game)
                print(Fore.GREEN + f"Game saved to database." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"An error occurred while saving the game: {e}" + Style.RESET_ALL)
        else:
            print(
                Fore.RED
                + "You are currently not playing a game. Use 'start' to start a new game."
                + Style.RESET_ALL
            )

    # William
    def do_load_db(self, line):
        """
        Load game state from database
        """
        try:
            loaded_game = self.database_handler.load_from_sqlite()
            if loaded_game:
                self.game = loaded_game
                self.game.image_handler.create_map_image(self.game.game_data.map, self.game.player)
                print(Fore.GREEN + "Game loaded from database." + Style.RESET_ALL)
                self.game.get_game_status()
            else:
                print(Fore.RED + "Could not load game from database." + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"An error occurred while loading the game: {e}" + Style.RESET_ALL)

    # Junho
    def do_load(self, line):
        """
        Load a saved game from a file
        """
        params = line.split()

        if len(params) < 1:
            print(Fore.RED + "Usage: load <method> <filename = optional>" + Style.RESET_ALL)
            return

        if len(params) > 3:
            print(Fore.RED + "Too many arguments. Usage: load <method> <filename = optional>" + Style.RESET_ALL)
            return

        method = params[0]
        valid_methods = ["pickle", "shelf"]  # Add more valid methods if needed

        if method not in valid_methods:
            print(
                Fore.RED + f"Invalid method: {method}. Valid methods are: {', '.join(valid_methods)}" + Style.RESET_ALL)
            return

        filename = None

        if len(params) > 1:
            filename = params[1]

        try:
            if method == "pickle":
                pickle_handler = FileHandlerFactory.get_file_handler('pickle')
                loaded_game = pickle_handler.load_game(filename)
                if loaded_game:
                    self.game = loaded_game
                    self.game.image_handler.create_map_image(self.game.game_data.map, self.game.player)
                    print(Fore.GREEN + "Game loaded from selected file" + Style.RESET_ALL)
                    self.game.get_game_status()
                else:
                    print(Fore.RED + "Could not load game from selected file" + Style.RESET_ALL)

            elif method == "shelf":
                shelve_handler = FileHandlerFactory.get_file_handler('shelve')
                loaded_game = shelve_handler.load_game(filename)

                if loaded_game:
                    self.game = loaded_game
                    self.game.image_handler.create_map_image(self.game.game_data.map, self.game.player)
                    print(Fore.GREEN + f"Game loaded from save file" + Style.RESET_ALL)
                    self.game.get_game_status()
                else:
                    print(Fore.RED + f"Could not load game from '{filename}.shelf'" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"An error occurred while loading the game: {e}" + Style.RESET_ALL)

    # Junho
    def do_help_all(self, line):
        """
        Display all available commands and descriptions
        """
        all_commands = [
            "start", "move_n", "move_e", "move_s", "move_w", "cower",
            "rotate", "place", "draw", "use_item", "search", "bury",
            "attack", "run", "get_inventory", "exit", "restart",
            "get_status", "save", "load", "help_all",
        ]
        print("Available commands and descriptions:")
        try:
            for command in all_commands:
                doc = getattr(self, f"do_{command}").__doc__
                print(f"{command}: {doc}")
        except Exception as e:
            print(Fore.RED + f"Invalid command found: {e}" + Style.RESET_ALL)

    def do_save_help(self, line):
        """
        Displays load/save commands & syntax
        """
        print(
            Fore.GREEN + "Loading\nUsage: load <method> \n\n"
            "Saving\nUsage: save <method> <filename = optional>\n\nMethods: pickle / shelf" + Style.RESET_ALL
        )
