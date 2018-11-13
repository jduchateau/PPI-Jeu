from pprint import pprint

import pygame
import math
import random

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
SHIELD_SIZE = (100, 120)
GUN_SIZE = (100, 120)
DECOR_SIZE = (300, 300)


##### FONCTIONS #####


#### Début ENTITE #####
def new_entity(type):
    '''
    Créer une entité

    :param type: "gamer", "enemy", "decor1", "decor2", "decor3", "shield", "gun"
    :return:
    '''
    size = [0, 0]
    size_shield = SHIELD_SIZE
    size_gun = GUN_SIZE

    extra = {}
    if type == "gamer" or type == "enemy":
        size = FIGURE_SIZE
    elif type == "decor1":
        size = DECOR_SIZE

    if type == "enemy":
        extra = {'inVision': False,
                 'deplace_dist': 50,
                 'randx': 2,
                 'randy': 2}

    return {
        'type': type,
        'visible': False,
        'position': [0, 0],
        'size': size,
        'speed': [0, 0],
        'color': None,
        'actualImg': None,
        'life': 100,
        'R': 300,  # Radius of vison
        'shield': {
            'exist': False,
            'size': size_shield,
            'position': [0,0]
        },
        'gun': {
            'exist': False,
            'size': size_gun,
            'position': None
        },
        'enemy': extra,

    }


def visible(entity):
    entity['visible'] = True


def invisible(entity):
    entity['visible'] = False


def is_visible(entity):
    return entity['visible']


def set_position(entity, x, y=None):
    '''
    Modifie la position de l'entité

    Soit en donnant un couple de valeur ou séparée par une virgule

    :param entity:
    :param x:
    :param y:
    :return:
    '''
    if y != None:
        entity['position'][0] = x
        entity['position'][1] = y
    else:
        entity['position'] = list(x)


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
    if entity['shield']['exist'] == True and entity['type'] == "gamer":
        entity['shield']['position'][0] = entity['position'][0] - 5
        entity['shield']['position'][1] = entity['position'][1]
        ecran.blit(imgShield, (entity['shield']['position']))


### Début DÉPLACEMENT ####

