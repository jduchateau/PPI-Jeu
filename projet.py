from pprint import pprint

import pygame
import math
import random

##### VARIABLES & CONSTANTES #####

WINDOWS_SIZE = (1000, 800)

GREY = (198, 186, 183)
BLACK = (52, 51, 50)
RED = (255, 70, 70)

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

# Vitesse
SPEED_MAX = 10
SPEED_MIN = 5
DIST_MOVE_MAX = 200

FIGURE_SIZE = (90, 115)
SHIELD_SIZE = (100, 120)
GUN_SIZE = (83, 114)
DECOR_SIZE = (300, 300)

DIST_ATTACK_MAX = 120
DIST_ENEMY_MIN = 90

GAUGE_SIZE = 100, 30
GAUGE_POSITION = WINDOWS_SIZE[0] - GAUGE_SIZE[0] - 50, 50


##### FONCTIONS #####

# TODO
#   après la mort du joueur afficher un message:
#       recomencer une partie
#       continuer à jouer (mode immortelle)
#       quitter
#   améliorer affichage attaque
#       meilleur placement
#       cacher après quelques secondes (Jakub)
#   attaque automatique des ennemis (Jakub)
#   emecher attaque en meme temps que bouclier
#   gérer les collision avec les décors (Raul)
#       et les actions qui en découle (Raul)


#### Début ENTITE #####
def new_entity(type):
    '''
    Créer une entité

    :param type: "gamer", "enemy", "decor1", "decor2", "decor3", "shield", "gun"
    :return:
    '''
    size = [0, 0]
    life = 0
    power = 10
    size_shield = SHIELD_SIZE
    size_gun = GUN_SIZE

    extra = {}
    if type == "gamer":
        size = FIGURE_SIZE
        life = 100
        power = 10
    elif type == "enemy":
        size = FIGURE_SIZE
        life = 10
        power = 0.5
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
        'active': True,  # Si faux ne peut rien faire ni attquer ni se défendre
        'position': [0, 0],
        'size': size,
        'speed': [0, 0],
        'color': None,
        'actualImg': None,
        'life': life,
        'power': power,
        'R': 300,  # Radius of vison
        'shield': {
            'active': False,
            'size': size_shield,
            'position': [0, 0]
        },
        'gun': {
            'active': False,
            'size': size_gun,
            'position': None,
            'end': 0,
            'direction': 0
        },
        'enemy': extra,

    }


def visible(entity):
    entity['visible'] = True


def invisible(entity):
    entity['visible'] = False


def is_visible(entity):
    return entity['visible']


def active(entity):
    entity['active'] = True


def inactive(entity, expiration=None):
    entity['active'] = False
    if expiration != None:
        entity['expiration'] = expiration


def is_active(entity):
    return entity['active']


def get_expiration(entity):
    if not is_active(entity):
        return entity['expiration']
    return None


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

    return entity['position']


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


def get_power(entity):
    return entity['power']


def set_power(entity, power, relatif):
    '''
    Définit la force de l'attque

    Si relatif ajoute power au pouvoir actuel
    :param entity:
    :param power: int
    :param relatif: bool
    :return:
    '''
    if relatif:
        entity['power'] += power
    else:
        entity['power'] = power


def get_life(entity):
    return entity['life']


def set_life(entity, life, relatif):
    '''
    Définit la force de l'attque

    Si relatif enleve life à la vie actuel
    :param entity:
    :param life: int
    :param relatif: bool
    :return:
    '''
    if relatif:
        entity['life'] += life
    else:
        entity['life'] = life


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

    if is_active(entity['shield']) and entity['type'] == "gamer":
        entity['shield']['position'][0] = entity['position'][0] - 5
        entity['shield']['position'][1] = entity['position'][1]
        ecran.blit(imgShield, (entity['shield']['position']))

    if is_active(entity['gun']):
        imgGunRotated = pygame.transform.rotate(imgGun, entity['gun']['direction'])
        ecran.blit(imgGunRotated, entity['gun']['position'])


##### FIN ENTITE ######

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

    if (dist >= dist_min and dist <= DIST_MOVE_MAX):
        speed = int(1 / (1 + math.exp(-(dist * 6 / DIST_MOVE_MAX))) * SPEED_MAX)
    elif (dist > DIST_MOVE_MAX):
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


