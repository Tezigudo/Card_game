__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.0'
__status__ = 'working'

from time import sleep

from rich import print as printcolor
from rich.console import Console

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
        self.money = Player.initial_money
        self.had_bet = 0
        self.played = None

    def __str__(self) -> str:
        """represent Player's name when printcolor player object"""
        return self.name

    def __repr__(self) -> str:
        """represent class name and object name"""
        return f'Player -> {self.name}'

    def __len__(self):
        return len(self.hand)

    @property
    def value(self) -> int:
        """return value from calculated value """
        return self.calculate_val

    @value.getter
    def calculate_val(self) -> int:
        """calculate value"""
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

    def show_hand(self) -> None:
        """Show hand of player """
        printcolor(f'{self.name} had {self.hand}')
        console.print(f'value = {self.value}')

    def same_card(self) -> bool:
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
        """check whether player value more that dealer value"""
        if self.value == dealer.value:
            return 'Draw'
        else:
            return self.value > dealer.value

    def all_in(self) -> None:
        """ Player all in!"""
        self.bet(self.money)

    def bet_min(self, minbet) -> None:
        """ Thhis will bet min bet"""
        self.bet(minbet)

    def call(self, minbet) -> None:
        """
        call for each person
        :return: None
        """
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
            amount = input()
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

    def __init__(self, name) -> None:
        """

        :param name: str
        """
        super().__init__(name)
        self.money = BlackJackPlayer.initial_money

    @property
    def value(self) -> int:
        """return player value"""
        return self.calculate_val

    @value.getter
    def calculate_val(self) -> int:
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

    def show_hand(self) -> None:
        """Show hand of player """
        printcolor(f'{self.name} had {self.hand}')
        if self.value < 22:
            printcolor(f'value = {self.value}')
        else:
            printcolor(f'value = [red]{self.value}[/red]')

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
                printcolor(f'{self} win and [green]got {self.had_bet}[/green]')
                self.money += self.had_bet * 2
            else:
                printcolor(f'{self} lose and [red]lost {self.had_bet}[/red]')
        else:
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')
        printcolor(f'{self} have {self.money} left.')
        self.had_bet = 0


class PokDengPlayer(Player):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.money = PokDengPlayer.initial_money

    def pok(self):
        if len(self) == 2:
            if self.value == 8:
                return 'Pok8'
            if self.value == 9:
                return 'Pok9'
        return False

    def deng(self) -> str | bool:
        if self.same_card():
            if len(self) == 2:
                return '2Deng'
            return '3Deng'
        return False

    def if_win(self, dealer) -> bool:

        if self.value == dealer.value:
            return 'Draw'
        return self.value > dealer.value

    def finalize(self, win=False, dealer_isDeng=False) -> None:

        if win:
            match self.deng():
                case 'Draw':
                    self.money += self.had_bet
                    printcolor(f'{self} [b]Draw[/b]')

                case '2Deng':
                    printcolor(f'{self} 2Deng! and got {self.had_bet}x2 = {self.had_bet * 2}')
                    self.money += self.had_bet * 3
                case '3Deng':
                    printcolor(f'{self} 3Deng! and got {self.had_bet}x3 = {self.had_bet * 3}')
                    self.money += self.had_bet * 4
                case _:
                    printcolor(f'{self} win and got {self.had_bet}')
                    self.money += self.had_bet * 2

        else:
            match dealer_isDeng:
                case '2Deng':
                    printcolor('Dealer 2Deng!'
                               f'{self} [red]lose[/red] {self.had_bet}x2 = {self.had_bet * 2}')
                    self.money -= self.had_bet
                case '3Deng':
                    printcolor('Dealer 3Deng!'
                               f'{self} [red]lose[/red] {self.had_bet}x3 = {self.had_bet * 3}')
                    self.money -= self.had_bet * 2
                case _:
                    printcolor('Dealer win'
                               f'{self} [red]lose[/red] {self.had_bet}')

        printcolor(f'{self} have {self.money} left.')
        self.had_bet = 0
