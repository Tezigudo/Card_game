__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.1'
__status__ = 'working'

from time import sleep

from rich import print as printcolor
from rich.console import Console

from BaseGame import BaseGame
from Player.Player import PokDengPlayer

console = Console()


class ComputerPlayer(PokDengPlayer):
    def __init__(self) -> None:
        super().__init__(self)
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
            player.play_one_turn(self)

    @property
    def min_bet(self):
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 9)

    def finalize(self):
        for player in self.now_player:
            player.finalize(self.dealer, win=player.if_win(self.dealer))

    def play(self):
        self.set_played()
        self.call_all()
        self.clear_screen()
        self.deal_card()
        self.draw_all_player()
        self.show_every_player_card()
        self.dealer.show_hand()
        self.finalize()
        self.set_played()
        sleep(3)
        self.clear_screen()


def play() -> None:
    """
    This function play entire game
    """
    Game.clear_screen()
    try:
        money = float(input('Enter each player money: '))
        PokDengPlayer.set_player_money(money)
        player_list = []
        print()
        while True:
            name = input(f'Enter Player{len(player_list) + 1} name: ')
            player_list.append(name)
            print(f'now Playerlist: {player_list}')
            printcolor('[green]Y[/green]/[red]N[/red]', end=': ')
            tmp = input()
            match tmp:
                case 'N' | 'n':
                    break
                case 'Y' | 'y':
                    continue
                case _:
                    print('Invalid input')

        g = Game(player_list)
        g.run()
    except ValueError:
        printcolor('[red]Invalid Input[/red]')
        sleep(1)
        play()


def main():
    play()


if __name__ == '__main__':
    main()
