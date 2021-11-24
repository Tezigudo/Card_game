__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.0'
__status__ = 'working'

import os
import sys
from time import sleep
# append back path to the current path
sys.path.insert(1, '/'.join(sys.path[0].split('/')[:-1]))
from rich import print as printcolor
from rich.console import Console

from Deck.Card import Card
from Player.Player import Player
from database import Save

console = Console()


class BaseGame:
    def __init__(self, name_list: list[str]) -> None:
        """Initialize a game

        Parameters
        ----------
        name_list : list[str]
            list of player name
        """
        self.Player_list = [Player(name) for name in name_list]
        # create an player list
        self.deck = Card()
        self.save = Save()

    def report_status(self) -> None:
        """report a current game status
        """
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
            # dealer draw
            self.dealer.draw(self.deck.deck)
            # player draw
            for player in self.now_player:
                player.draw(self.deck.deck)

    def show_every_player_card(self) -> None:
        """show every player card in game
        """
        # iterate each player in now player
        for player in self.now_player:
            console.print(f'{player}:', style='bold cyan')
            print(f'{player} hand are: {player.hand} ')
            console.print(f'value: {player.value}')
            print()

    def set_played(self) -> None:
        """set status for player
        whether have money to play in each turn
        """
        for player in self.Player_list:
            player.played = player.money > 0

    @property
    def now_player(self) -> list[Player]:
        """return an player which not knock(money>=0)"""
        return [player for player in self.Player_list if player.played]

    def reset(self) -> None:
        """reset a entire game
        """
        self.deck.reset()
        self.dealer.reset()
        for player in self.Player_list:
            player.reset()

    @staticmethod
    def clear_screen() -> None:
        """clear a screen """
        os.system('clear')

    @property
    def min_bet(self) -> int:
        """return a minbet of each player for each player in game

        Returns
        -------
        int
            min bet of each player
        """
        return round(sum(player.money for player in self.Player_list) / len(self.Player_list) / 5)

    def run(self) -> None:
        """run an entire game and count what round is it
        """
        times = 0
        while len(self.now_player) > 1 or times == 0:
            times += 1
            printcolor(f'round{time}:')
            self.play()
            self.report_status()
            self.reset()
            printcolor('_____________________' * 2 + '\n')
