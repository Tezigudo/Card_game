
class Player:

    initial_money = 0

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.money = Player.initial_money
        self.had_bet = 0

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def draw(self, deck):
        self.hand.append(deck.pop())

    @property
    def value(self):
        return self.calculate_val()

    @value.setter
    def calculate_val(self):
        s = 0
        for card in self.hand:
            val = card.split()[0]
            if val == 'Ace':
                s += 1
            elif val in ('King', 'Queen', 'Jack', 'King'):
                s += 10
            else:
                s += int(val)
        return s

    @classmethod
    def set_player_money(cls, money):
        cls.initial_money = money

    def show_hand(self):
        print(f'{self.name} had {self.hand}')
        print(f'value = {self.value}')