def move_ennemy(entity, actualTime):
    '''
    Déplace l'ennemi en verifiant si le personnage est dans son champ de vision ou pas
        1) Si dans le champ de vision ( inVision == True) : il avance vers gamer avec la vitese de gamer // 2
        2) Si pas dans le champ de vision( inVision == False) : il se deplace sur une distance de 50 pixels avec une vitesse qui varie entre -2 et 2


    :param entity:
    '''

    # Si pas actif on s'arrête ici
    if not is_active(entity):
        # Et si l'entité a expire la supprime
        if get_expiration(entity) <= actualTime:
            invisible(entity)
            del entity

        return False

    inVision = entity['enemy']['inVision']
    deplace_dist = entity['enemy']['deplace_dist']
    randx = entity['enemy']['randx']
    randy = entity['enemy']['randy']

    # Calule la distance entre l'ennemis et le joueur
    gamer = gamers[0]
    dist = tuple(x - y for x, y in zip(get_position(gamer), get_position(entity)))  # différence entre deux tuples
    margin = DIST_ENEMY_MIN

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

        entity = new_entity(generator['type'])
        set_position(entity, position)
        set_image(entity, generator['image'])
        visible(entity)

        if generator['type'] == 'enemy':
            enemies.append(entity)
        elif generator['type'] in ['decor1', 'decor2', 'decor3']:
            decors.append(entity)
            # Supprime ancien décor en surplut
            if len(decors) > 5:
                del decors[0]


##### Fin GÉNÉRATEUR ######

##### Début Attaque #####
def attack(entity, target, time, addMort=True):
    '''
    Entity attaque target

    :param entity: entité à l'origine de l'attaque
    :param target: cible de l'attaque
    :param time: int
    :param addMort: incrémente nb_mort si vrai
    :return:
    '''
    global nb_morts

    delait = 800 #ms
    if not is_visible(target) or not is_active(target) \
            or is_active(entity['shield']):
        return False

    # Distence entre les deux
    delta_x = target['position'][0] - entity['position'][0]
    delta_y = target['position'][1] - entity['position'][1]
    dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

    print('Attaque ? ' + str(dist))

    if dist < DIST_ATTACK_MAX:
        print('!!! Attaque !!! ')

        active(entity['gun'])
        entity['gun']['end'] = time + delait

        # Calcule la direction et la position de l'image
        direction = math.degrees(math.asin(-delta_y / dist))
        print(direction)

        # Regle le problème de reduction de domaine (et de signe) dans l'arcsin
        if delta_x < 0:
            direction += 180

        entity['gun']['direction'] = direction
        set_position(entity['gun'], get_position(target))

        set_life(target, -get_power(entity), True)
        pprint({'Vie': get_life(target)})

        # Mort
        if get_life(target) <= 0:
            if addMort:
                nb_morts += 1
                pprint({'Nombre de morts': nb_morts})

            inactive(target, time + delait)


def auto_attack(ennemies, gamer, time):
    '''
    Les ennemies attaque le joueur

    :param ennemies: list
    :param gamer: entity
    :param time: int
    '''

    for i in range(len(ennemies)):
        delta_x = get_position(gamer)[0] - get_position(ennemies[i])[0]
        delta_y = get_position(gamer)[1] - get_position(ennemies[i])[1]
        dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

        if dist < DIST_ATTACK_MAX and is_active(ennemies[i]) and is_visible(ennemies[i]):
            attack(ennemies[i], gamer, time)
            print(get_life(gamer))


def attack_enemy(gamer, mouseposition, time):
    '''
    Attaque l'enemy dans la direction donné par la souris
    :param gamer:
    :param mouseposition:
    :return:
    '''

    targetPoint = mouseposition
    pprint(targetPoint)

    # Trouver l'ennemi dans cette direction
    for i in range(len(enemies)):
        if abs(targetPoint[0] - get_position(enemies[i])[0]) < DIST_ATTACK_MAX \
                and abs(targetPoint[1] - get_position(enemies[i])[1]) < DIST_ATTACK_MAX \
                and is_visible(enemies[i]):
            attack(gamer, enemies[i], time)


##### Fin Attaque #####

