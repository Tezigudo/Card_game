from time import sleep
import turtle
from math import ceil


class Screen:
    def __init__(self) -> None:
        """ Initialize"""
        # screen
        self.screen = turtle.Screen()
        self.screen.bgcolor('green')
        self.screen.screensize(600, 420)
        # painter
        self.painter = turtle.Turtle()
        self.painter.hideturtle()
        self.painter.penup()
        # title
        turtle.title('Card game Graphic')

    def show_hand(self, player) -> None:
        """show a graphic hand

        Parameters
        ----------
        player : Player object
            Player object whether is PokDengPlayer or BlackJackPlayer
        """
        self.painter.penup()
        self.painter.goto(-300, 260)  # goto top left
        self.painter.pencolor('cyan')
        # show a player name graphic
        self.painter.write(player.name, True, align="left", font=("Menlo", 28, "bold"))
        self.painter.pencolor('white')
        self.painter.write(" Turn", True, align="left", font=("Menlo", 28, "bold"))
        self.painter.goto(-300, 230)  # go to below name
        self.painter.write("Value = ", True, align="left", font=("Menlo", 20, "bold"))
        self.painter.pencolor('cyan')
        # show player value graphic
        self.painter.write(player.value, True, align="left", font=("Menlo", 20, "bold"))

        hands = []
        x, y = -50*ceil(len(player.hand)/2+1), -60  # card must be on a middle of screen
        for card in player.hand:
            val, suit = card.split(' of ')
            # create turtle object that illustrated each card of player
            turtle_card = turtle.Turtle()
            turtle_card.hideturtle()  # hide turtle
            turtle_card.penup()
            turtle_card.goto(x, y)  # make turtle go to each card position
            shape = f'Card_pic/{val if val.isdigit() else val[0]}{suit[0]}.gif'
            # add shape to each turtle to be that card curren value
            self.screen.addshape(shape)
            turtle_card.shape(shape)
            hands.append(turtle_card)
            x += 100  # increment x position for next card
        for each_turtle_card in hands:
            # show a card in each position
            each_turtle_card.showturtle()
        print('Look at your Screen(canvas)')
        sleep(2.5)  # make an delay to make sure that user see a card from screen graphic
        self.reset()  # reset screen to green bg after finished each turn

    def reset(self) -> None:
        """reset screen
        """
        self.screen.clearscreen()
        self.screen.bgcolor('green')

    def write_rainbow(self, text: str) -> None:
        """write rainbow text graphic on a screen

        Parameters
        ----------
        text : str
            text that user want to write on a screen(rainbow color)
        """
        color = ['purple', 'indigo', 'blue', 'cyan', 'yellow', 'orange', 'red']
        now = 0
        for alp in text:  # iterate over each alphabet in text
            # if alphabet be a space or whitespace character will set color to be green
            if alp == ' ':
                self.painter.pencolor('green')
            else:
                self.painter.pencolor(color[now % 7])
                now += 1  #increment a now color index
            # write a text
            self.painter.write(alp, True, align="left", font=("Menlo", 40, "bold"))