def speed(entity, point, axe):
    '''
    On utilise la fonction sigmoide pour calculer la vitesse

    :param entity: object entité
    :param point:
    :param axe: 0 || 1
    :return: speed
    '''

    dist_min = entity['size'][0] // 2
    dist = abs((entity['position'][axe] + entity['size'][axe] // 2) - point)

    if (dist >= dist_min and dist <= DIST_MAX):
        speed = int(1 / (1 + math.exp(-(dist * 6 / DIST_MAX))) * SPEED_MAX)
    elif (dist > DIST_MAX):
        speed = SPEED_MAX
    else:
        if ((entity['position'][axe] + entity['size'][axe] // 2) != point):
            speed = 1
        else:
            speed = 0

    return speed


def move_gamer(entity):
    '''
    Déplace un joueur
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


def move_ennemy(entity):
    global inVision, deplace_dist, randx, randy
    '''
    Déplace l'ennemi en verifiant si le personnage est dans son champ de vision ou pas
        1) Si dans le champ de vision ( inVision == True) : il avance vers gamer avec la vitese de gamer // 2
        2) Si pas dans le champ de vision( inVision == False) : il se deplace sur une distance de 50 pixels avec une vitesse qui varie entre -2 et 2


    :param entity:
    '''
    inVision = entity['enemy']['inVision']
    deplace_dist = entity['enemy']['deplace_dist']
    randx = entity['enemy']['randx']
    randy = entity['enemy']['randy']

    # Calule la distance entre l'ennemis et le joueur
    gamer = gamers[0]
    dist = tuple(x - y for x, y in zip(get_position(gamer), get_position(entity)))  # différence entre deux tuples
    margin = gamer['size'][0]

    # Determine la vitesse
    # Verifie champ de vision
    if (dist[0] > entity['R']):
        inVision = False
    elif (dist[1] > entity['R']):
        inVision = False
    elif (dist[0] <= entity['R']):
        inVision = True
    elif (dist[1] <= entity['R']):
        inVision = True

    if (inVision == True):  # In the vision field
        vitessex = speed(entity, (gamer['position'][0] - entity['size'][0]), 0) / 2.0
        vitessey = speed(entity, gamer['position'][1], 1) / 2.0
        if (entity['position'][0] < (gamer['position'][0] - margin)):
            if (vitessex < 0):
                vitessex *= -1
        elif (entity['position'][0] > (gamer['position'][0] + margin)):
            if (vitessex > 0):
                vitessex *= -1
        else:
            vitessex = 0

        if (entity['position'][1] < (gamer['position'][1])):
            if (vitessey < 0):
                vitessey *= -1
        elif (entity['position'][1] > (gamer['position'][1])):
            if (vitessey > 0):
                vitessey *= -1
        else:
            vitessey = 0
    elif (inVision == False):  # Not in the vision field
        if (deplace_dist <= 0):
            deplace_dist = 50
            if (entity['position'][0] < 0):
                randx = random.randint(1, 2)
            elif (entity['position'][1] < 0):
                randy = random.randint(1, 2)
            else:
                randx = random.randint(-2, 2)
                randy = random.randint(-2, 2)
        if (deplace_dist > 0):
            deplace_dist -= 1
        vitessex = randx
        vitessey = randy

    # Applique le déplacement
    entity['position'][0] += vitessex
    entity['position'][1] += vitessey

    entity['enemy']['inVision'] = inVision
    entity['enemy']['deplace_dist'] = deplace_dist
    entity['enemy']['randx'] = randx
    entity['enemy']['randy'] = randy


#### Fin DÉPLACEMENT #####

##### FIN ENTITE ######

##### Début GÉNÉRATEUR ######

def new_generator(type, frequency, zone, image):
    '''
    Créer un générateur

    :param type: "enemy", "decor1", "decor2", "decor3"
    :param frequency: frequence de base en miliseconde
    :param zone: "edge", "all"
    :param image: Surface
    :return:
    '''
    return {
        "type": type,
        "frequency": frequency,
        "zone": zone,
        "new_time": 0,
        "image": image
    }


def generate(generator, level, time):
    '''

    :param generator:
    :param level:
    :return:
    '''

    global gamers, enemies, decors

    if generator['new_time'] < time:
        # Nouveau temps
        new_time = time + generator["frequency"] - level / 1000
        generator['new_time'] = new_time

        # Choisi l'emplacelent
        position = (0, 0)
        if generator['zone'] == 'edge':
            if random.randint(0, 1):
                position = (0, random.randint(0, WINDOWS_SIZE[1]))
            else:
                position = (random.randint(0, WINDOWS_SIZE[0]), 0)
        elif generator['zone'] == 'all':
            position = (random.randint(0, WINDOWS_SIZE[0]), random.randint(0, WINDOWS_SIZE[1]))
            pprint(position)

        entity = new_entity(generator['type'])
        set_position(entity, position)
        set_image(entity, generator['image'])
        visible(entity)

        if generator['type'] == 'enemy':
            enemies.append(entity)
        elif generator['type'] in ['decor1', 'decor2', 'decor3']:
            decors.append(entity)
            # Supprime ancien décor en surplut
            if len(decors) > 2:
                del decors[0]


##### Fin GÉNÉRATEUR ######


def traite_entrees():
    global fini, mouse_clicked, mx, my
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == MOUSE_LEFT:
            mouse_clicked = True
            mx, my = pygame.mouse.get_pos()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                gamer['shield']['exist'] = True
            else:
                gamer['shield']['exist'] = False

def draw_all():
    global gamers, enemies, decors

    # Fusionne les listes dans le bonne ordre
    entities = decors + enemies + gamers
    for entity in entities:
        draw(entity, fenetre)


def level():
    '''
    Calcule le niveau du joueur

    :return: level [0-infinity[
    '''
    global nb_morts

    return nb_morts // 5

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

imgShield = pygame.image.load(path + 'Bouclier.png').convert_alpha(fenetre)
imgShield = pygame.transform.scale(imgShield, SHIELD_SIZE)

# Personage
gamer = new_entity('gamer')

set_position(gamer, WINDOWS_SIZE[0] / 2 - get_size(gamer)[0] / 2, WINDOWS_SIZE[1] / 2 - get_size(gamer)[1] / 2)
set_image(gamer, imgE1Joueur)
visible(gamer)
gamers.append(gamer)

# Generateurs
enemiesGenerator = new_generator('enemy', 5 * 1000, 'edge', imgE2Ennemis)
decor1Generator = new_generator('decor1', 5 * 1000, 'all', imgDecor1)
decor2Generator = new_generator('decor2', 5 * 1000, 'all', imgDecor2)
decor3Generator = new_generator('decor3', 5 * 1000, 'all', imgDecor3)

##### OBJECTS INI END #####

##### VARIABLES #####
temps = pygame.time.Clock()
mx = 0
my = 0
mouse_clicked = False
fini = False
shield_position =(gamer['position'][0], gamer['position'][1])
nb_morts = 0

##### THE MAIN WHILE #####
while not fini:
    actualTime = pygame.time.get_ticks()
    levelGamer = level()
    traite_entrees()
    fenetre.fill(GREY)
    draw_all()

    # Déplacement
    for enemy in enemies:
        move_ennemy(enemy)

    if mouse_clicked:
        move_gamer(gamers[0])

    generate(enemiesGenerator, levelGamer, actualTime)
    generate(decor1Generator, levelGamer, actualTime)

    pygame.display.flip()
    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
