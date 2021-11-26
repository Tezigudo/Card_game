
import sys
from time import sleep
from math import floor
# make the path is Card_Game
sys.path.insert(1, '/'.join(sys.path[0].split('/')[:-1]))

from rich import print as printcolor
from rich.console import Console

from Hand import Screen

console = Console()


class Player:
    """define a Player object using through all card game"""

    initial_money = 0

    def __init__(self, name: str) -> None:
        """initialize

        Parameters
        ----------
        name : str
            name of each player
        """
        self.name = name
        self.hand = []
        self.money = self.get_initial_money()
        self.had_bet = 0
        self.played = None
        self._screen = Screen()

    def __str__(self) -> str:
        """represent Player'current_val name when printcolor player object"""
        return self.name

    def __repr__(self) -> str:
        """represent class name and object name"""
        return f'Player -> {self.name}'

    def __len__(self) -> int:
        return len(self.hand)

    @property
    def name(self) -> str:
        """get or set value of name

        Returns
        -------
        str
            str of name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        # check whether name is string or not
        if not isinstance(name, str):
            raise TypeError('Name must be string')
        # check if name not empty ('')
        if not name:
            raise ValueError('Name cant be empty')
        # check if name is less than 10 character
        if len(name) > 10:
            raise ValueError('Invalid name')
        # set value of new name
        self._name = name.capitalize()

    @classmethod
    def get_initial_money(cls) -> int:
        """get initial money of each player in that Game

        Returns
        -------
        int
            player initial money
        """
        return cls.initial_money

    @property
    def value(self) -> int:
        """return value from calculated value """
        current_val = 0
        for card in self.hand:
            val = card.split()[0]
            match val:
                case 'Ace':
                    current_val += 1
                case 'King' | 'Queen' | 'Jack':
                    current_val += 10
                case _:
                    current_val += int(val)
        return current_val % 10

    @classmethod
    def set_player_money(cls, money: int) -> None:
        """set all player money

        Parameters
        ----------
        money : int
            money that want to set

        Raises
        ------
        ValueError
            raise if money is invalid
        """
        money = floor(money)
        if money <= 0:  # check if valid money
            printcolor('[red]Money cant be less than or equal zero[/red]')
            raise ValueError
        cls.initial_money = money  # set money

    def draw(self, deck: list, more=False) -> None:
        """print what card that draw if more is True else not printcolor

        Parameters
        ----------
        deck : list
            list of deck
        more : bool, optional
            it will be True when it isnt initial draw(dealcard), by default False
        """
        tmp = deck.pop()
        self.hand.append(tmp)
        if more:
            printcolor(f'{self} has Draw [blue]{tmp}[/blue]')

    def show_hand(self) -> None:
        """Show hand of player """
        printcolor(f'{self.name} had {self.hand}')
        console.print(f'value = {self.value}')

    def bet(self, money: int) -> None:
        """bet

        Parameters
        ----------
        money : int
            money of player'current_val bet
        """
        self.money -= money
        self.had_bet = money

    def finalize(self, win=False) -> None:
        """add bet money o player if win else minus if draw do nothing
        then reset the bet money

        Parameters
        ----------
        win : bool, optional
            win can be Draw or bool, by default False
        """

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
        """check whether player win or not if draw it will return 'Draw'

        Returns
        -------
        str or bool
            Draw or True or False
        """
        if self.value == dealer.value:
            return 'Draw'
        return self.value > dealer.value

    def all_in(self) -> None:
        """ Player all in!"""
        self.bet(self.money)

    def bet_min(self, minbet: int) -> None:
        """This will bet min bet

        Parameters
        ----------
        minbet : int
            minbet of each player
        """
        self.bet(minbet)

    def call(self, minbet: int) -> None:
        """call for each person

        Parameters
        ----------
        minbet : int
            minbet of each player

        Raises
        ------
        ValueError
            if amount less than zero
        ValueError
            if amount equal zero
        """
        # if player money less than minbet those player will be force to all in
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
                if amount % 1:  # check if amount was not integer
                    amount = round(amount)  # round the amount into integer
                    printcolor(f'your amount was round to {amount}')
                    sleep(1)

                if not amount:  # if amount is zero ValueError must be raise
                    console.print(f'--Amount can not be zero--', style='red')
                    raise ValueError

                if amount < 0:  # if amount lessthan zero ValueError must be raise too
                    console.print(f'--Negative Amount--', style='red')
                    raise ValueError

                elif amount < minbet:  # id amount less than minbet user must enter a valid money
                    printcolor('please enter amount that [red]more than or equal[/red] to minbet')
        
                elif amount > self.money:  # if amount more than player money user must enter a valid money
                    printcolor('you not have enough amount please try again')
                else:
                    # if every thing go fine will break the loop
                    break
            except ValueError:
                # Catch if user enter (all in) or (min bet)
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

        self.bet(amount)  # bet the money
        printcolor(f'{self} have bet: {amount}')
        printcolor(f'{self} have {self.money} left.')

    def reset(self) -> None:
        """reset the one turn game
        """
        self.had_bet = 0
        self.hand = []

    def show_status(self):
        """show status of player
        """
        printcolor(f'{self}: {"[green]IN-GAME[/green]" if self.played else "[red]LOSES[/red]"}')


class BlackJackPlayer(Player):
    """This is a player for BlackJackGame"""

    @property
    def value(self) -> int:
        """get player value

        Returns
        -------
        int
            value of player hand
        """
        current_val = ace_count = 0
        for card in self.hand:
            val = card.split()[0]
            match val:
                case 'Ace':
                    ace_count += 1
                case 'King' | 'Queen' | 'Jack' | 'King':
                    current_val += 10
                case _:
                    current_val += int(val)

        # calculate value of ace card if player have ace card in hand
        # by default ace value is 11
        # if current val + ace val and burst ace val will be 1
        while ace_count:
            if current_val + 11 <= 21:
                current_val += 11
            else:
                current_val += 1
            ace_count -= 1

        return current_val

    def show_hand(self) -> None:
        """Show hand of player
        """

        # terminal output

        printcolor(f'{self.name} had {self.hand}')
        # if player valid value output in terminal will be oridinary color
        if self.value < 22:
            printcolor(f'value = {self.value}')
        # red otherwise(Burst)
        else:
            printcolor(f'value = [red]{self.value}[/red]')

        # Grahical output

        # write a BLACKJACK! with rainbow color(graphic) if player blackjack
        if self.blackjack():
            self._screen.painter.goto(-200, 160)
            self._screen.painter.pencolor('')
            self._screen.write_rainbow('BLACK JACK!')
        # write a BURST with orange color if player burst
        elif not self.check_if_hand_valid():
            self._screen.painter.goto(-80, 150)
            self._screen.painter.pencolor('orange')
            self._screen.painter.write('BURST!', True, align="left", font=("Menlo", 40, "bold"))

        self._screen.show_hand(self)  # show a player hand with graphic

    def show_unblind_card(self) -> None:
        """show unblinded card
        """
        printcolor(f'[blue]{self}:[/blue]')
        print(f'unblind is: {self.hand[0]}')

    def check_if_hand_valid(self) -> bool:
        """check whether player value less than 21

        Returns
        -------
        bool
            True if valid hand otherwise False 
        """
        return self.value < 22

    def blackjack(self) -> bool:
        """check whether player is Blackjack

        Returns
        -------
        bool
            True if player Blackjack otherwise False
        """
        return self.value == 21

    def draw_one_turn(self, game) -> None:
        """draw one turn for black jack player

        Parameters
        ----------
        game : Game object
            BlackJackGame object
        """
        self.show_hand()  # show player hand
        while self.value <= 21:  # loop until player is burst
            # if player burst or player black jack will break the loop
            if not self.check_if_hand_valid() or self.blackjack():
                break
            ans = input('Want to draw? (Y/N): ').strip()
            if ans.upper() == 'Y':
                self.draw(game.deck.deck, more=True)  # draw more card to player
            elif ans.upper() == 'N':
                break
            else:
                printcolor('[red]Invalid Input[/red] please try again')
            self.show_hand()  # show hand of the player after player enter a value

    def if_win(self, dealer) -> str | bool:
        """check whether player value more that dealer value

        Parameters
        ----------
        dealer : BlackJackPlayer object

        Returns
        -------
        bool or string
            if blackjack burst or draw it will return each word
            by default, it will return if current value is morethan dealer value
        """
        if self.blackjack():
            return 'Blackjack'
        if not self.check_if_hand_valid():
            return 'Burst'
        if self.value == dealer.value:
            return 'Draw'
        else:
            return self.value > dealer.value

    def finalize(self, win=None) -> None:
        """Finalize Blackjack player same func as player

        Parameters
        ----------
        win : bool, str
            win can be Blackjack, Burst or Draw, by default None (False)
        """

        match win:
            # if player blackjack win be set to True
            # and will print green color text that player are blackjack
            case 'Blackjack':
                printcolor(f'{self.name} [green]Black Jack![/green]')
                win = True
            # if player burst win be set to False
            # and will print red color text that player are burst
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
        self.had_bet = 0  # reset a bet money


class PokDengPlayer(Player):
    """This is player for PokDeng game """

    def same_card(self) -> bool:
        """return if same card and deng 

        Returns
        -------
        bool
            if valid hand(length hand < 4) and have same card it will be True
        """
        return len({card.split()[0] for card in self.hand}) == 1 and 1 < len(self.hand) < 4

    def pok(self) -> int:
        """check if player pok or not
        player will pok when have number of card in hand equal 2
        and value is 8 or 9

        Returns
        -------
        int
            if pok
                8 will return 8
                9 will return 9
            0 otherwise (bool 0 is False)
        """

        if len(self) == 2:
            if self.value == 8:
                return 8
            if self.value == 9:
                return 9
        return 0

    def deng(self) -> int:
        """check if player deng or not

        Returns
        -------
        int
            2 if 2 deng
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

    def show_hand(self) -> None:
        """ show hand of player
        """

        # inherit all method from show_hand() function from player
        # is the terminal output
        super().show_hand()

        # display a graphic output

        self._screen.painter.pencolor('white')
        self._screen.painter.goto(-300, 200)  # move painter to top left
        self._screen.painter.write('Pok: ', True, align="left", font=("Menlo", 20, "bold"))
        self._screen.painter.pencolor('cyan')
        self._screen.painter.write(self.pok() or 'None', True, align="left", font=("Menlo", 20, "bold"))

        self._screen.painter.pencolor('white')
        self._screen.painter.goto(-300, 170)
        self._screen.painter.write('Deng: ', True, align="left", font=("Menlo", 20, "bold"))
        self._screen.painter.pencolor('cyan')
        self._screen.painter.write(self.deng() or 'None', True, align="left", font=("Menlo", 20, "bold"))
        self._screen.painter.pencolor('white')

        self._screen.show_hand(self)  # show card in hand by graphic


    def play_one_turn(self, game) -> None:
        """play one turn for PokdengPlayer

        Parameters
        ----------
        game : Game object (PokDengGame)
            this is from module PokDengGame
        """

        print()
        console.print(f"{self}'current_val Turn:", style='blue')
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
        if win == 'Draw':  # check if draw
            self.money += self.had_bet
            printcolor(f'{self} [b]Draw[/b]')

        elif win:  # check if win
            multiple = self.deng() or 1  # check if deng else multiple will be 1
            if self.deng():
                printcolor(
                    f'{self} {multiple}Deng!\n'
                    f'{self} hand are {self.hand} '
                    f'and [green]got[/green] {self.had_bet}x{multiple} = {self.had_bet * multiple}')
            else:
                printcolor(f'{self} win and [green]got[/green] {self.had_bet}')
            # append money to player money
            self.money += self.had_bet * (multiple + 1)

        else:
            multiple = dealer.deng()  # dealer multiple
            if dealer.deng():
                printcolor(f'Dealer {multiple}Deng!\n'
                           f'Dealer hand are {dealer.hand} '
                           f'and [red]lose[/red] {self.had_bet}x{multiple} = {self.had_bet * multiple}')
            else:
                printcolor(f'{self} lose and [red]lose[/red] {self.had_bet}')
            self.money -= self.had_bet * multiple

        printcolor(f'{self} have {self.money} left.')
        self.had_bet = 0
