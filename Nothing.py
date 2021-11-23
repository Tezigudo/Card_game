# from Player.Player import PokDengPlayer
from Player.Hand import Screen
from Player.Player import BlackJackPlayer

s = Screen()
p = BlackJackPlayer('God')
# s.write_rainbow('Hello its me')
p.hand = ['Ace of Clubs', '3 of Clubs', 'King of Spades', '2 of Diamonds', 'King of Clubs']

p.show_hand()
