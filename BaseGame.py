__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.0'
__status__ = 'working'

import os
from time import sleep

from rich.console import Console
from rich import print as printcolor
from Card import Card
from Player import Player

console = Console(color_system='windows')


class BaseGame:
    def __init__(self, name_list: list[str]) -> None:
        self.Player_list = [Player(name) for name in name_list]
        # create an player list
        self.deck = Card()

    def report_status(self):
        print('current Game status:')
        for player in self.Player_list:
            player.show_status()

    def call_all(self) -> None:
        """call all Player"""
        min_bet = self.min_bet
        for player in self.now_player:
            player.call(minbet=min_bet)
            sleep(1)
            print()

    def deal_card(self) -> None:
        """deal card to all player"""
        for _ in range(2):
            self.dealer.draw(self.deck.deck)
            for player in self.now_player:
                player.draw(self.deck.deck)

    def show_every_player_card(self) -> None:
        for player in self.now_player:
            console.print(f'{player}:', style='bold cyan')
            print(f'{player} hand are: {player.hand}')
            console.print(f'value: {player.value}')
            print()

    def set_played(self) -> None:
        for player in self.Player_list:
            player.played = player.money > 0

    @property
    def now_player(self) -> list[Player]:
        """return an player which not knock(money>=0)"""
        return [player for player in self.Player_list if player.played]

    def reset(self) -> None:
        self.deck.reset()
        self.dealer.reset()
        for player in self.Player_list:
            player.reset()

    @staticmethod
    def clear_screen() -> None:
        """ clear a screen """
        os.system('clear')

    @property
    def min_bet(self):
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 5)

    def run(self) -> None:
        time = 0
        while len(self.now_player) > 1 or time == 0:
            time += 1
            printcolor(f'round{time}:')
            self.play()
            self.report_status()
            self.reset()
            printcolor('_____________________' * 2 + '\n')
        else:
            try:
                console.print(f'{self.now_player[0]} win', style='green')
            except IndexError:
                console.print('Dealer win', style='green')
            printcolor('_____________________' * 2 + '\n')
