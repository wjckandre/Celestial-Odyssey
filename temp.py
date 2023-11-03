import pygame
import sys
import time


class Plateforme:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        # Vous pouvez ajouter d'autres propriétés spécifiques ici


# Initialisation de Pygame
pygame.init()

# Configuration de l'écran
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Celeste Clone")

# Couleurs
WHITE = (255, 255, 255)

# Joueur
player_image = pygame.image.load("6.png") 
player_width = 60
player_height = 83
player_x = 50
player_y = 50
player_x_speed = 0
player_y_speed = 0
gravity = 0.05
jump_strength = -4
jump_speed = 3
player_movement_speed = 1.2
is_facing_left = False

# Variables de dash
dash_cooldown = 0.5
dash_duration = 0.15
is_dashing = False
dash_timer = 0
dash_horizontal_movement_speed = 6 # Vitesse du dash en direction horizontale
dash_vertical_movement_speed = 6    # Vitesse du dash en direction verticale
dash_horizontal_speed = 0
dash_vertical_speed = 0
remain_dashes = 1

# Plateformes
level_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
platforms = []
platform_width = screen_width / len(level_matrix[0])
platform_height = screen_height / len(level_matrix)

for row in range(len(level_matrix)):
    for col in range(len(level_matrix[row])):
        if level_matrix[row][col] == 1:
            platform = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
            platforms.append(platform)


# Ajouter une plateforme fictive au bas de l'écran
ground = pygame.Rect(0, screen_height - 10, screen_width, 10)
platforms.append(ground)

# Variables de saut
is_jumping = False
last_jump_time = 0
jump_cooldown = 0.2  # Cooldown de 0.2 secondes entre les sauts

# Boucle de jeu
running = True
while running:
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not is_dashing:
        if keys[pygame.K_LEFT] :
            player_x_speed = -player_movement_speed
            is_facing_left = True
        elif keys[pygame.K_RIGHT]:
            player_x_speed = player_movement_speed
            is_facing_left = False
        else:
            player_x_speed = 0

    # Gravité
    on_ground = False
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_y_speed > 0:
                if player_rect.top < platform.bottom:
                    player_y = platform.top - player_height
                    player_y_speed = 0
                    is_jumping = False
                    if remain_dashes == 0 : remain_dashes += 1
                    on_ground = True
            elif player_y_speed < 0:
                if player_rect.bottom > platform.top:
                    player_y = platform.bottom
                    player_y_speed = 0

    if keys[pygame.K_SPACE] and on_ground and current_time - last_jump_time >= jump_cooldown and not is_dashing :
        player_y_speed = jump_strength
        player_x_speed *= jump_speed
        is_jumping = True
        last_jump_time = current_time
        

    if is_dashing:
        player_x_speed = dash_horizontal_speed
        player_y_speed = dash_vertical_speed
        if current_time - dash_timer >= dash_duration:
            is_dashing = False

    elif keys[pygame.K_LSHIFT] and current_time - dash_timer >= dash_cooldown and not is_dashing and remain_dashes > 0:
        remain_dashes -= 1
        is_dashing = True
        dash_timer = current_time
        if keys[pygame.K_LEFT]:
            dash_horizontal_speed = -dash_horizontal_movement_speed
        elif keys[pygame.K_RIGHT]:
            dash_horizontal_speed = dash_horizontal_movement_speed
        else:
            dash_horizontal_speed = 0

        if keys[pygame.K_UP]:
            dash_vertical_speed = -dash_vertical_movement_speed
        elif keys[pygame.K_DOWN]:
            dash_vertical_speed = dash_vertical_movement_speed
        else:
            dash_vertical_speed = 0
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if is_facing_left:
                dash_horizontal_speed = -dash_horizontal_movement_speed
            else:
                dash_horizontal_speed = dash_horizontal_movement_speed

    if not on_ground and not is_dashing:
        player_y_speed += gravity

    player_x += player_x_speed
    player_y += player_y_speed

    # Limite de l'écran
    if player_x < 0:
        player_x = 0
    if player_x > screen_width - player_width:
        player_x = screen_width - player_width
    if player_y > screen_height - player_height:
        player_y = screen_height - player_height
        player_y_speed = 0
        is_jumping = False

    if keys[pygame.K_0]:
        player_x = 50
        player_y = 50
    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner les plateformes
    for platform in platforms:
        pygame.draw.rect(screen, (0, 0, 255), platform)


    if is_facing_left:
        player_image_flipped = pygame.transform.flip(player_image, True, False)
        screen.blit(player_image_flipped, (player_x, player_y))
    else:
        screen.blit(player_image, (player_x, player_y))

    print(remain_dashes)

    pygame.display.update()

# Quitter Pygame
pygame.quit()
sys.exit()
