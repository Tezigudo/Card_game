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

    def show_hand(self, player):
        self.painter.penup()
        self.painter.goto(-300, 260)
        self.painter.pencolor('cyan')
        self.painter.write(player.name, True, align="left", font=("Menlo", 28, "bold"))
        self.painter.pencolor('white')
        self.painter.write(" Turn", True, align="left", font=("Menlo", 28, "bold"))
        self.painter.goto(-300, 230)
        self.painter.write("Value = ", True, align="left", font=("Menlo", 20, "bold"))
        self.painter.pencolor('cyan')
        self.painter.write(player.value, True, align="left", font=("Menlo", 20, "bold"))

        hands = []
        x, y = -50*ceil(len(player.hand)/2+1), -60
        for card in player.hand:
            val, suit = card.split(' of ')
            turtle_card = turtle.Turtle()
            turtle_card.hideturtle()
            turtle_card.penup()
            turtle_card.goto(x, y)
            shape = f'Card_pic/{val if val.isdigit() else val[0]}{suit[0]}.gif'
            self.screen.addshape(shape)
            turtle_card.shape(shape)
            hands.append(turtle_card)
            x += 100
        for each_turtle_card in hands:
            each_turtle_card.showturtle()
        print('Look at your Screen(canvas)')
        sleep(3)
        self.reset()

    def reset(self):
        self.screen.clearscreen()
        self.screen.bgcolor('green')

    def write_rainbow(self, text):
        color = ['purple', 'indigo', 'blue', 'cyan', 'yellow', 'orange', 'red']
        now = 0
        for alp in text:
            if alp == ' ':
                self.painter.pencolor('green')
            else:
                self.painter.pencolor(color[now % 7])
                now += 1

            self.painter.write(alp, True, align="left", font=("Menlo", 40, "bold"))
