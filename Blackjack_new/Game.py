import random
from Card import Card
from Player import Black_Jack_player
from time import sleep


class computer_player(Black_Jack_player):

    num = 0

    def __init__(self):
        super().__init__(self)
        computer_player.num += 1
        self.name = 'BOT'+str(computer_player.num)
        self.money = computer_player.initial_money

    def draw_one_turn(self, game):
        while self.val < 18:
            self.draw(game.deck.deck)
        if self.is_fail():
            return False
        return True


class Game:
    def __init__(self, name_list: list[str]):
        self.Player_list = [Black_Jack_player(name) for name in name_list]
        self.dealer = computer_player()
        self.deck = Card()
        self.deal_card()

    def deal_card(self):
        for _ in range(2):
            for player in self.Player_list:
                player.draw(self.deck.deck)

    def show_every_player_card(self, show_len=False):
        for player in self.Player_list:
            player.show_unblined_card()
            if show_len:
                print(f'Have {len(player.hand)} Card')
            print()

    def Draw_all_player(self):
        self.show_every_player_card()

        for player in self.Player_list:
            print(f"{player}'s Turn:")
            is_continue = player.draw_one_turn(self)
            if not is_continue:
                print(f'{player} Drough')


def main():
    money = float(input('Enter each player money: '))
    Black_Jack_player.set_player_money(money)
    g = Game(['God', 'Tw'])
    g.Draw_all_player()
    g.show_every_player_card(show_len=True)
    for x in g.Player_list:
        print(x, x.hand)


if __name__ == '__main__':
    main()
