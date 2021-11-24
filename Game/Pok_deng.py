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
from Player.Hand import Screen

console = Console()


class ComputerPlayer(PokDengPlayer):
    def __init__(self) -> None:
        self.name = 'Dealer'
        self.hand = []
        self.money = self.get_initial_money()
        self.had_bet = 0
        self.played = None
        self._screen = Screen()

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
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 7)

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

    @staticmethod
    def show_rule() -> None:
        print()
        printcolor('[b]Pok deng Rule[/b]')
        printcolor('list of value in Pokdeng game are:\n'
                   '[blue]POK8[/blue] and [blue]POK9[/blue] --> Player have 2 card and value are 8 and 9\n'
                   '[blue]multiple[/blue] [cyan]DENG[/cyan] --> Player have all same val but not same suit(optional)\n'
                   'and will get  a [blue]multiple[/blue]X of money'
                   'Player won whether value more then dealer\n')
        printcolor('At first Every player bet\n'
                   'Then Dealer Deal 2 card to each Player hand'
                   '(Include himself)\n'
                   'then each player will choose whether to [cyan]draw or not[/cyan]\n'
                   'if [blue]Dealer POK[/blue] each player [red]will not able to Draw more[/red]\n'
                   'but if player pok! Player will be judge whether [green]gain[/green] or [red]lose[/red]\n')

    def run(self):
        super().run()
        try:
            winner = self.now_player[0]
            console.print(f'{winner} win', style='green')
            self.save.add_score('Pok_Deng', winner.name, 1)
        except IndexError:
            console.print('Dealer win', style='green')
        printcolor('_____________________' * 2 + '\n')


def play() -> None:
    """
    This function play entire game
    """
    Game.clear_screen()
    try:
        money = float(input('Enter each player money: ').strip())
        PokDengPlayer.set_player_money(money)
        player_list = []
        print()
        while True:
            name = input(f'Enter Player{len(player_list) + 1} name: ').strip()
            player_list.append(name)
            print(f'now Playerlist: {player_list}')
            printcolor('[green]Y[/green]/[red]N[/red]', end=': ')
            tmp = input().strip()
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


def main() -> None:
    """main func"""
    while True:
        console.print('Welcome to Pok-Deng game', style='blue')
        console.print('1.) PLay a game', style='blue')
        console.print('2.) Read rule and win condition', style='blue')
        console.print('3.) Quit', style='blue')
        choice = input('Please choose(1/2/3): ').strip()
        match choice:
            case '1':
                play()
                printcolor('Play again? ([green]Y[/green]/[red]N[/red]): ', end='')
                tmp = input().strip()
                if tmp.upper() == 'Y':
                    play()
                elif tmp.upper() == 'N':
                    continue
                else:
                    print('Invalid input')

                    continue
            case '2':
                Game.show_rule()
            case '3':
                for i in range(3, 0, -1):
                    printcolor(f'Game will exit in {i}', end='\r')
                    sleep(1)
                print()
                break
            case _:
                printcolor('[red]Invalid Input[/red]')
        print()


if __name__ == '__main__':
    main()
