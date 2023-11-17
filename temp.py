import pygame
import sys
import time
from level1 import level_matrix

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
gravity = 0.09
jump_strength = -6
jump_speed = 3
player_movement_speed = 1.8
is_facing_left = False

# Variables de dash
dash_cooldown = 0.1
dash_horizontal_duration = 0.28
dash_vertical_duration = 0.12
is_horizontal_dashing = False
is_vertical_dashing = False
dash_timer = 0
dash_horizontal_movement_speed = 8 # Vitesse du dash en direction horizontale
dash_vertical_movement_speed = 8    # Vitesse du dash en direction verticale
dash_horizontal_speed = 0
dash_vertical_speed = 0
remain_dashes = 1
image_remanente = pygame.image.load("imageremanente.png")
image_remanente_pos = [(player_x, player_y)]
is_image_remanente_facing_left = [False]
is_reset_dash_touched = False
timer_reset_dash = 0
reset_dash_respawn_time = 3

# Plateformes


platforms = []
pics = []
picsHaut = []
picsBas = []
picsGauche = []
picsDroite = []
resetDashs = []
platform_width = screen_width / len(level_matrix[0])
platform_height = screen_height / len(level_matrix)
imageResetDash = pygame.transform.scale((pygame.image.load("resetdash.png")), (platform_width,platform_height))
imageSpike = pygame.transform.scale((pygame.image.load("Spike.png")),(platform_width,platform_height))
imageSpikeVertical = pygame.image.load("SpikeVertical.png")
imageSpikeBas = pygame.transform.rotate(imageSpike, 180)
imageSpikeDroite = pygame.transform.rotate(imageSpike, -90)
imageSpikeGauche = pygame.transform.rotate(imageSpike, 90)
imageSpikeDroite = pygame.transform.scale(imageSpikeDroite,(platform_width,platform_height))
imageSpikeGauche = pygame.transform.scale(imageSpikeGauche,(platform_width,platform_height))

for row in range(len(level_matrix)):
    for col in range(len(level_matrix[row])):
        if level_matrix[row][col] == 1:
            platform = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
            platforms.append(platform)
        elif level_matrix[row][col] == 2:
            if level_matrix[row+1][col] == 1:
                picHaut = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
                picsHaut.append(picHaut)
            elif level_matrix[row-1][col] == 1:
                picBas = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
                picsBas.append(picBas)
            elif level_matrix[row][col-1] == 1:
                picDroite = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
                picsDroite.append(picDroite)
            elif level_matrix[row][col+1] == 1:
                picGauche = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
                picsGauche.append(picGauche)
            pic = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
            pics.append(pic)

        elif level_matrix[row][col] == 3:
            resetDash = pygame.Rect(col * platform_width, row * platform_height, platform_width, platform_height)
            resetDashs.append(resetDash)


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
    if not (is_vertical_dashing or is_horizontal_dashing):
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


# COLLISION PLATEFORMES
    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_y_speed > 0:
                if player_rect.top < platform.bottom and player_rect.bottom < platform.bottom:
                    player_y = platform.top - player_height
                    player_y_speed = 0
                    is_jumping = False
                    on_ground = True
                    if remain_dashes == 0:
                        remain_dashes += 1
            elif player_y_speed < 0:
                if player_rect.bottom > platform.top and player_rect.top > platform.top:
                    player_y = platform.bottom
                    player_y_speed = 0
            if player_x_speed < 0:
                # Ajout de la logique pour bloquer le personnage sur le côté de la plateforme
                if player_rect.left < platform.right and player_rect.right > platform.right and ((player_rect.bottom-5) > platform.top and (player_rect.bottom-5) < platform.bottom):
                    player_x = platform.right
                    player_x_speed = 0
            elif player_x_speed > 0:
                # Ajout de la logique pour bloquer le personnage sur le côté de la plateforme
                if player_rect.left < platform.left and player_rect.right > platform.left and ((player_rect.bottom-5) > platform.top and (player_rect.bottom-5) < platform.bottom):
                    player_x = platform.left - player_width
                    player_x_speed = 0


# COLLISION PICS
    for pic in pics:
        if player_rect.colliderect(pic):
            player_x = 50
            player_y = 50
            remain_dashes = 0
            is_jumping = True
            is_horizontal_dashing = False
            is_vertical_dashing = False
            player_x_speed = 0
            player_y_speed = 0

