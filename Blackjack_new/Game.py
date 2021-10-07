# from __future__ import annotations
# from typing import List
from Card import Card
from Player import BlackJackPlayer
from time import sleep
from rich.console import Console
from rich import print as printcolorcolour

console = Console()


class ComputerPlayer(BlackJackPlayer):
    """create an computer player for black jack"""

    num = 0

    def __init__(self):
        super().__init__(self)
        ComputerPlayer.num += 1
        self.name = 'BOT' + str(ComputerPlayer.num)

    def draw_one_turn(self, game):
        """draw card until computer hand values more than 17"""
        while self.value <= 17:
            self.draw(game.deck.deck)
            if not self.check_if_hand_valid() or self.blackjack():
                break


class Game:
    """Entire game object"""

    def __init__(self, name_list: list[str]):
        self.Player_list = [BlackJackPlayer(name) for name in name_list]
        # create an player list
        self.dealer = ComputerPlayer()  # create an dealer player
        self.deck = Card()

    def deal_card(self):
        """deal card to all player"""
        for _ in range(2):
            self.dealer.draw(self.deck.deck)
            for player in self.now_player:
                player.draw(self.deck.deck)

    def show_every_player_card(self, show_len=False):
        """show every player card unblinded and show the length of it if show_len"""
        for player in self.now_player:
            player.show_unblined_card()
            if show_len:
                printcolor(f'Have {len(player.hand)} Card')
            printcolor()

    def draw_all_player(self):
        """Draw card to all payer"""
        self.show_every_player_card()
        self.dealer.show_unblined_card()
        printcolor()

        for player in self.now_player:
            console.printcolor(f"{player}'s Turn:", style='blue')
            player.draw_one_turn(self)
            printcolor()
        self.dealer.draw_one_turn(self)

    def finalize(self):
        """Finalize the game whether player get money or lose money"""
        printcolor(f'Dealer hand are {self.dealer.hand}\nDealer Score are {self.dealer.value}\n')

        if not self.dealer.check_if_hand_valid():
            printcolor('Dealer Burst:')
            for player in self.now_player:
                if player.check_if_hand_valid:
                    player.finalize(win=True)
                else:
                    player.finalize(win='Draw')

        elif self.dealer.blackjack():
            printcolor('Dealer Blackjack!')
            for player in self.now_player:
                if player.value != 21:
                    player.finalize(win=False)
                else:
                    player.finalize(win='Draw')
        else:
            for player in self.now_player:
                player.finalize(win=player.if_win(self.dealer))

    def call_all(self):
        """call all Player"""
        for player in self.now_player:
            player.call()
            printcolor()

    def set_played(self):
        for player in self.Player_list:
            if player.money > 0:
                player.played = True
            else:
                player.played = False

    def play(self):
        """This Func Use to play one game"""
        self.set_played()
        self.call_all()
        self.deal_card()
        self.draw_all_player()
        self.show_every_player_card(show_len=True)
        self.finalize()
        self.set_played()

    @property
    def now_player(self):
        """return an player which not knock(money>=0)"""
        return [player for player in self.Player_list if player.played]

    def reset(self):
        self.deck.reset()
        self.dealer.reset()
        for player in self.Player_list:
            player.reset()

    def run(self):
        time = 0
        while len(self.now_player) > 1 or time == 0:
            time += 1
            printcolor(f'round{time}:')
            self.play()
            self.reset()
            printcolor('_____________________' * 2 + '\n')
        else:
            try:
                console.printcolor(f'{self.now_player[0]} win', style='green')
            except IndexError:
                console.printcolor('Dealer win', style='green')
            printcolor('_____________________' * 2 + '\n')

def play_one_ronud():
    money = float(input('Enter each player money: '))
    BlackJackPlayer.set_player_money(money)
    g = Game(['God', 'Tonwan'])
    g.run()


def main():
    """main func"""
    while True:
        console.printcolor('Welcome to Blackjack game', style='blue')
        console.printcolor('1.) PLay a game', style='blue')
        console.printcolor('2.) Read rule and win condition', style='blue')
        console.printcolor('3.) Quit', style='blue')
        choice = input('Please choose(1/2/3)')
        match choice:
            case '1':
                play_one_ronud()
                printcolor('Play again? ([green]Y[/green]/[red]N[/red])')
                
            case '2':
                # TODO: Do the rule of blackjack
                pass
            case '3':
                for i in range(3, 0, -1):
                    printcolor(f'Game will exit in {i}', end='\r')
                    sleep(1)
                break
            case _:
                printcolor('[red]Invalid Input[/red]')


if __name__ == '__main__':
    main()
    console.printcolor('Thanks for Enjoy Us xD', style='blue')
