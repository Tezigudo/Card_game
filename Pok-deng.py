__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.1'
__status__ = 'working'


from Base_game import Base_game
from Player import Player


class Game(Base_game):
    def __init__(self, name_list: list[str]) -> None:
        super().__init__(name_list)

# NOTE: check if less than or equal using __lt__
