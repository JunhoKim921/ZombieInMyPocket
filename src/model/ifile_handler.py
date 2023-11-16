from abc import ABC, abstractmethod


class IFileHandler(ABC):
    @abstractmethod
    def save_game(self, game, filename):
        pass

    @abstractmethod
    def load_game(self, filename):
        pass
