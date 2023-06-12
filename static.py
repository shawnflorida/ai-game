import turtle


import pygame

pygame.mixer.init()

coin_sound = pygame.mixer.Sound("bgmusic/coin.mp3")
hurt_sound = pygame.mixer.Sound("audio/hurt.mp3")
win_sound = pygame.mixer.Sound("audio/win.mp3")
lose_sound = pygame.mixer.Sound("audio/lose.mp3")
heart_sound = pygame.mixer.Sound("audio/heart.mp3")
#teleport_sound = pygame.mixer.Sound("audio/teleport.mp3")

screen_space_coordinates = []
player_position_bidirectional_destination = ()
current_enemy_location = []


#It needs to have the current tuples of all enemies as the starting position that will be fitted into the function and the latest player position bidirectional is the
#is the final location that they need to find , whil only have the choices of the screen space coordinates as their neighboring nodes. 