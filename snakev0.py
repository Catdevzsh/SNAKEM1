import numpy as np
import pygame
import pygame.sndarray
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# Game Settings
screen_width = 600
screen_height = 400
snake_block = 10
snake_speed = 15
font_style = pygame.font.SysFont(None, 35)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Initialize game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Sound generation function for stereo sound
def generate_beep(duration_ms, frequency):
    sample_rate = 44100
    samples = np.arange(duration_ms * (sample_rate / 1000.0))
    waveform = np.sin(2 * np.pi * frequency * samples / sample_rate)
    waveform = np.int16(waveform * 32767)  # Convert to 16-bit signed integers
    # Duplicate the waveform into 2 channels for stereo
    stereo_waveform = np.column_stack((waveform, waveform))
    sound = pygame.sndarray.make_sound(stereo_waveform)
    return sound

# Game Functions
def display_score(score):
    value = font_style.render(f"Score: {score}", True, white)
    screen.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, green, [x, y, snake_block, snake_block])

def game_loop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(black)
            message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, red)
            screen.blit(message, [screen_width / 6, screen_height / 3])
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            generate_beep(200, 440).play()  # Game over beep
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                generate_beep(200, 440).play()  # Game over beep
                game_close = True

        draw_snake(snake_block, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            generate_beep(100, 880).play()  # Eating food beep
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
