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
        self.dealer.draw_one_turn(self)
        for player in self.Player_list:
            print()
            console.print(f"{player}'s Turn:", style='blue')
            player.show_hand()
            if not player.pok():
                player.draw_one_turn(self)
            else:
                print(f'{player} POK{player.pok()}!')
            print()
            sleep(2)
            self.clear_screen()



    def play(self):
        self.deal_card()





def main():
    pass


if __name__ == '__main__':
    printcolor('this will tmp execute')
    sleep(3)
