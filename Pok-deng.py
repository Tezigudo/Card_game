from Base_game import Base_game
from Player import Player


class Game(Base_game):
    def __init__(self, name_list: list[str]) -> None:
        super().__init__(name_list)

