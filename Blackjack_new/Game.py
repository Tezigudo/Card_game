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
        if self.is_fail():
            return False
        return True


class Game:
    '''Entire game object'''
    def __init__(self, name_list: list[str]):
        self.Player_list = [Black_Jack_player(name) for name in name_list]
        # create an player list
        self.dealer = computer_player() # create an dealer player
        self.deck = Card()
        self.deal_card()

    def deal_card(self):
        '''deal card to all player'''
        for _ in range(2):
            for player in self.Player_list:
                player.draw(self.deck.deck)

    def show_every_player_card(self, show_len=False):
        '''show every player card unblineded and show the length of it if show_len'''
        for player in self.Player_list:
            player.show_unblined_card()
            if show_len:
                print(f'Have {len(player.hand)} Card')
            print()

    def Draw_all_player(self):
        '''Draw card to all payer'''
        self.show_every_player_card()
        self.dealer.show_unblined_card()
        print()

        for player in self.Player_list:
            print(f"{player}'s Turn:")
            is_continue = player.draw_one_turn(self)
            if not is_continue:
                print(f'{player} Drough')

    def finalize(self):
        for player in self.Player_list:
            player.finialize(win=player.if_win(self.dealer))
            


def main():
    '''main func'''
    money = float(input('Enter each player money: '))
    Black_Jack_player.set_player_money(money)
    g = Game(['God', 'Tw'])
    g.Draw_all_player()
    g.show_every_player_card(show_len=True)
    for x in g.Player_list:
        print(x, x.hand)


if __name__ == '__main__':
    main()
