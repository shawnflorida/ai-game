import time
import pygame
import sys

from maze import start_game

# Set the screen dimensions
screen_width = 1000  # Replace with the actual width of your screen
screen_height = 500  # Replace with the actual height of your screen

# Setup pygame/window
pygame.init()
pygame.display.set_caption('Speedscapes: Portal Jump')
screen = pygame.display.set_mode((screen_width, screen_height) )

# Load and resize the background image
background = pygame.image.load("pics/main_bg.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load button imagesx
start_button_img = pygame.image.load("pics/start.png").convert_alpha()
quit_button_img = pygame.image.load("pics/quit.png").convert_alpha()

font = pygame.font.SysFont(None, 20)
# Load and play the audio file
pygame.mixer.music.load("audio/main_audio.mp3")
pygame.mixer.music.play(-1, start=8)
# Set the initial volume (0.5 is half of the maximum volume)
pygame.mixer.music.set_volume(0.4)


# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    while True:
        screen.blit(background, (0, 0))  # Blit the background image onto the screen
        mx, my = pygame.mouse.get_pos()

        button_width = 160
        button_height = 58
        button_x1 = (screen_width - button_width) // 2 - 130
        button_x2 = (screen_width - button_width) // 2 + 100
        button_y = screen_height - 100

        button_1 = pygame.Rect(button_x1, button_y, button_width, button_height)
        button_2 = pygame.Rect(button_x2, button_y, button_width, button_height)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
                pygame.quit()
                sys.exit()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        # Resize button images
        start_button_img_resized = pygame.transform.scale(start_button_img, (button_width, button_height))
        quit_button_img_resized = pygame.transform.scale(quit_button_img, (button_width, button_height))

        screen.blit(start_button_img_resized, (button_x1, button_y))
        screen.blit(quit_button_img_resized, (button_x2, button_y))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def game():
    pygame.quit()
    running = True
    while running:
        running = False
                
        pygame.mixer.init()
        pygame.mixer.music.load('bgmusic/main.mp3')
        pygame.mixer.music.play(-1)
        start_game(1)
        pygame.display.update()
        click = True
    sys.exit()

       


def quit():
    running = False
    while running:
        screen.fill((0, 0, 0))

        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.update()
main_menu()


