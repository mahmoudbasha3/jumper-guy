# Jumper Guy Game with Collision Detection
import random
import pygame
from sys import exit
from random import randint, choice

# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('D:/GitHub/jumper-guy/graphics/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('D:/GitHub/jumper-guy/graphics/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('D:/GitHub/jumper-guy/graphics/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('D:/GitHub/jumper-guy/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# --- Obstacle Class ---
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('D:/GitHub/jumper-guy/graphics/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('D:/GitHub/jumper-guy/graphics/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('D:/GitHub/jumper-guy/graphics/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('D:/GitHub/jumper-guy/graphics/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# --- Collision Function ---
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# --- Setup ---
pygame.init()

game_over_sound = pygame.mixer.Sound('D:/GitHub/jumper-guy/audio/game_over.mp3')
game_over_sound.set_volume(0.5)

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Jumper Guy")
clock = pygame.time.Clock()
test_font = pygame.font.Font("D:/GitHub/jumper-guy/graphics/Pixeltype.ttf", 50)

# Music
bg_music = pygame.mixer.Sound('D:/GitHub/jumper-guy/audio/music.mp3')
bg_music.play(loops=-1)

# Background
sky_surface = pygame.image.load("D:/GitHub/jumper-guy/graphics/Sky.png").convert()
sky_rect = sky_surface.get_rect(topleft=(0, 0))
ground_surface = pygame.image.load("D:/GitHub/jumper-guy/graphics/ground.png").convert()

# Start screen image
player_stand = pygame.image.load("D:/GitHub/jumper-guy/graphics/player_stand.png").convert_alpha()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Game variables
start_time = 0
my_score = 0
game_active = False
is_start_screen = True

# Obstacle spawn timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


# --- Score Function ---
def score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    text_surface = test_font.render(f"Score: {current_time}", False, "Black")
    text_rect = text_surface.get_rect(center=sky_rect.center)
    screen.blit(text_surface, text_rect)
    return current_time


# --- Start Screen Function ---
def start_screen():
    screen.fill((192, 232, 236))
    player_rect_game_over = pygame.transform.scale2x(player_stand).get_rect(center=screen.get_rect().center)
    screen.blit(pygame.transform.scale2x(player_stand), player_rect_game_over)

    restart_text = test_font.render("To start, press any button", False, "Red")
    restart_text_rect = restart_text.get_rect(midtop=player_rect_game_over.midbottom)
    screen.blit(restart_text, restart_text_rect)

    title_text = test_font.render("Jumper Guy", False, (122, 154, 156))
    title_text_rect = title_text.get_rect(midbottom=player_rect_game_over.midtop)
    screen.blit(title_text, title_text_rect)


# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        elif event.type == pygame.KEYDOWN and not game_active:
            game_active = True
            start_time = pygame.time.get_ticks()
            obstacle_group.empty()
            player.sprite.rect.midbottom = (80, 300)
            player.sprite.gravity = 0

        if is_start_screen:
            start_screen()
            if event.type == pygame.KEYDOWN:
                is_start_screen = False
                start_time = pygame.time.get_ticks()

    if game_active and not is_start_screen:
        screen.blit(sky_surface, sky_rect)
        screen.blit(ground_surface, (0, 300))

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()  # <-- Collision detection here!

        my_score = score()

    elif not game_active and not is_start_screen:
        # Stop background music
        bg_music.stop()

        # Play game over sound
        game_over_sound.play()

        screen.fill((192, 232, 236))
        player_rect_game_over = pygame.transform.scale2x(player_stand).get_rect(center=screen.get_rect().center)
        screen.blit(pygame.transform.scale2x(player_stand), player_rect_game_over)

        game_over_text = test_font.render("Game Over", False, "Red")
        game_over_text_rect = game_over_text.get_rect(midbottom=player_rect_game_over.midtop)
        screen.blit(game_over_text, game_over_text_rect)

        restart_text = test_font.render("Press any key to restart", False, "Red")
        restart_text_rect = restart_text.get_rect(midtop=player_rect_game_over.midbottom)
        screen.blit(restart_text, restart_text_rect)

        score_text = test_font.render(f"Your score: {my_score}", False, (122, 154, 156))
        score_text_rect = score_text.get_rect(midtop=restart_text_rect.midbottom)
        screen.blit(score_text, score_text_rect)

        title_text = test_font.render("Jumper Guy", False, (122, 154, 156))
        title_text_rect = title_text.get_rect(midbottom=game_over_text_rect.midtop)  # Center the text
        screen.blit(title_text, title_text_rect)

    pygame.display.update()
    clock.tick(60)

