"""
This is PokDeng Game that contain ComputerPlayer and Game
"""

from time import sleep

from rich import print as printcolor
from rich.console import Console

import BaseGame
from Player.Hand import Screen
from Player.Player import BlackJackPlayer

BaseGame = BaseGame.BaseGame

console = Console()


class ComputerPlayer(BlackJackPlayer):
    """create an computer player for black jack"""

    def __init__(self) -> None:
        """Initialize a pokdeng computer player
        with name is dealer
        """
        self.name = 'Dealer'
        self.hand = []
        self.money = self.get_initial_money()
        self.had_bet = 0
        self.played = None
        self._screen = Screen()

    def draw_one_turn(self, game) -> None:
        """draw card until computer hand values more than 17"""
        while self.value <= 17:
            self.draw(game.deck.deck)
            if not self.check_if_hand_valid() or self.blackjack():
                break


class Game(BaseGame):
    """BlackJackGame"""

    def __init__(self, name_list: list[str]) -> None:
        """Initialize a BlackJackGame with playerlist and dealer

        Parameters
        ----------
        name_list : list[str]
            list of player name
        """
        super().__init__(name_list)  # inherit previous initialize of basegame
        self.Player_list = [BlackJackPlayer(name) for name in name_list]
        # create an player list that contain a BlackJackPlayer object
        self.dealer = ComputerPlayer()  # create an dealer player

    def show_every_player_card(self, show_len=False) -> None:
        """show every player card unblinded and show the length of it if show_len

        Parameters
        ----------
        show_len : bool
            if show len it will show number of card in player hand, by default False
        """
        # iterate over player in now player(money > 0)
        for player in self.now_player:
            player.show_unblind_card()
            if show_len:
                printcolor(f'Have {len(player.hand)} Card')
            printcolor()

    def draw_all_player(self) -> None:
        """Draw card to all payer
        """
        # iterate over player in now player(money > 0)
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
        """Finalize the game whether player get money or lose money
        """

        self.dealer.show_hand()
        # check dealer hand
        if not self.dealer.check_if_hand_valid():
            printcolor('[green]Dealer Burst[/green]:')
            for player in self.now_player:
                if player.check_if_hand_valid():
                    player.finalize(win=True)
                else:
                    player.finalize(win='Draw')

        # check whether dealer are blackjack
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

    def show_game_wincount(self):
        name_and_wincount_dict = self.save.game_history('Black_Jack')

        self._screen.painter.goto(-300, 260)  # goto top left
        # show a player name graphic
        self._screen.painter.pencolor('cyan')
        self._screen.painter.write('BlackJackGame Score stats', True, align="left",
                                   font=("Menlo", 30, "bold"))
        self._screen.painter.goto(-300, 200)
        self._screen.painter.pencolor('white')
        self._screen.painter.write('name        wincount', True, align="left",
                                   font=("Menlo", 28, "bold"))
        curr_x, curr_y = -300, 160
        self._screen.painter.pencolor('cyan')
        for name, win_count in name_and_wincount_dict.items():
            self._screen.painter.goto(curr_x, curr_y)
            self._screen.painter.write(f'{name:<6}     {win_count:>6}', True, align="left",
                                       font=("Menlo", 28, "bold"))
            curr_y -= 35
        sleep(2)
        self._screen.reset()

    @staticmethod
    def show_rule() -> None:
        """Show rule of the game
        """
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
        """return a minbet of each player for each player in game

        Returns
        -------
        int
            min bet of each player
        """
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 5)

    def run(self):
        """run a game
        """
        super().run()  # inherit all method of run function in basegame
        try:
            # winner is the now player in the list(now it have 1 player left)
            # then it will be now_player[0]
            winner = self.now_player[0]
            console.print(f'{winner} win', style='green')
            # save score into database
            self.save.add_score('Black_Jack', winner.name, 1)
        except IndexError:  # catching exception if all player loses then dealer will win
            console.print('Dealer win', style='green')
        printcolor('_____________________' * 2 + '\n')


def play() -> None:
    """
    This function play entire game
    """
    Game.clear_screen()
    try:
        money = float(input('Enter each player money: ').strip())
        # set money for all BlackJackPlayer
        BlackJackPlayer.set_player_money(money)
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

        g = Game(player_list)  # creating a game object
        g.run()  # run a game
    except ValueError:  # catching exception that unnumeric input from player
        printcolor('[red]Invalid Input[/red]')
        sleep(1)
        play()


def main() -> None:
    """main func"""
    while True:
        console.print('Welcome to Blackjack game', style='blue')
        console.print('1.) PLay a game', style='blue')
        console.print('2.) Read rule and win condition', style='blue')
        console.print('3.) see wincount', style='blue')
        console.print('4.) Quit', style='blue')
        choice = input('Please choose(1/2/3): ').strip()
        print()
        match choice:
            case '1':
                play()
                printcolor(
                    'Play again? ([green]Y[/green]/[red]N[/red]): ', end='')
                tmp = input().strip()
                if tmp.upper() == 'Y':
                    play()
                elif tmp.upper() == 'N':
                    Game.clear_screen()
                    continue
                else:
                    printcolor('[red]Invalid input[/red]')
                    Game.clear_screen()
                    continue
            case '2':
                Game.show_rule()  # showrule
            case '3':
                gam = Game(['God'])
                gam.show_game_wincount()
            case '4':
                for i in range(3, 0, -1):  # countdown
                    printcolor(f'Game will exit in {i}', end='\r')
                    sleep(1)
                print()
                break
            case _:
                printcolor('[red]Invalid Input[/red]')
        print()


if __name__ == '__main__':
    main()
    console.print('Thanks for Enjoy Us xD', style='blue')