##### Collisions #####
def collision(entity, target):
    if ((entity['position'][0] + entity['size'][0]) >= target['position'][0] and entity['position'][0] <= (
            target['position'][0] + target['size'][0])):
        if ((entity['position'][1] + entity['size'][1]) >= target['position'][1] and entity['position'][1] <= (
                target['position'][1] + target['size'][1])):
            return 1
    else:
        return 0


def collisions_deco(entity, second):
    if (entity['type'] == "gamer"):
        if (collision(entity, second)):
            print('in babe')


##### Fin collisions #####

##### Définition JAUGE #####

def new_gauge(rect, fct_value):
    return {
        'rect': rect,
        'fct': fct_value
    }


def show_gauge(gauge, screen):
    left = gauge['fct']()
    if left < 0: left = 0
    rect = gauge['rect']
    witdh_death = int(rect.width * (100 - left) / 100)

    if left < 100:
        pygame.draw.rect(screen, RED, (rect.left, rect.top, witdh_death, rect.height))
    if left > 0:
        pygame.draw.rect(screen, BLACK, (rect.left + witdh_death, rect.top, rect.width - witdh_death, rect.height))


##### Fin JAUGE #####

def traite_entrees(time):
    global fini, mx, my
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            fini = True

        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == MOUSE_LEFT:
                mx, my = pygame.mouse.get_pos()
            elif evenement.button == MOUSE_RIGHT:
                attack_enemy(gamers[0], pygame.mouse.get_pos(), time)
                mx, my = pygame.mouse.get_pos()

        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                active(gamers[0]['shield'])  # gamer['shield']['active'] = True
        elif evenement.type == pygame.KEYUP:
            if evenement.key == pygame.K_SPACE:
                inactive(gamers[0]['shield'])  # gamer['shield']['active'] = False


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


def lifeGamer():
    global gamers
    return get_life(gamers[0])


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

imgGun = pygame.image.load(path + 'Attaque.png').convert_alpha(fenetre)
imgGun = pygame.transform.scale(imgGun, GUN_SIZE)
imgGun = pygame.transform.rotate(imgGun, -90)

# Personage
gamer = new_entity('gamer')

set_position(gamer, WINDOWS_SIZE[0] / 2 - get_size(gamer)[0] / 2, WINDOWS_SIZE[1] / 2 - get_size(gamer)[1] / 2)
set_image(gamer, imgE1Joueur)
visible(gamer)
gamers.append(gamer)

del gamer

# Generateurs
enemiesGenerator = new_generator('enemy', 5 * 1000, 'edge', imgE2Ennemis)
decor1Generator = new_generator('decor1', 5 * 1000, 'all', imgDecor1)
decor2Generator = new_generator('decor2', 10 * 1000, 'all', imgDecor2)
decor3Generator = new_generator('decor3', 10 * 1000, 'all', imgDecor3)

# Jauge de vie
gaugeLife = new_gauge(pygame.Rect(GAUGE_POSITION[0], GAUGE_POSITION[1], GAUGE_SIZE[0], GAUGE_SIZE[1]), lifeGamer)

##### OBJECTS INI END #####

##### VARIABLES #####
temps = pygame.time.Clock()
mx = WINDOWS_SIZE[0] / 2
my = WINDOWS_SIZE[1] / 2
fini = False
shield_position = (gamers[0]['position'][0], gamers[0]['position'][1])
nb_morts = 0

##### THE MAIN WHILE #####
while not fini:
    actualTime = pygame.time.get_ticks()
    levelGamer = level()
    traite_entrees(actualTime)
    fenetre.fill(GREY)
    draw_all()

    # Déplacement
    for enemy in enemies:
        move_ennemy(enemy, actualTime)

    move_gamer(gamers[0])

    auto_attack(enemies, gamers[0], actualTime)

    show_gauge(gaugeLife, fenetre)

    generate(enemiesGenerator, levelGamer, actualTime)
    generate(decor1Generator, levelGamer, actualTime)
    generate(decor2Generator, levelGamer, actualTime)
    generate(decor3Generator, levelGamer, actualTime)

    for decor in decors:
        if (decor['type'] == "decor2"):
            collisions_deco(gamers[0], decor)

    pygame.display.flip()
    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
