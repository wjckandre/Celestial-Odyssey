import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de l'écran
largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Plateforme")

# Couleurs
blanc = (255, 255, 255)
bleu = (0, 0, 255)

# Personnage
personnage = pygame.Rect(50, 500, 40, 40)
personnage_vitesse = 1
saut = False
saut_compteur = 400


# Plateformes
plateformes = [pygame.Rect(100, 300, 200, 10),
              pygame.Rect(400, 450, 200, 10),
              pygame.Rect(200, 200, 200, 10)]

# Boucle de jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        personnage.x -= personnage_vitesse
    if touches[pygame.K_RIGHT]:
        personnage.x += personnage_vitesse

    if not saut:
        if touches[pygame.K_SPACE]:
            saut = True
            
    else:

        if saut_compteur > 200:
            personnage.y -= 1
            saut_compteur -= 1
        elif saut_compteur > 0:
            personnage.y += 1
            saut_compteur -= 1
        else:
            saut = False
            saut_compteur = 400
        


    # Gravité
    if personnage.y < hauteur - 50 and not saut:
        personnage.y += 1

    # Collision avec les plateformes
    for plateforme in plateformes:
        if personnage.colliderect(plateforme):
            saut = False
            saut_compteur = 400
            personnage.y = plateforme.y - personnage.height

    # Effacer l'écran
    ecran.fill(blanc)

    # Dessiner le personnage
    pygame.draw.rect(ecran, bleu, personnage)

    # Dessiner les plateformes
    for plateforme in plateformes:
        pygame.draw.rect(ecran, bleu, plateforme)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
