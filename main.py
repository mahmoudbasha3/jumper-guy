# Example file showing a basic pygame "game loop"
from typing import Tuple

import random
import pygame
from sys import exit

# pygame setup
pygame.init()

# a function to display the score
def score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    text_surface = test_font.render("score: " + str(current_time), False, "Black")
    text_rect = text_surface.get_rect(center=sky_rect.center)
    screen.blit(text_surface, text_rect)
    return current_time


test_font = pygame.font.Font("D:/Ericsson data scientist role/SWE skills/python_projects/graphics/Pixeltype.ttf",
                                 50)
start_time = 0
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

sky_surface = pygame.image.load("D:/Ericsson data scientist role/SWE skills/python_projects/graphics/Sky.png").convert()
sky_rect = sky_surface.get_rect(topleft=(0,0))

ground_surface = pygame.image.load("D:/Ericsson data scientist role/SWE skills/python_projects/graphics/ground.png").convert()

player_surf = pygame.image.load("D:/Ericsson data scientist role/SWE skills/python_projects/graphics/player_stand.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(200,310))

snail_surface = pygame.image.load("D:/Ericsson data scientist role/SWE skills/python_projects/graphics/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(800,310))
obstacle_rect_list = []

gravity = 0
game_active = False
is_start_screen = True
my_score = 0

def obstacle_move():
    if obstacle_rect_list:
        for obstacle in obstacle_rect_list:
            obstacle.x -= 3
            screen.blit(snail_surface,obstacle)
            # if obstacle.left <= -74:
            #     obstacle_rect_list.remove(obstacle)

def start_screen():
    screen.fill((192, 232, 236))
    player_rect_game_over = pygame.transform.scale2x(player_surf).get_rect(center=screen.get_rect().center)
    screen.blit(pygame.transform.scale2x(player_surf), player_rect_game_over)
    # text stuff

    restart_text = test_font.render("To start press any button on keyboard", False, "Red")
    restart_text_rect = restart_text.get_rect(midtop=player_rect_game_over.midbottom)
    screen.blit(restart_text, restart_text_rect)

    title_text = test_font.render("Jumper Guy", False, (122, 154, 156))
    title_text_rect = title_text.get_rect(
        bottomright=((player_rect_game_over.midtop[0],player_rect_game_over.midtop[1]-45)))
    screen.blit(pygame.transform.scale2x(title_text), title_text_rect)

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,400)

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.y>=250:
                    gravity = -25
                    player_rect.y += gravity
        elif event.type == pygame.KEYDOWN and game_active == False:
            game_active = True
            start_time = pygame.time.get_ticks()
        if is_start_screen :
            start_screen()
            if event.type == pygame.KEYDOWN:
                is_start_screen = False
                start_time = pygame.time.get_ticks()
        if event.type==obstacle_timer and game_active:
            obstacle_rect_list.append(snail_surface.get_rect(midbottom=(random.randint(900,1100),310)))


    if game_active and not is_start_screen:

        obstacle_move()

        if player_rect.y < 250:
            gravity +=1
            player_rect.y += gravity

        screen.blit(sky_surface,sky_rect)
        screen.blit(ground_surface, (0, 300))

        screen.blit(player_surf, player_rect)

        # screen.blit(snail_surface, snail_rect)
        # snail_rect.left-=4
        # pygame.draw.line(screen,"Green",screen.get_rect().topleft,screen.get_rect().bottomright)

        #puts the moving snail back to the right of the screen
        # if snail_rect.left <= -74:
        #     snail_rect.left = 800

        if snail_rect.colliderect(player_rect):
            game_active = False
            snail_rect.left = 800
            game_is_over = True
        my_score = score()
    elif not game_active and not is_start_screen:

        # screen for game over
        # player image stuff
        screen.fill((192,232,236))
        player_rect_game_over = pygame.transform.scale2x(player_surf).get_rect(center=screen.get_rect().center)
        screen.blit(pygame.transform.scale2x(player_surf), player_rect_game_over)
        #text stuff
        game_over_text = test_font.render("Game Over", False, "Red")
        game_over_text_rect = game_over_text.get_rect(midbottom=player_rect_game_over.midtop)
        screen.blit(game_over_text, game_over_text_rect)

        restart_text = test_font.render("To restart press any button on keyboard", False, "Red")
        restart_text_rect = restart_text.get_rect(midtop=player_rect_game_over.midbottom)
        screen.blit(restart_text, restart_text_rect)

        score_text = test_font.render("your score is "+str(my_score), False, (122, 154, 156))
        score_text_rect = score_text.get_rect(midtop=restart_text_rect.midbottom)
        screen.blit(score_text, score_text_rect)

        title_text = test_font.render("Jumper Guy", False, (122, 154, 156))
        title_text_rect = title_text.get_rect(midbottom=(game_over_text_rect.midtop[0]-90,game_over_text_rect.midtop[1]-40))
        screen.blit(pygame.transform.scale2x(title_text), title_text_rect)


    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()