__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.0'
__status__ = 'Finished'

import random


class Card:
    """ Card object"""

    def __init__(self) -> None:
        self.deck = self.create_deck()
        self.shuffle()

    @staticmethod
    def create_deck() -> list[str]:
        """this func create a deck using nested loop"""
        deck = []
        for suit in ('Clubs', 'Diamonds', 'Hearts', 'Spades'):
            for val in range(1, 14):
                match val:
                    case 1:
                        val = 'Ace'
                    case 11:
                        val = 'Jack'
                    case 12:
                        val = 'Queen'
                    case 13:
                        val = 'King'
                    case _:
                        pass
                deck.append(f'{val} of {suit}')
        return deck

    def shuffle(self) -> None:
        """shuffle a deck!"""
        random.shuffle(self.deck)

    def reset(self) -> None:
        """reset a deck"""
        self.deck = self.create_deck()
        self.shuffle()
