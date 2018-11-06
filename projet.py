import pygame
import math

##### VARIABLES & CONSTANTES #####

FENETRE_HAUTEUR = 800
FENETRE_LARGEUR = 1000

GREY       = (198, 186, 183)
BLACK_PERS = ( 52,  51,  50)

MOUSE_LEFT = 1
MOUSE_RIGHT = 2


#### Vitesse
SPEED_MAX = 10
SPEED_MIN = 5
DIST_MAX = 200


##### FONCTIONS #####


#### Début ENTITE #####
def new_entity():
    return {
        'visible': True,
        'position': [0, 0],
        'size': [0, 0],
        'color': None,
        'actualImg': None,
        'life':100
    }


def visible(entity):
    entity['visible'] = True


def invisible(entity):
    entity['visible'] = False


def place(entity, x, y):
    entity['position'][0] = x
    entity['position'][1] = y


def set_size(entity, w, h):
    entity['size'][0] = w
    entity['size'][1] = h


def set_color(entity, c):
    entity['color'] = c


def dessine(ecran, entity, number):
    # ecran.bilt(entity['actualImg'], entity['position'])
    if (number == 0):
        pygame.draw.rect(ecran, entity['color'], (entity['position'], entity['size']))
    elif (number == 1):
        pygame.draw.circle(ecran, entity['color'], entity['position'], entity['size'][0] // 2)


def vitesse(entity, m, axe):
    '''
    On utilise la fonction sigmoide pour calculer la vitesse

    :param entity: object entité
    :param m: TODO je ne comprend pas "m"
    :param axe: 0 || 1
    :return: vitesse
    '''

    dist_min = entity['size'][0] // 2
    dist = abs((entity['position'][axe] + entity['size'][axe] // 2) - m)

    if (dist >= dist_min and dist <= DIST_MAX):
        # v = k*entity['position'][axe] + t
        v = int(1 / (1 + math.exp(-(dist * 6 / DIST_MAX))) * SPEED_MAX)
    elif (dist > DIST_MAX):
        v = SPEED_MAX
    else:
        if ((entity['position'][axe] + entity['size'][axe] // 2) != m):
            v = 1
        else:
            v = 0

    return v


def move_pers(entity, vx, vy):
    global mx, my
    ## verifie vitese (  compare si la x > ou < xmouse et si y > ou < que ymouse) et modifier la vitesse
    vx = vitesse(entity, vx, mx, 0)
    vy = vitesse(entity, vy, my, 1)

    if ((entity['position'][0] + entity['size'][0] // 2) > mx):
        if (vx > 0):
            vx *= -1
    elif ((entity['position'][0] + entity['size'][0] // 2) < mx):
        if (vx < 0):
            vx *= -1
    if ((entity['position'][1] + entity['size'][1] // 2) > my):
        if (vy > 0):
            vy *= -1
    elif ((entity['position'][1] + entity['size'][1] // 2) < my):
        if (vy < 0):
            vy *= -1
    ## verifie vitese fin

    if ((entity['position'][0] + entity['size'][0] // 2) != mx):
        entity['position'][0] += vx
    if ((entity['position'][1] + entity['size'][1] // 2) != my):
        entity['position'][1] += vy


# print(" dx: ", diff_vx)
#### FIN ENTITE
def traite_entrees():
    global fini, mouse_clicked, mx, my
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == MOUSE_LEFT:
            mouse_clicked = True
            mx, my = pygame.mouse.get_pos()


def draw():
    # choisir 0 : dissiner un rect
    # choisir 1 : dessiner une sphere
    dessine(fenetre, pers, 0)


pygame.init()
############ INITIALISE ############
#### PERS
pers_size = (30, 30)
pers_location = ((FENETRE_LARGEUR // 2 - pers_size[0] // 2), (FENETRE_HAUTEUR // 2 - pers_size[1] // 2))
pers = new_entity()
visible(pers)
set_size(pers, pers_size[0], pers_size[1])
set_color(pers, BLACK_PERS)
place(pers, pers_location[0], pers_location[1])

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('Game')

############ INITIALISE END ############

############ VARIABLES ############
temps = pygame.time.Clock()
mx = 0
my = 0
mouse_clicked = False
fini = False

############ THE MAIN WHILE ############
while not fini:
    traite_entrees()
    fenetre.fill(GREY)
    draw()
    if (mouse_clicked == True):
        move_pers(pers, 3, 3)
    pygame.display.flip()
    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
