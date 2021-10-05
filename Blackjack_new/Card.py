import random


class Card:
    ''' Card object'''
    def __init__(self):
        self.deck = self.create_deck()
        self.shuffle()

    def create_deck(self) -> list[str]:
        '''this func create a deck using nested loop'''
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

    def shuffle(self):
        '''shuffle a deck!'''
        random.shuffle(self.deck)

    def reset(self):
        '''reset a deck'''
        self.deck = self.create_deck()
