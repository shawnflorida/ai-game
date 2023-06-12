import turtle

from static import *
from utility import hide_sprite


class Treasure(turtle.Turtle):
    t_count = 0

    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.name = 'Treasure'
        self.shape('misc/gold.gif')
        self.gold = 10
        self.setposition(x, y)
        Treasure.t_count += 1

    def hide(self):
        hide_sprite(self)

    @staticmethod
    def return_t_count():
        return Treasure.t_count


class Box(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.name = 'Box'
        self.shape('misc/box.gif')
        self.color('#D4AF37')
        self.powerup = 3
        self.setposition(x, y)
        
    def hide(self):
        hide_sprite(self)


# classes
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color('#362020')
        self.penup()
        self.speed(0)
        self.name = 'Wall'
        self.hideturtle()


class Space(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.name = 'Space'
        self.hideturtle()
