from pprint import pprint

import pygame
import math

##### VARIABLES & CONSTANTES #####

WINDOWS_SIZE = (1000, 800)

GREY = (198, 186, 183)
BLACK_PERS = (52, 51, 50)

MOUSE_LEFT = 1
MOUSE_RIGHT = 2

# Vitesse
SPEED_MAX = 10
SPEED_MIN = 5
DIST_MAX = 200

FIGURE_SIZE = (90, 115)
DECOR_SIZE = (300, 300)


##### FONCTIONS #####


#### Début ENTITE #####
def new_entity(type):
    '''

    :param type: "gamer", "enemy", "decor1", "decor2", "decor3"
    :return:
    '''
    return {
        'type': type,
        'visible': True,
        'position': [0, 0],
        'size': [0, 0],
        'speed': [0, 0],
        'color': None,
        'actualImg': None,
        'life': 100
    }


def visible(entity):
    entity['visible'] = True


def invisible(entity):
    entity['visible'] = False


def is_visible(entity):
    return entity['visible']


def set_position(entity, x, y):
    entity['position'][0] = x
    entity['position'][1] = y


def get_position(entity, round=False):
    '''
    Retourne la position de l'entité arrondie si demandé dans int

    :param entity:
    :param round: Arrondis les valeur de la position
    :return: Position
    '''
    if round:
        return int(entity['position'][0]), int(entity['position'][1])

    return tuple(entity['position'])


def set_size(entity, w, h=None):
    '''
    Modifie la taille d'une entité.

    Soit en donnant la largeur et hauteur séparément ou dans un Tulp.
    :param entity:
    :param w:
    :param h:
    '''
    if h != None:
        entity['size'][0] = w
        entity['size'][1] = h
    else:
        entity['size'][0] = w[0]
        entity['size'][1] = w[1]


def get_size(entity):
    return tuple(entity['size'])


def set_image(entity, image):
    entity['actualImg'] = image


def get_image(entity):
    return entity['actualImg']


def set_color(entity, c):
    entity['color'] = c


def draw(entity, ecran):
    '''
    Dessine l'entité sur la fenetre selon les parametres de celle ci.

    Si il y a une couleur un rectangle de  cette couleur
    Si il y a une image l'image à la taille
    :param entity:
    :param ecran:
    '''
    if not is_visible(entity):
        return

    if entity['color'] is tuple:
        pygame.draw.rect(ecran, entity['color'], (entity['position'], entity['size']))
    elif get_image(entity):
        ecran.blit(get_image(entity), get_position(entity, True))


def speed(entity, mouse, axe):
    '''
    On utilise la fonction sigmoide pour calculer la vitesse

    :param entity: object entité
    :param mouse:
    :param axe: 0 || 1
    :return: speed
    '''

    dist_min = entity['size'][0] // 2
    dist = abs((entity['position'][axe] + entity['size'][axe] // 2) - mouse)

    if (dist >= dist_min and dist <= DIST_MAX):
        speed = int(1 / (1 + math.exp(-(dist * 6 / DIST_MAX))) * SPEED_MAX)
    elif (dist > DIST_MAX):
        speed = SPEED_MAX
    else:
        if ((entity['position'][axe] + entity['size'][axe] // 2) != mouse):
            speed = 1
        else:
            speed = 0

    return speed


def move_entity(entity):
    '''
    Déplace l'entité
    :param entity:
    '''
    global mx, my

    # verifie vitese (compare si la x > ou < xmouse et si y > ou < que ymouse) et modifier la vitesse
    vx = speed(entity, mx, 0)
    vy = speed(entity, my, 1)

    if ((entity['position'][0] + entity['size'][0] / 2) > mx):
        if (vx > 0):
            vx *= -1
    elif ((entity['position'][0] + entity['size'][0] / 2) < mx):
        if (vx < 0):
            vx *= -1

    if ((entity['position'][1] + entity['size'][1] / 2) > my):
        if (vy > 0):
            vy *= -1
    elif ((entity['position'][1] + entity['size'][1] / 2) < my):
        if (vy < 0):
            vy *= -1
    # verifie vitese fin

    if ((entity['position'][0] + entity['size'][0] / 2) != mx):
        entity['position'][0] += vx
    if ((entity['position'][1] + entity['size'][1] / 2) != my):
        entity['position'][1] += vy


##### FIN ENTITE ######

def traite_entrees():
    global fini, mouse_clicked, mx, my
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == MOUSE_LEFT:
            mouse_clicked = True
            mx, my = pygame.mouse.get_pos()


def draw_all():
    global gamers, enemies, decors

    # Fusionne les listes dans le bonne ordre
    entities = decors + enemies + gamers
    for entity in entities:
        draw(entity, fenetre)


##### OBJECTS INIT #####
pygame.init()

fenetre = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption('Battail dans le vide')

# Liste des entitées selon le type
gamers = []
enemies = []
decors = []

# Images
path = 'img/'
imgE1Joueur = pygame.image.load(path + 'E1_Joueur.png').convert_alpha(fenetre)
imgE1Joueur = pygame.transform.scale(imgE1Joueur, FIGURE_SIZE)

imgE2Ennemis = pygame.image.load(path + 'E2_Ennemis.png').convert_alpha(fenetre)
imgE2Ennemis = pygame.transform.scale(imgE2Ennemis, FIGURE_SIZE)

imgDecor1 = pygame.image.load(path + 'Decor_1.png').convert_alpha(fenetre)
imgDecor1 = pygame.transform.scale(imgDecor1, DECOR_SIZE)

imgDecor2 = pygame.image.load(path + 'Decor_2.png').convert_alpha(fenetre)
imgDecor2 = pygame.transform.scale(imgDecor2, DECOR_SIZE)

imgDecor3 = pygame.image.load(path + 'Decor_3.png').convert_alpha(fenetre)
imgDecor3 = pygame.transform.scale(imgDecor3, DECOR_SIZE)

# Personage
gamer = new_entity('gamer')

set_size(gamer, FIGURE_SIZE)
set_position(gamer, WINDOWS_SIZE[0] / 2 - get_size(gamer)[0] / 2, WINDOWS_SIZE[1] / 2 - get_size(gamer)[1] / 2)
set_image(gamer, imgE1Joueur)
visible(gamer)
gamers.append(gamer)

# Decor (artificel)
decor1 = new_entity('decor1')

set_size(decor1, DECOR_SIZE)
set_position(decor1, WINDOWS_SIZE[0] * 4 / 6, WINDOWS_SIZE[1] / 2)
set_image(decor1, imgDecor1)
visible(decor1)

decors.append(decor1)


##### OBJECTS INI END #####

##### VARIABLES #####
temps = pygame.time.Clock()
mx = 0
my = 0
mouse_clicked = False
fini = False

##### THE MAIN WHILE #####
while not fini:
    traite_entrees()
    fenetre.fill(GREY)
    draw_all()
    if (mouse_clicked == True):
        move_entity(gamer)
    pygame.display.flip()
    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