# COLLISION RESET DASH
    for resetdash in resetDashs:
        if player_rect.colliderect(resetdash) and current_time - timer_reset_dash >= reset_dash_respawn_time:
            remain_dashes = 1
            timer_reset_dash = current_time
    



# SAUT
    if keys[pygame.K_SPACE] and on_ground and current_time - last_jump_time >= jump_cooldown and not (is_vertical_dashing or is_horizontal_dashing) :
        player_y_speed = jump_strength
        player_x_speed *= jump_speed
        is_jumping = True
        last_jump_time = current_time
        
# DASH
    if is_horizontal_dashing or is_vertical_dashing:
        player_x_speed = dash_horizontal_speed
        player_y_speed = dash_vertical_speed
        if current_time - dash_timer >= (dash_horizontal_duration + dash_vertical_duration)/4 and len(image_remanente_pos) == 1:
            image_remanente_pos.append((player_x,player_y))
            is_image_remanente_facing_left.append(is_facing_left)
        if current_time - dash_timer >= dash_horizontal_duration:
            is_horizontal_dashing = False
        if current_time - dash_timer >= dash_vertical_duration:
            is_vertical_dashing = False

    elif keys[pygame.K_LSHIFT] and current_time - dash_timer >= dash_cooldown and remain_dashes > 0:
        image_remanente_pos.append((player_x, player_y))
        is_image_remanente_facing_left.append(is_facing_left)
        if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            is_vertical_dashing = True
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            is_horizontal_dashing = True
        elif not(keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            is_horizontal_dashing = True

        remain_dashes -= 1
        dash_timer = current_time
        if is_vertical_dashing and is_horizontal_dashing:
            if keys[pygame.K_UP]:
                dash_vertical_speed = -dash_vertical_movement_speed/1.7
            elif keys[pygame.K_DOWN]:
                dash_vertical_speed = dash_vertical_movement_speed/1.7
            else:
                dash_vertical_speed = 0
            if keys[pygame.K_LEFT]:
                dash_horizontal_speed = -dash_horizontal_movement_speed/1.7
            elif keys[pygame.K_RIGHT]:
                dash_horizontal_speed = dash_horizontal_movement_speed/1.7
            else:
                dash_horizontal_speed = 0
        else:
            if is_vertical_dashing:
                if keys[pygame.K_UP]:
                    dash_vertical_speed = -dash_vertical_movement_speed
                elif keys[pygame.K_DOWN]:
                    dash_vertical_speed = dash_vertical_movement_speed
            else:
                dash_vertical_speed = 0
            
            
            if is_horizontal_dashing:
                if keys[pygame.K_LEFT]:
                    dash_horizontal_speed = -dash_horizontal_movement_speed
                elif keys[pygame.K_RIGHT]:
                    dash_horizontal_speed = dash_horizontal_movement_speed
                
                elif not (keys[pygame.K_UP]) and not (keys[pygame.K_DOWN]):
                    if is_facing_left:
                        dash_horizontal_speed = -dash_horizontal_movement_speed
                    else:
                        dash_horizontal_speed = dash_horizontal_movement_speed
            else:
                dash_horizontal_speed = 0
        
    if not on_ground and not (is_vertical_dashing or is_horizontal_dashing):
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
        
    # Dessiner les pics
    for pic in picsHaut:
        screen.blit(imageSpike, pic)
    for pic in picsBas:
        screen.blit(imageSpikeBas, pic)
    for pic in picsDroite:
        screen.blit(imageSpikeDroite, pic)
    for pic in picsGauche:
        screen.blit(imageSpikeGauche, pic)
    #  Dessiner les reset dash

    # for resetdash in resetDashs:
    if current_time - timer_reset_dash >= reset_dash_respawn_time : 
        for i in resetDashs:
            screen.blit(imageResetDash, i)
       
        

    # Dessiner le personnage
    if remain_dashes == 0:
        player_image = pygame.image.load("dashsprite.png")
        for i in range(len(image_remanente_pos)):
            if is_image_remanente_facing_left[i]:
                image_remanente_flipped = pygame.transform.flip(image_remanente, True, False)
                screen.blit(image_remanente_flipped, image_remanente_pos[i])
            else:    
                screen.blit(image_remanente, image_remanente_pos[i])

    else:
        image_remanente_pos.clear()
        is_image_remanente_facing_left.clear()
        player_image = pygame.image.load("6.png")
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
