import pygame, sys
import os
mainClock = pygame.time.Clock()
from pygame.locals import *
from pygame import mixer
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cowboy vs Alien PVP")
screen = pygame.display.set_mode((900, 500),0,32)

font = pygame.font.SysFont(None, 80)
font2 = pygame.font.SysFont(None, 35)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 7
BULLET_VEL = 12
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
COWBOY_WIDTH, COWBOY_HEIGHT = 60, 45

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

COWBOY_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Cowboy.png'))
COWBOY = pygame.transform.rotate(pygame.transform.scale(
    COWBOY_IMAGE, (COWBOY_WIDTH, COWBOY_HEIGHT)), 0)

ALIEN_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
ALIEN = pygame.transform.rotate(pygame.transform.scale(
    ALIEN_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background-1.jpg')), (WIDTH, HEIGHT))

MENUBG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'menubg.jpg')), (WIDTH, HEIGHT))

HOWTOPLAYBG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'howtoplaybg.jpg')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, alien_health, cowboy_health):
    WIN.blit(SPACE, (0, 0))

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(alien_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(cowboy_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(COWBOY, (yellow.x, yellow.y))
    WIN.blit(ALIEN, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def cowboy_handle_movement(keys_pressed, cowboy):
    if keys_pressed[pygame.K_a] and cowboy.x - VEL > 0:  # LEFT
        cowboy.x -= VEL
    if keys_pressed[pygame.K_d] and cowboy.x + VEL + cowboy.width < BORDER.x:  # RIGHT
        cowboy.x += VEL
    if keys_pressed[pygame.K_w] and cowboy.y - VEL > 0:  # UP
        cowboy.y -= VEL
    if keys_pressed[pygame.K_s] and cowboy.y + VEL + cowboy.height < HEIGHT - 15:  # DOWN
        cowboy.y += VEL


def alien_handle_movement(keys_pressed, alien):
    if keys_pressed[pygame.K_LEFT] and alien.x - VEL > BORDER.x + BORDER.width:  # LEFT
        alien.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and alien.x + VEL + alien.width < WIDTH:  # RIGHT
        alien.x += VEL
    if keys_pressed[pygame.K_UP] and alien.y - VEL > 0:  # UP
        alien.y -= VEL
    if keys_pressed[pygame.K_DOWN] and alien.y + VEL + alien.height < HEIGHT - 15:  # DOWN
        alien.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def game():

    mixer.init()
    mixer.music.load('Assets/battlebgm.mp3')
    mixer.music.play(-1)

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, COWBOY_WIDTH, COWBOY_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    alien_health = 10
    cowboy_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                alien_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                cowboy_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if alien_health <= 0:
            mixer.init()
            mixer.music.load('Assets/victory.mp3')
            mixer.music.play(-1)
            winner_text = "Cowboy Wins!"

        if cowboy_health <= 0:
            mixer.init()
            mixer.music.load('Assets/victory.mp3')
            mixer.music.play(-1)
            winner_text = "Alien Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        cowboy_handle_movement(keys_pressed, yellow)
        alien_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    alien_health, cowboy_health)
    game()

click = False

def main_menu():

    mixer.init()
    mixer.music.load('Assets/menubgm.mp3')
    mixer.music.play(-1)

    while True:

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(335, 215, 225, 50)
        button_2 = pygame.Rect(285, 320, 325, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                how()
        pygame.draw.rect(screen, (255, 255, 255), button_1)
        pygame.draw.rect(screen, (255, 255, 255), button_2)

        WIN.blit(MENUBG, (0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def how():
    running = True
    while running:

        WIN.blit(HOWTOPLAYBG, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

main_menu()
