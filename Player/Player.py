__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.0'
__status__ = 'working'

import sys
from time import sleep

sys.path.insert(1, '/'.join(sys.path[0].split('/')[:-1]))

from rich import print as printcolor
from rich.console import Console

from Hand import Screen

console = Console()


class Player:
    """define a Player object using through all card game"""

    initial_money = 0

    def __init__(self, name: str) -> None:
        """
        initialize
        hand: player's hand
        money: player's money
        had_bet: player's bet
        played: are play or not
        """
        self.name = name
        self.hand = []
        self.money = self.get_initial_money()
        self.had_bet = 0
        self.played = None
        self._screen = Screen()

    def __str__(self) -> str:
        """represent Player's name when printcolor player object"""
        return self.name

    def __repr__(self) -> str:
        """represent class name and object name"""
        return f'Player -> {self.name}'

    def __len__(self):
        return len(self.hand)

    @property
    def name(self): 
        return self._name

    @name.setter
    def name(self, name):
        if type(name) != str:
            raise TypeError('Name must be string')
        if not name:
            raise ValueError('Name cant be empty')
        if len(name) > 10:
            raise ValueError('Invalid name')
        self._name = name.capitalize()

    @classmethod
    def get_initial_money(cls):
        return cls.initial_money

    @property
    def value(self) -> int:
        """return value from calculated value """
        s = 0
        for card in self.hand:
            val = card.split()[0]
            match val:
                case 'Ace':
                    s += 1
                case 'King' | 'Queen' | 'Jack':
                    s += 10
                case _:
                    s += int(val)
        return s % 10

    @classmethod
    def set_player_money(cls, money: int) -> None:
        """set all player money when"""
        cls.initial_money = money

    def draw(self, deck, more=False) -> None:
        """print what card that draw if more is True else not printcolor"""
        tmp = deck.pop()
        self.hand.append(tmp)
        if more:
            printcolor(f'{self} has Draw [blue]{tmp}[/blue]')

    def show_hand(self) -> None:
        """Show hand of player """
        printcolor(f'{self.name} had {self.hand}')
        console.print(f'value = {self.value}')

        self._screen.show_hand(self)


    def same_card(self) -> bool:
        """ return if same card and deng """
        return len({card.split()[0] for card in self.hand}) == 1 and 1 < len(self.hand) < 4

    def bet(self, money: int) -> None:
        """bet"""
        self.money -= money
        self.had_bet = money

    def finalize(self, win=False) -> None:
        """add bet money o player if win else minus if draw do nothing
        then reset the bet money"""

        if win == 'Draw':
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')
        elif win:
            printcolor(f'{self} win and [green]got {self.had_bet}[/green]')
            self.money += self.had_bet * 2
        else:
            printcolor(f'{self} lose and [red]lost {self.had_bet}[/red]')
        printcolor(f'{self} have {self.money} left.')

    def if_win(self, dealer) -> str | bool:
        """
        check whether player win or not if draw it will return 'Draw'
        """
        if self.value == dealer.value:
            return 'Draw'
        return self.value > dealer.value

    def all_in(self) -> None:
        """ Player all in!"""
        self.bet(self.money)

    def bet_min(self, minbet) -> None:
        """ This will bet min bet"""
        self.bet(minbet)

    def call(self, minbet) -> None:
        """call for each person """
        if self.money < minbet:
            self.all_in()
            printcolor(f'{self} was [red]FORCE[/red] to [blue]ALL-IN[/blue]')
            printcolor(f'{self} have bet: {self.had_bet}')
            return
        printcolor(f'{self} amount is: {self.money}')
        while True:
            printcolor('[bold yellow](All-IN | all in | all-in | ALL IN)[/bold yellow] to [blue]ALL-IN[/blue]')
            printcolor(
                '[bold orange](MIN-BET | min bet | min-bet | MIN-BET)[/bold orange] to bet of value of [yellow]minbet[/yellow]')
            console.print(f'Please enter amount to bet ({minbet=})', end=': ')
            amount = input().strip()
            try:
                amount = float(amount)
                if amount % 1:
                    amount = round(amount)
                    printcolor(f'your amount was round to {amount}')
                    sleep(1)
                if amount < 0:
                    console.print(f'--Negative Amount--', style='red')
                    raise ValueError
                elif amount < minbet:
                    printcolor('please enter amount that [red]more than or equal[/red] to minbet')
                elif amount > self.money:
                    printcolor('you not have enough amount please try again')
                else:
                    break
            except ValueError:
                match amount:
                    case 'All-IN' | 'all in' | 'all-in' | 'ALL IN':
                        self.all_in()
                        printcolor(f'{self} [blue]ALL-IN[/blue]')
                        printcolor(f'{self} have bet: {self.had_bet}')
                        return

                    case 'MIN-BET' | 'min bet' | 'min-bet' | 'MIN-BET':
                        self.bet_min(minbet)
                        printcolor(f'{self} has bet [yellow]minimum of bet[/yellow]')
                        printcolor(f'{self} have bet: {self.had_bet}')
                        return

                    case _:
                        printcolor('[red]Invalid Input[/red] please try again:')
            print()

        self.bet(amount)
        printcolor(f'{self} have bet: {amount}')
        printcolor(f'{self} have {self.money} left.')

    def reset(self) -> None:
        self.had_bet = 0
        self.hand = []

    def show_status(self):
        printcolor(f'{self}: {"[green]IN-GAME[/green]" if self.played else "[red]LOSES[/red]"}')


