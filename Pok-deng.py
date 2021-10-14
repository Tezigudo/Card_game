__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.1'
__status__ = 'working'

from time import sleep

from rich import print as printcolor
from rich.console import Console

from BaseGame import BaseGame
from Player import PokDengPlayer

c = Console()


class ComputerPlayer(PokDengPlayer):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Dealer'

    def draw_one_turn(self):
        pass


class Game(BaseGame):
    def __init__(self, name_list: list[str]) -> None:
        super().__init__(name_list)
        self.Player_list = [PokDengPlayer(name) for name in name_list]


def main():
    pass


if __name__ == '__main__':
    printcolor('this will tmp execute')
    sleep(3)
