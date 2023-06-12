import functools
import os
import random
import time
import turtle
from collections import deque
from  static import *

def hide_sprite(sprite):
    sprite.setposition(2000, 2000)
    sprite.hideturtle()


def set_direction():
    return random.choice(['up', 'down', 'left', 'right'])


cwd = os.getcwd()


def distance_manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return dx + dy


def trigger_assign_gif(screen):
    # iterate over the files in the enemy directory and register them
    list_folder = ['enemy/level1',
                   'enemy/level2',
                   'enemy/level3',
                   'player',
                   'misc',
                   'walls/level1',
                   'walls/level2',
                   'walls/level3',
                   'walls'
                   ]

    for folder in list_folder:
        for filename in os.listdir(os.path.join(cwd, folder)):
            if filename.endswith('.gif'):
                name = filename.split('.')[0]
                screen.register_shape(f"{folder}/{filename}")


def trigger_floor_gif(game_level, screen_width, screen_height):
    blocks_turtle = turtle.Turtle()
    blocks_turtle.speed(0)
    blocks_turtle.hideturtle()

    # Set the jungle.gif image as the turtle shape
    
    for i in range(-screen_width // 2, screen_width // 2, 25):
        for j in range(-screen_height // 2, screen_height // 2, 25):
            blocks_turtle.shape(f"walls/level{game_level}/tile.gif")

            blocks_turtle.penup()
            blocks_turtle.goto(i, j)
            blocks_turtle.stamp()


def start_enemies_moving(t, enemies, wn, player):
    for enemy_sprite in enemies:
        enemy_sprite.bidirectional_search(player)

        wn.ontimer(functools.partial(enemy_sprite.change_direction), t=t)

    wn.update()
    




def player_move(player, wn):
    wn.listen()
    wn.onkeypress(player.move_up, "Up")
    wn.onkeypress(player.move_down, "Down")
    wn.onkeypress(player.move_left, "Left")
    wn.onkeypress(player.move_right, "Right")
    wn.onkeypress(player.teleport, " ")
    wn.onkeypress(player.switch_teleport, "x")