class BlackJackPlayer(Player):
    """create a black jack object that inherit from player"""

    @property
    def value(self) -> int:
        """return player value"""
        s = ace_count = 0
        for card in self.hand:
            val = card.split()[0]
            match val:
                case 'Ace':
                    ace_count += 1
                case 'King' | 'Queen' | 'Jack' | 'King':
                    s += 10
                case _:
                    s += int(val)

        while ace_count:
            if s + 11 <= 23:
                s += 11
            else:
                s += 1
            ace_count -= 1

        return s

    def show_hand(self) -> None:
        """Show hand of player """
        printcolor(f'{self.name} had {self.hand}')
        if self.value < 22:
            printcolor(f'value = {self.value}')
        else:
            printcolor(f'value = [red]{self.value}[/red]')

        if self.blackjack():
            self._screen.painter.goto(-200, 190)
            self._screen.painter.pencolor('')
            self._screen.write_rainbow('BLACK JACK!')
        elif not self.check_if_hand_valid():
            self._screen.painter.goto(-80, 180)
            self._screen.painter.pencolor('orange')
            self._screen.painter.write('BURST!', True, align="left", font=("Menlo", 40, "bold"))

        self._screen.show_hand(self)

    def show_unblind_card(self) -> None:
        """show unblinded card"""
        printcolor(f'[blue]{self}:[/blue]')
        print(f'unblind is: {self.hand[0]}')

    def check_if_hand_valid(self) -> bool:
        """check whether player value less than 21"""
        return self.value < 22

    def blackjack(self) -> bool:
        """check whether player is Blackjack"""
        return self.value == 21

    def draw_one_turn(self, game) -> None:
        """draw one turn for black jack"""
        self.show_hand()
        while self.value <= 21:
            if not self.check_if_hand_valid() or self.blackjack():
                break
            ans = input('Want to draw? (Y/N): ')
            if ans.upper() == 'Y':
                self.draw(game.deck.deck, more=True)
            elif ans.upper() == 'N':
                break
            else:
                printcolor('[red]Invalid Input[/red] please try again')
            self.show_hand()

    def if_win(self, dealer) -> str | bool:
        """check whether player value more that dealer value"""
        if self.blackjack():
            return 'Blackjack'
        if not self.check_if_hand_valid():
            return 'Burst'
        if self.value == dealer.value:
            return 'Draw'
        else:
            return self.value > dealer.value

    def finalize(self, win=None) -> None:
        """Finalize Blackjack player same func as player"""

        match win:
            case 'Blackjack':
                printcolor(f'{self.name} [green]Black Jack![/green]')
                win = True
            case 'Burst':
                printcolor(f'{self.name} [red]Burst![/red]')
                win = False

        if win != 'Draw':
            if win:
                printcolor(f'{self} win and [green] {self.had_bet}[/green]')
                self.money += self.had_bet * 2
            else:
                printcolor(f'{self} lose and [red]lost {self.had_bet}[/red]')
        else:
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')
        printcolor(f'{self} have {self.money} left.')
        self.had_bet = 0


class PokDengPlayer(Player):
    """This is player for PokDeng game """

    def pok(self) -> int:
        if len(self) == 2:
            if self.value == 8:
                return 8
            if self.value == 9:
                return 9
        return 0

    def deng(self) -> int:
        """
        This will return 2 if 2 deng
                         3 if 3 deng
                         0 otherwise
        """
        if self.same_card():
            if len(self) == 2:
                return 2
            return 3
        return 0

    def draw_one_turn(self, game) -> None:
        """Draw one turn

        Parameters
        ----------
        game : Game object
            ex. BaseGame, Black_Jack
        """
        while True:
            ans = input('Want to draw? (Y/N): ')
            match ans.upper():
                case 'Y' | 'N':
                    break
                case _:
                    printcolor('[red]Invalid Input[/red] please try again')
        if ans.upper() == 'Y':
            self.draw(game.deck.deck, more=True)
        self.show_hand()
        self._screen.reset()

    def play_one_turn(self, game):

        print()
        console.print(f"{self}'s Turn:", style='blue')
        self.show_hand()
        if not self.pok():
            self.draw_one_turn(game)
        else:
            print(f'{self} POK{self.pok()}!')
        print()
        sleep(2)
        game.clear_screen()

    def finalize(self, dealer, win=False) -> None:
        """ Finallize of player in end of turn
        whatever gain or lose money

        Parameters
        ----------
        dealer : Player
            Dealer
        win : bool, optional
            win can be whatever bool or Draw, by default False
        """
        if win == 'Draw':
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')

        elif win:
            multiple = self.deng() or 1
            if self.deng():
                printcolor(
                    f'{self} {multiple}Deng!\n'
                    f'{self} hand are {self.hand} '
                    f'and [green]got[/green] {self.had_bet}x{multiple} = {self.had_bet * multiple}')
            else:
                printcolor(f'{self} win and [green]got[/green] {self.had_bet}')
            self.money += self.had_bet * (multiple + 1)

        else:
            multiple = dealer.deng()
            if dealer.deng():
                printcolor(f'Dealer {multiple}Deng!\n'
                           f'Dealer hand are {dealer.hand} '
                           f'and [red]lose[/red] {self.had_bet}x{multiple} = {self.had_bet * multiple}')
            else:
                printcolor(f'{self} lose and [red]lose[/red] {self.had_bet}')
            self.money -= self.had_bet * multiple

        printcolor(f'{self} have {self.money} left.')
        self.had_bet = 0
