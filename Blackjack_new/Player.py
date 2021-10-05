class Player:
    '''define a Player object using through all card game'''

    initial_money = 0

    def __init__(self, name):
        '''initialize
        hand: player's hand
        money: player's money
        had_bet: player's bet
        '''
        self.name = name
        self.hand = []
        self.money = Player.initial_money
        self.had_bet = 0

    def __str__(self):
        '''represent Player's name when print player object'''
        return self.name

    def __repr__(self):
        '''represent class name and object name'''
        return f'Player -> {self.name}'

    @property
    def value(self):
        '''return value from calculated value '''
        return self.calculate_val

    @value.getter
    def calculate_val(self):
        '''calculate value'''
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
        '''set all player money when'''
        cls.initial_money = money

    def draw(self, deck, more=False):
        '''print what card that draw if more is True else not print'''
        tmp = deck.pop()
        self.hand.append(tmp)
        if more:
            print(f'{self} has Draw {tmp}')

    def show_hand(self):
        '''Show hand of player '''
        print(f'{self.name} had {self.hand}')
        print(f'value = {self.value}')

    def bet(self, money):
        '''bet'''
        self.had_bet = money

    def finialize(self, win=False):
        '''add bet money o player if win else minus if draw do nothing
        then reset the bet money'''

        if win != 'Draw':
            if win:
                print(f'{self} win and got {self.had_bet}')
                self.money += self.had_bet
            else:
                print(f'{self} lose and lost {self.had_bet}')
                self.money -= self.had_bet
        else:
            print(f'{self} Draw')
        print(f'{self} have {self.money} left.')
        self.had_bet = 0

    def if_win(self, dealer):
        '''check whether player value more that dealer value'''
        if self.value == dealer.value:
            return 'Draw'
        else:
            return self.value > dealer.value

    def call(self):
        print(f'{self} amount is: {self.money}')
        try:
            amount = float(input('Please enter amount to bet: '))
        except ValueError:
            print('Invalid input')
            self.call()
        if amount > self.money:
            print('you not have enough amount please try again')
            self.call()
        else:
            self.bet(amount)
            print(f'{self} have bet: {amount}')
            print(f'{self} have {self.money} left.')


class Black_Jack_player(Player):
    '''create a black jack object that inherit from player'''
    def __init__(self, name):
        super().__init__(name)
        self.money = Black_Jack_player.initial_money

    @property
    def value(self):
        '''return player value'''
        return self.calculate_val

    @value.getter
    def calculate_val(self):
        '''calculate value for player and return in'''
        s = ace_count = 0
        for card in self.hand:
            val = card.split()[0]
            if val == 'Ace':
                ace_count += 1
            elif val in ('King', 'Queen', 'Jack', 'King'):
                s += 10
            else:
                s += int(val)

        while ace_count:
            if s + 11 <= 23:
                s += 11
            else:
                s += 1
            ace_count -= 1

        return s

    def show_unblined_card(self):
        '''show unblinded card'''
        print(f'{self}:')
        print(f'unblind is: {self.hand[0]}')

    def check_if_hand_valid(self):
        '''check whether player value less than 21'''
        return self.value < 22

    def blackjack(self):
        return self.value == 21

    def draw_one_turn(self, game):
        '''draw one turn for black jack'''
        self.show_hand()
        while self.value <= 21:
            if not self.check_if_hand_valid():
                break
            ans = input('Want to draw? (Y/N): ')
            if ans.upper() == 'Y':
                self.draw(game.deck.deck, more=True)
            elif ans.upper() == 'N':
                break
            else:
                print('Invalid Input please try again')
            self.show_hand()
        if self.blackjack():
            print('black jack')
            return True
        if not self.check_if_hand_valid():
            return False
        return True
