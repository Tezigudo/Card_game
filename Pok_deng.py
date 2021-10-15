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

console = Console(color_system='windows')


class ComputerPlayer(PokDengPlayer):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Dealer'

    def draw_one_turn(self, game) -> None:
        if self.value < 6:
            self.draw(game.deck.deck, more=True)


class Game(BaseGame):
    def __init__(self, name_list: list[str]) -> None:
        super().__init__(name_list)
        self.Player_list = [PokDengPlayer(name) for name in name_list]
        self.dealer = ComputerPlayer()

    def draw_all_player(self) -> None:
        if self.dealer.pok():
            printcolor(f'DEALER POK{self.dealer.pok()}')
            return
        self.dealer.draw_one_turn(self)
        for player in self.now_player:
            player.play_one_turn()

    def finallize(self):
        for player in self.Player_list:
            player.finalize(win=player.if_win(self.dealer), dealer_deng=self.dealer.deng())

    def play(self):
        self.set_played()
        self.call_all()
        self.clear_screen()
        self.deal_card()
        self.draw_all_player()
        self.show_every_player_card()
        self.finalize()
        self.set_played()
        sleep(3.5)
        self.clear_screen()


def main():
    pass


if __name__ == '__main__':
    printcolor('this will tmp execute')
    sleep(3)
