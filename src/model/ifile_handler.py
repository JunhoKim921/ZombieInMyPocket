"""
Module providing the IFileHandler interface.

Defines an abstract base class (ABC).
Serves as an interface for file handling operations.
"""


from abc import ABC, abstractmethod


class IFileHandler(ABC):
    """
    Interface for file handling operations.

    This interface declares methods for saving and loading game states.
    Concrete implementations must provide these methods.
    """

    @abstractmethod
    def save_game(self, game, filename):
        """
        Save a game state to a file.

        :param game: The game object to be saved.
        :param filename: The name of the file to save the game to.
        """
        pass

    @abstractmethod
    def load_game(self, filename):
        """
        Load a game state from a file.

        :param filename: The name of the file to load the game from.
        :return: The loaded game object.
        """
        pass
