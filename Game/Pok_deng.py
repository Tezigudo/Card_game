__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.1'
__status__ = 'working'

from time import sleep

from rich import print as printcolor
from rich.console import Console

from BaseGame import BaseGame
from Player.Hand import Screen
from Player.Player import PokDengPlayer

console = Console()


class ComputerPlayer(PokDengPlayer):
    """create an computer player for PokDeng
    """

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
        """draw one turn for computer player

        Parameters
        ----------
        game : Game
            a PokDengGame object
        """
        if self.value < 6:
            self.draw(game.deck.deck, more=True)


class Game(BaseGame):
    """PokDengGame
    """

    def __init__(self, name_list: list[str]) -> None:
        """Initialize a PokdengGame object

        Parameters
        ----------
        name_list : list of name
            list of player name
        """
        super().__init__(name_list)  # inherit previous initialize of basegame
        # create an player list that contain a list of PokdengPlayer object
        self.Player_list = [PokDengPlayer(name) for name in name_list]
        self.dealer = ComputerPlayer()  # create a dealer player object

    def draw_all_player(self) -> None:
        """Draw all player
        """
        if self.dealer.pok():
            printcolor(f'DEALER POK{self.dealer.pok()}')
            return
        self.dealer.draw_one_turn(self)
        for player in self.now_player:
            player.play_one_turn(self)

    @property
    def min_bet(self) -> int:
        """min bet of each player in the game

        Returns
        -------
        int
            a minbet of each player
        """
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 7)

    def finalize(self) -> None:
        """Finalize each player in now player(player that money > 0)
        """
        for player in self.now_player:
            player.finalize(self.dealer, win=player.if_win(self.dealer))

    def play(self) -> None:
        """play one PokDeng game
        """
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

    def show_game_wincount(self) -> None:
        """show wincount of each player in PokDengGame
        """
        name_and_wincount_dict = self.save.game_history('Pok_Deng')

        self._screen.painter.goto(-300, 260)  # goto top left
        # show a player name graphic
        self._screen.painter.pencolor('cyan')
        self._screen.painter.write('PokDengGame Score stats', True, align="left",
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
        """Show a rule of game
        """
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
        """ run a game and summary winner
        """
        super().run()  # inherit all method of run function in basegame
        try:
            # winner is the now player in the list(now it have 1 player left)
            # then it will be now_player[0]
            winner = self.now_player[0]
            console.print(f'{winner} win', style='green')
            # save score into database
            self.save.add_score('Pok_Deng', winner.name, 1)
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
        # set money for all PokDengPlayer
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

        g = Game(player_list)  # creating a game object
        g.run()
    except ValueError:  # catching exception that unnumeric input from player
        printcolor('[red]Invalid Input[/red]')
        sleep(1)
        play()


def main() -> None:
    """main func"""
    while True:
        console.print('Welcome to Pok-Deng game', style='blue')
        console.print('1.) PLay a game', style='blue')
        console.print('2.) Read rule and win condition', style='blue')
        console.print('3.) see wincount', style='blue')
        console.print('4.) Quit', style='blue')
        choice = input('Please choose(1/2/3/4): ').strip()
        match choice:
            case '1':
                play()
                printcolor(
                    'Play again? ([green]Y[/green]/[red]N[/red]): ', end='')
                tmp = input().strip()
                if tmp.upper() == 'Y':
                    play()
                elif tmp.upper() == 'N':
                    continue
                else:
                    print('Invalid input')
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
