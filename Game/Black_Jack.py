__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.1'
__status__ = 'working'

from time import sleep

from rich import print as printcolor
from rich.console import Console

import BaseGame
BaseGame = BaseGame.BaseGame
from Player.Player import BlackJackPlayer


console = Console()


class ComputerPlayer(BlackJackPlayer):
    """create an computer player for black jack"""

    num = 0

    def __init__(self) -> None:
        ComputerPlayer.num += 1
        self.name = 'BOT' + str(ComputerPlayer.num)
        self.hand = []
        self.money = self.get_initial_money()
        self.had_bet = 0
        self.played = None

    def draw_one_turn(self, game) -> None:
        """draw card until computer hand values more than 17"""
        while self.value <= 17:
            self.draw(game.deck.deck)
            if not self.check_if_hand_valid() or self.blackjack():
                break


class Game(BaseGame):
    """Entire game object"""

    def __init__(self, name_list: list[str]) -> None:
        super().__init__(name_list)
        self.Player_list = [BlackJackPlayer(name) for name in name_list]
        # create an player list
        self.dealer = ComputerPlayer()  # create an dealer player

    def show_every_player_card(self, show_len=False) -> None:
        """show every player card unblinded and show the length of it if show_len"""
        for player in self.now_player:
            player.show_unblind_card()
            if show_len:
                printcolor(f'Have {len(player.hand)} Card')
            printcolor()

    def draw_all_player(self) -> None:
        """Draw card to all payer"""
        for player in self.now_player:
            self.show_every_player_card()
            self.dealer.show_unblind_card()
            print()
            console.print(f"{player}'s Turn:", style='blue')
            player.draw_one_turn(self)
            print()
            sleep(2)
            self.clear_screen()
        self.dealer.draw_one_turn(self)

    def finalize(self) -> None:
        """Finalize the game whether player get money or lose money"""
        printcolor(f'Dealer hand are {self.dealer.hand}\nDealer Score are {self.dealer.value}\n')

        if not self.dealer.check_if_hand_valid():
            printcolor('[green]Dealer Burst[/green]:')
            for player in self.now_player:
                if player.check_if_hand_valid():
                    player.finalize(win=True)
                else:
                    player.finalize(win='Draw')

        elif self.dealer.blackjack():
            printcolor('Dealer Blackjack!')
            for player in self.now_player:
                if not player.blackjack():
                    player.finalize(win=False)
                else:
                    player.finalize(win='Draw')
        else:
            for player in self.now_player:
                player.finalize(win=player.if_win(self.dealer))

    def play(self) -> None:
        """This Func Use to play one game"""
        self.set_played()
        self.call_all()
        self.clear_screen()
        self.deal_card()
        self.draw_all_player()
        self.show_every_player_card(show_len=True)
        self.finalize()
        self.set_played()
        sleep(3.5)
        self.clear_screen()

    @staticmethod
    def show_rule() -> None:
        print()
        printcolor('[b]Black Jack Rule[/b]')
        printcolor('Value of list if win are:\n'
                   ' - if player are [green]21[/green]'
                   ' we will call it [blue]BLACKJACK[/blue]\n'
                   ' Automatically [green]win[/green] '
                   '[red]EXCEPT[/red] dealer are [blue]blackjack[/blue] too\n'
                   ' This condition player will [white]DRAW[/white]\n\n'
                   ' - if player are more than [white]21[/white]'
                   ' will automatically [red]lost money[/red]\n'
                   ' - else [green]win[/green] if value is ever '
                   '[green]more than[/green] dealer [red]lose[/red] otherwise\n')
        printcolor('Lets go to [blue]How to Play[/blue]\n'
                   'First player draw all card until player '
                   '[red]NOT CONTINUE TO DRAW[/red]\n'
                   'or PLAYER VALUE IS [red]NOT VALID[/red] '
                   'Then compare each [blue]player[/blue] and [blue]dealer[/blue] value.\n'
                   'if player [green]money[/green] is less than '
                   '0 that player [red]will be [b]ELIMINATED[/b][/red]\n')

    @property
    def min_bet(self):
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 5)

    def run(self):
        super().run()
        try:
            winner = self.now_player[0]
            console.print(f'{winner} win', style='green')
            self.save.add_score('Black_Jack', winner.name, 1)
        except IndexError:
            console.print('Dealer win', style='green')
        printcolor('_____________________' * 2 + '\n')


def play() -> None:
    """
    This function play entire game
    """
    Game.clear_screen()
    try:
        money = float(input('Enter each player money: '))
        BlackJackPlayer.set_player_money(money)
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


def main() -> None:
    """main func"""
    while True:
        console.print('Welcome to Blackjack game', style='blue')
        console.print('1.) PLay a game', style='blue')
        console.print('2.) Read rule and win condition', style='blue')
        console.print('3.) Quit', style='blue')
        choice = input('Please choose(1/2/3): ')
        match choice:
            case '1':
                play()
                printcolor('Play again? ([green]Y[/green]/[red]N[/red]): ', end='')
                tmp = input()
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
                break
            case _:
                printcolor('[red]Invalid Input[/red]')


if __name__ == '__main__':
    main()
    console.print('Thanks for Enjoy Us xD', style='blue')
