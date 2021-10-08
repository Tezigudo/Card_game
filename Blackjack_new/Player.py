# from __future__ import annotations
from time import sleep

from rich import print as printcolor
from rich.console import Console

console = Console()


# @dataclass
class Player:
    """define a Player object using through all card game"""

    initial_money = 0

    def __init__(self, name: str):
        """
        initialize
        hand: player's hand
        money: player's money
        had_bet: player's bet
        played: are play or not
        """
        self.name = name
        self.hand = []
        self.money = Player.initial_money
        self.had_bet = 0
        self.played = None

    def __str__(self):
        """represent Player's name when printcolor player object"""
        return self.name

    def __repr__(self):
        """represent class name and object name"""
        return f'Player -> {self.name}'

    @property
    def value(self):
        """return value from calculated value """
        return self.calculate_val

    @value.getter
    def calculate_val(self):
        """calculate value"""
        s = 0
        for card in self.hand:
            val = card.split()[0]
            match val:
                case 'Ace':
                    s += 1
                case 'King' | 'Queen' | 'Jack' | 'King':
                    s += 10
                case _:
                    s += int(val)
        return s

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

    def show_hand(self):
        """Show hand of player """
        printcolor(f'{self.name} had {self.hand}')
        if self.value < 22:
            printcolor(f'value = {self.value}')
        else:
            printcolor(f'value = [red]{self.value}[/red]')

    def bet(self, money: int) -> None:
        """bet"""
        self.money -= money
        self.had_bet = money

    def finalize(self, win=False) -> None:
        """add bet money o player if win else minus if draw do nothing
        then reset the bet money"""

        if win != 'Draw':
            if win:
                printcolor(f'{self} win and [green]got {self.had_bet}[/green]')
                self.money += self.had_bet * 2
            else:
                printcolor(f'{self} lose and [red]lost {self.had_bet}[/red]')
        else:
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')
        printcolor(f'{self} have {self.money} left.')

    def if_win(self, dealer) -> str | bool:
        """check whether player value more that dealer value"""
        if self.value == dealer.value:
            return 'Draw'
        else:
            return self.value > dealer.value

    def all_in(self) -> None:
        self.bet(self.money)

    def call(self):
        """
        call for each person
        :return: None
        """
        printcolor(f'{self} amount is: {self.money}')
        while True:
            printcolor('[yellow](All-IN | all in | all-in | ALL IN)[/yellow] to all in')
            amount = input('Please enter amount to bet: ')
            try:
                amount = float(amount)
                if amount % 1:
                    amount = round(amount)
                    printcolor(f'your amount was round to {amount}')
                    sleep(1)
                if amount > self.money:
                    printcolor('you not have enough amount please try again')
                elif amount < 0:
                    console.print(f'--Negative Amount--', style='red')
                    raise ValueError
                else:
                    break
            except ValueError:
                match amount:
                    case 'All-IN' | 'all in' | 'all-in' | 'ALL IN':
                        self.all_in()
                        printcolor(f'{self} [blue]ALL-IN[/blue]')
                        printcolor(f'{self} have bet: {self.had_bet}')
                        return

                    case _:
                        printcolor('[red]Invalid Input[/red] please try again:')
            print()

        self.bet(amount)
        printcolor(f'{self} have bet: {amount}')
        printcolor(f'{self} have {self.money} left.')

    def reset(self):
        self.had_bet = 0
        self.hand = []


class BlackJackPlayer(Player):
    """create a black jack object that inherit from player"""

    def __init__(self, name):
        """

        :param name: str
        """
        super().__init__(name)
        self.money = BlackJackPlayer.initial_money

    @property
    def value(self):
        """return player value"""
        return self.calculate_val

    @value.getter
    def calculate_val(self):
        """calculate value for player and return in"""
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

    def show_unblind_card(self):
        """show unblinded card"""
        printcolor(f'[blue]{self}:[/blue]')
        print(f'unblind is: {self.hand[0]}')

    def check_if_hand_valid(self):
        """check whether player value less than 21"""
        return self.value < 22

    def blackjack(self):
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
            return 'BlackJack'
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
                printcolor(f'{self} win and [green]got {self.had_bet}[/green]')
                self.money += self.had_bet * 2
            else:
                printcolor(f'{self} lose and [red]lost {self.had_bet}[/red]')
        else:
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')
        printcolor(f'{self} have {self.money} left.')
        self.had_bet = 0
