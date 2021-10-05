import random
from Card import Card
from Player import Black_Jack_player
from time import sleep


class computer_player(Black_Jack_player):
    '''create an computer player for blck jack'''

    num = 0

    def __init__(self):
        super().__init__(self)
        computer_player.num += 1
        self.name = 'BOT'+str(computer_player.num)
        self.money = computer_player.initial_money

    def draw_one_turn(self, game):
        '''draw card untill computer hand values more than 17'''
        while self.val < 18:
            self.draw(game.deck.deck)
        if not self.check_if_hand_valid():
            return False
        return True


class Game:
    '''Entire game object'''
    def __init__(self, name_list: list[str]):
        self.Player_list = [Black_Jack_player(name) for name in name_list]
        # create an player list
        self.dealer = computer_player()  # create an dealer player
        self.deck = Card()
        self.deal_card()

    def deal_card(self):
        '''deal card to all player'''
        for _ in range(2):
            self.dealer.draw(self.deck.deck)
            for player in self.now_player:
                player.draw(self.deck.deck)

    def show_every_player_card(self, show_len=False):
        '''show every player card unblineded and show the length of it if show_len'''
        for player in self.now_player:
            player.show_unblined_card()
            if show_len:
                print(f'Have {len(player.hand)} Card')
            print()

    def Draw_all_player(self):
        '''Draw card to all payer'''
        self.show_every_player_card()
        self.dealer.show_unblined_card()
        print()

        for player in self.now_player:
            print(f"{player}'s Turn:")
            is_continue = player.draw_one_turn(self)
            if not is_continue:
                print(f'{player} Burst')

    def finalize(self):
        for player in self.now_player:
            player.finialize(win=player.if_win(self.dealer))

    def call_all(self):
        for player in self.now_player:
            player.call()

    def play(self):
        self.call_all()
        self.Draw_all_player()
        self.show_every_player_card(show_len=True)
        self.finalize()

    @property
    def now_player(self):
        return [player for player in self.Player_list if player.money > 0]


def main():
    '''main func'''
    money = float(input('Enter each player money: '))
    Black_Jack_player.set_player_money(money)
    g = Game(['God', 'Tw'])
    g.play()


if __name__ == '__main__':
    main()

'''
TODO: tomorrow I will fix the bug
-> input num
-> test if more than 21 and break then continue
TODO: finished the game part then fix any bug okey.
'''
