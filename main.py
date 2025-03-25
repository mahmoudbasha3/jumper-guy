# Example file showing a basic pygame "game loop"
import random
import pygame
from sys import exit

# pygame setup
pygame.init()

# Function to display the score
def score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    text_surface = test_font.render("Score: " + str(current_time), False, "Black")
    text_rect = text_surface.get_rect(center=sky_rect.center)
    screen.blit(text_surface, text_rect)
    return current_time

def player_walk_animate():
    global player_index, player_surf

    if player_rect.bottom < 215:
        player_surf = player_jump
    else:
        player_index +=0.1
        if player_index > 2:
            player_index = 0
        player_surf = player_walk_list[int(player_index)]


# Load font
test_font = pygame.font.Font("D:/GitHub/jumper-guy/graphics/Pixeltype.ttf", 50)

# Game variables
start_time = 0
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# Load images
sky_surface = pygame.image.load("D:/GitHub/jumper-guy/graphics/Sky.png").convert()
sky_rect = sky_surface.get_rect(topleft=(0, 0))

ground_surface = pygame.image.load("D:/GitHub/jumper-guy/graphics/ground.png").convert()

player_stand = pygame.image.load("D:/GitHub/jumper-guy/graphics/player_stand.png").convert_alpha()
player_walk_1 = pygame.image.load("D:/GitHub/jumper-guy/graphics/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("D:/GitHub/jumper-guy/graphics/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("D:/GitHub/jumper-guy/graphics/jump.png").convert_alpha()
player_walk_list = [player_walk_1,player_walk_2]
player_index = 0
player_surf = player_walk_list[player_index]
player_rect = player_surf.get_rect(midbottom=(200, 400))  # ✅ Player positioned 100 pixels higher


snail_surface1 = pygame.image.load("D:/GitHub/jumper-guy/graphics/snail1.png").convert_alpha()
snail_surface2 = pygame.image.load("D:/GitHub/jumper-guy/graphics/snail2.png").convert_alpha()
snail_frames = [snail_surface1,snail_surface2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_surface1 = pygame.image.load("D:/GitHub/jumper-guy/graphics/Fly1.png").convert_alpha()
fly_surface2 = pygame.image.load("D:/GitHub/jumper-guy/graphics/Fly2.png").convert_alpha()
fly_frames = [fly_surface1,fly_surface2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []  # Stores tuples (surface, rect)

gravity = 0
game_active = False
is_start_screen = True
my_score = 0


def obstacle_move():
    global game_active
    if obstacle_rect_list:
        updated_obstacles = []  # Temporary list to store updated obstacles

        for surface, rect in obstacle_rect_list:  # Iterate safely
            rect.x -= 4

            # Update surface for animation
            if surface in snail_frames:
                surface = snail_surf  # Use updated snail_surf
            elif surface in fly_frames:
                surface = fly_surf  # Use updated fly_surf

            # Draw the obstacle
            screen.blit(surface, rect)

            # Check for collision
            if rect.colliderect(player_rect):
                game_active = False
                obstacle_rect_list.clear()  # Clear obstacles immediately
                return  # Exit function immediately to stop further updates

            # If no collision and still on-screen, keep obstacle
            if rect.left > -74:
                updated_obstacles.append((surface, rect))

        obstacle_rect_list[:] = updated_obstacles  # ✅ Safely update the list


# Start screen function
def start_screen():
    screen.fill((192, 232, 236))
    player_rect_game_over = pygame.transform.scale2x(player_stand).get_rect(center=screen.get_rect().center)
    screen.blit(pygame.transform.scale2x(player_stand), player_rect_game_over)

    restart_text = test_font.render("To start, press any button", False, "Red")
    restart_text_rect = restart_text.get_rect(midtop=player_rect_game_over.midbottom)
    screen.blit(restart_text, restart_text_rect)

    title_text = test_font.render("Jumper Guy", False, (122, 154, 156))
    title_text_rect = title_text.get_rect(
        bottomright=(player_rect_game_over.midtop[0], player_rect_game_over.midtop[1] - 45))
    screen.blit(pygame.transform.scale2x(title_text), title_text_rect)

# Event timer for obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)

fly_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_timer, 400)

snail_timer = pygame.USEREVENT + 3
pygame.time.set_timer(snail_timer, 500)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Player Jump
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.y >= 215:
                    gravity = -25  # Jump force

            # Generate Obstacles
            if event.type == obstacle_timer:
                random_int = random.randint(1, 10)
                if random_int % 2 == 0:
                    obstacle_rect_list.append(
                        (snail_surf, snail_surf.get_rect(midbottom=(random.randint(900, 1100), 310))))
                else:
                    obstacle_rect_list.append((fly_surf, fly_surf.get_rect(
                        midbottom=(random.randint(900, 1100), 215))))  # Adjust fly height

            if event.type == snail_timer:
                if snail_index == 0: snail_index =1
                else: snail_index = 0
                snail_surf = snail_frames[snail_index]

            if event.type == fly_timer:
                if fly_index == 0: fly_index =1
                else: fly_index = 0
                fly_surf = fly_frames[fly_index]

        elif event.type == pygame.KEYDOWN and not game_active:
            # Restart Game
            game_active = True
            start_time = pygame.time.get_ticks()
            obstacle_rect_list.clear()
            player_rect.y = 215  # Reset player position higher
            gravity = 0

        if is_start_screen:
            start_screen()
            if event.type == pygame.KEYDOWN:
                is_start_screen = False
                start_time = pygame.time.get_ticks()

    if game_active and not is_start_screen:
        # Apply gravity
        gravity += 1
        player_rect.y += gravity

        # Prevent falling through the ground
        if player_rect.y >= 215:
            player_rect.y = 215
            gravity = 0

        # Draw elements
        screen.blit(sky_surface, sky_rect)
        screen.blit(ground_surface, (0, 300))
        player_walk_animate()
        screen.blit(player_surf, player_rect)

        obstacle_move()  # Move obstacles

        my_score = score()  # Display score

    elif not game_active and not is_start_screen:
        # Game Over Screen
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
        title_text_rect = title_text.get_rect(
            midbottom=(game_over_text_rect.midtop[0] - 90, game_over_text_rect.midtop[1] - 40))
        screen.blit(pygame.transform.scale2x(title_text), title_text_rect)

    pygame.display.update()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
