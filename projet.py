from pprint import pprint

import pygame
import pygame.freetype
import math
import random

##### VARIABLES & CONSTANTES #####

ZOOM = 0.8
WINDOWS_SIZE = (int(1000*ZOOM), int(800*ZOOM))
GREY = (198, 186, 183)
BLACK = (52, 51, 50)
RED = (255, 70, 70)

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

# Vitesse
SPEED_MAX = 10
SPEED_MIN = 5
DIST_MOVE_MAX = 200

FIGURE_SIZE = (int(90*ZOOM), int(115*ZOOM))
SHIELD_SIZE = (int(100*ZOOM), int(120*ZOOM))
GUN_SIZE = (int(83*ZOOM), int(114*ZOOM))
DECOR_SIZE = (int(300*ZOOM), int(300*ZOOM))

DIST_ATTACK_MAX = 150  # px
ATTACK_DURATION = 500  # ms
DIST_ENEMY_MIN = 90

GAUGE_SIZE = int(100*ZOOM), int(30*ZOOM)
GAUGE_POSITION = WINDOWS_SIZE[0] - GAUGE_SIZE[0] - int(50*ZOOM), int(50*ZOOM)


##### FONCTIONS #####

#### Début ENTITE #####
def new_entity(type):
    '''
    Créer une entité

    :param type: "gamer", "enemy", "decor1", "decor2", "decor3"
    :return:
    '''
    size = [0, 0]
    life = 0
    power = 10
    images = {}
    size_shield = SHIELD_SIZE
    size_gun = GUN_SIZE
    # size_gun = 0
    extra = {}
    if type == "gamer":
        size = FIGURE_SIZE
        life = 100
        power = 10
    elif type == "enemy":
        size = FIGURE_SIZE
        life = 10
        power = 0.5
    elif type in ("decor1", "decor2", "decor3"):
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
        'animations': {},
        'images': images,
        'actualAnimation': {'name': '', 'step': None, 'time': None, 'repete': False},
        'actual_direction_img': 'right'
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


def set_life(entity, life, relatif=False):
    '''
    Définit la force de l'attque

    Si relatif ajoute life à la vie actuel (en vérifiant les bornes [0, 100])
    :param entity:
    :param life: int
    :param relatif: bool
    :return:
    '''
    if relatif:
        entity['life'] += life
        if entity['life'] > 100:
            entity['life'] = 100
        elif entity['life'] < 0:
            entity['life'] = 0
    else:
        entity['life'] = life


##### Fin ENTITEE ######


##### Début ANIMATION ######

def create_animation(entity, animation, images=False):
    '''
    Creer une animation
    :param entity: le nom de l'entité
    :param animation: nom : [{Nom_Image, Temps}, ...]
    :param images: la posibilité d'ajouter des objets de surface nommée
    '''
    entity['animations'].update(animation)

    if isinstance(images, dict):
        entity['images'].update(images)


def start_animation(entity, animation_name, temps, repete):
    '''
    Commencer une animation
    :param entity: le nom de l'entité
    :param animation_name: le nom de l'animation
    :param temps : temps actuen en milisecondes
    :param repete: le nombre de fois que l'animation va etre répétée
    '''
    actual_time = temps
    entity['actualAnimation']['name'] = animation_name
    entity['actualAnimation']['step'] = 0
    entity['actualAnimation']['time'] = actual_time
    entity['actualAnimation']['repete'] = repete


def is_animated(entity):
    return entity['actualAnimation']['name'] != '', entity['actualAnimation']['name']


def stop_animation(entity):
    '''
    Arreter une animation
    :param entity: le nom de l'entité
    '''
    entity['actualAnimation']['name'] = ''
    entity['actualAnimation']['step'] = None
    entity['actualAnimation']['time'] = None
    entity['actualAnimation']['repete'] = False


def get_actual_image(entity, actualtime):
    '''
    Retourne la surface affichée actuelement
    :param entity: le nom de l'entité
    :param actualtime: temps actuel en ms
    :return: surface
    '''

    name = entity['actualAnimation']['name']
    step = entity['actualAnimation']['step']
    animTime = entity['actualAnimation']['time']
    repete = entity['actualAnimation']['repete']

    if name != '' and name in entity['animations']:
        nomImage, duree = entity['animations'][name][step]

        if duree == None:
            nextTime = actualTime + 1  # force vrai
        else:
            nextTime = animTime + duree  # prochain changement

        if actualtime < nextTime:
            image = entity['images'][nomImage]
            return image
        else:
            if step == len(entity['animations'][name]) - 1:
                if repete:
                    step = 0
                else:
                    stop_animation(entity)
            else:
                step += 1

            entity['actualAnimation']['step'] = step
            entity['actualAnimation']['time'] = actualTime
            nomImage = entity['animations'][name][step][0]
            return entity['images'][nomImage]
    else:
        return None


def draw(entity, ecran, time):
    '''
    Dessine l'entité sur la fenetre selon les parametres de celle ci.

    Si il y a une couleur un rectangle de  cette couleur
    Si il y a une image l'image à la taille
    :param entity:
    :param ecran:
    '''
    if not is_visible(entity):
        return

    surface = get_actual_image(entity, time)
    if surface != None:
        ecran.blit(surface, get_position(entity, True))

    if is_active(entity['shield']) and entity['type'] == "gamer":
        entity['shield']['position'][0] = entity['position'][0] - 5
        entity['shield']['position'][1] = entity['position'][1]
        ecran.blit(imgShield, (entity['shield']['position']))

    # Désactive l'épé si expirée et affiche
    if entity['gun']['end'] < time:
        inactive(entity['gun'])

    if is_active(entity['gun']):
        if entity['type'] == 'gamer':
            imgGunRotated = pygame.transform.rotate(imgGun, entity['gun']['direction'])
        else:
            imgGunRotated = pygame.transform.rotate(imgGunEnnemy, entity['gun']['direction'])
        ecran.blit(imgGunRotated, entity['gun']['position'])



##### Fin ANIMATION ######

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


def move_gamer(entity, temps):
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

    if (vx == 0 and vy == 0):
        start_animation(entity, 'anim_gamer_' + entity['actual_direction_img'] + '_static', temps, True)
    else:
        if (vx < 0 and is_animated(entity)[1] != "anim_gamer_left"):
            start_animation(entity, 'anim_gamer_left', temps, True)
            entity['actual_direction_img'] = 'left'
        elif (vx > 0 and is_animated(entity)[1] != "anim_gamer_right"):
            start_animation(entity, 'anim_gamer_right', temps, True)
            entity['actual_direction_img'] = 'right'


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
    delta_x = get_position(gamer)[0] - get_position(entity)[0]
    delta_y = get_position(gamer)[1] - get_position(entity)[1]
    dist = math.hypot(delta_x, delta_y)
    margin = DIST_ENEMY_MIN

    # Determine la vitesse
    # Verifie si le joueur est dans le champ de vision
    if (dist > entity['R']):
        inVision = False
    else:
        inVision = True

    if inVision:  # In the vision field
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

    else:  # Not in the vision field
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

    # Animation
    print(vitessex, vitessey)
    if (vitessex == 0 and vitessey == 0):
        start_animation(entity, 'anim_enemy_' + entity['actual_direction_img'] + '_static', actualTime, True)
    else:
        if (vitessex < 0 and is_animated(entity)[1] != "anim_enemy_left"):
            start_animation(entity, 'anim_enemy_left', actualTime, True)
            entity['actual_direction_img'] = 'left'
        elif (vitessex > 0 and is_animated(entity)[1] != "anim_enemy_right"):
            start_animation(entity, 'anim_enemy_right', actualTime, True)
            entity['actual_direction_img'] = 'right'

    # Applique le déplacement
    entity['position'][0] += vitessex
    entity['position'][1] += vitessey

    entity['enemy']['inVision'] = inVision
    entity['enemy']['deplace_dist'] = deplace_dist
    entity['enemy']['randx'] = randx
    entity['enemy']['randy'] = randy


#### Fin DÉPLACEMENT #####

##### Début GÉNÉRATEUR ######

def new_generator(type, frequency, zone, animation, images):
    '''
    Créer un générateur

    :param type: "enemy", "decor1", "decor2", "decor3"
    :param frequency: frequence de base en miliseconde
    :param zone: "edge", "all"
    :param animation: dictionnaire d'animation
    :param images:dictionnaire d'images
    :return:
    '''
    return {
        "type": type,
        "frequency": frequency,
        "zone": zone,
        "new_time": 0,
        "animation": animation,
        "images": images
    }


def generate(generator, level, time):
    '''

    :param generator:
    :param level:
    :return:
    '''

    global gamers, enemies, decors
    global anim_enemy_right, anim_enemy_left, images_enemy, imgDecor1, imgDecor2, imgDecor3

    if generator['new_time'] < time:
        # Nouveau temps
        new_time = time + generator["frequency"]
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

        # Ajoute les animations et images
        create_animation(entity, generator['animation'], generator['images'])

        visible(entity)

        if generator['type'] == 'enemy':
            set_life(entity, level * 1 / 5, True)

            enemies.append(entity)
        elif generator['type'] in ['decor1', 'decor2', 'decor3']:
            start_animation(entity, 'anim_' + generator['type'], time, True)

            pprint(entity)

            decors.append(entity)
            # Supprime ancien décor en surplut
            if len(decors) > 5:
                del decors[0]


##### Fin GÉNÉRATEUR ######

##### Début Attaque #####
def attack(entity, target, time, addMort):
    '''
    Entity attaque target

    :param entity: entité à l'origine de l'attaque
    :param target: cible de l'attaque
    :param time: int
    :param addMort: incrémente nb_mort ou le joueur meurt
    :return:
    '''
    global nb_morts, mort

    if not is_visible(target) or not is_active(target) \
            or is_active(target['shield']) or is_active(entity['shield']):
        return False

    # Distence entre les deux
    delta_x = target['position'][0] - entity['position'][0]
    delta_y = target['position'][1] - entity['position'][1]
    dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

    if dist < DIST_ATTACK_MAX:

        active(entity['gun'])
        entity['gun']['end'] = time + ATTACK_DURATION

        # Calcule la direction et la position de l'image
        direction = 0
        if dist != 0:
            if delta_y <= 0:
                direction = math.acos(delta_x / dist)
            else:
                direction = -math.acos(delta_x / dist)

        entity['gun']['direction'] = math.degrees(direction)
        set_position(entity['gun'], get_position(target))

        set_life(target, -get_power(entity), True)

        # Mort
        if get_life(target) <= 0:
            if addMort:
                nb_morts += 1
            else:
                mort = True

            inactive(target, time + ATTACK_DURATION)


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
        dist = math.hypot(delta_x, delta_y)

        if dist < DIST_ATTACK_MAX and is_active(ennemies[i]) and is_visible(ennemies[i]):
            attack(ennemies[i], gamer, time, False)


def attack_enemy(gamer, mouseposition, time):
    '''
    Attaque l'enemy dans la direction donné par la souris
    :param gamer:
    :param mouseposition:
    :return:
    '''

    targetPoint = mouseposition

    # Trouver l'ennemi dans cette direction
    for i in range(len(enemies)):
        if abs(targetPoint[0] - get_position(enemies[i])[0]) < DIST_ATTACK_MAX \
                and abs(targetPoint[1] - get_position(enemies[i])[1]) < DIST_ATTACK_MAX \
                and is_visible(enemies[i]):
            attack(gamer, enemies[i], time, True)


##### Fin Attaque #####

##### Définition Collisions #####

def colliRectCicle(rleft, rtop, width, height, center_x, center_y, radius):
    '''
    Détecte une collision entre un rectangle et un cercle

    inspiré de [https://stackoverflow.com/questions/24727773/detecting-rectangle-collision-with-a-circle]
    '''

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width / 2, rtop + height / 2

    # bounding box of the circle
    cleft, ctop = center_x - radius, center_y - radius
    cright, cbottom = center_x + radius, center_y + radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft + width):
        for y in (rtop, rtop + height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x - center_x, y - center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected


def collision_decors(gamer):
    '''
    Détecte une collision entre le gamer
    et les décors et applique les actions requises
    '''
    global decors

    rleft = get_position(gamer)[0]
    rtop = get_position(gamer)[1]
    width = get_size(gamer)[0]
    height = get_size(gamer)[1]

    for decor in decors:

        radius = get_size(decor)[0] / 2
        center_x = get_position(decor)[0] + radius
        center_y = get_position(decor)[1] + radius

        if colliRectCicle(rleft, rtop, width, height, center_x, center_y, radius):
            type = decor['type']
            if type == 'decor2':
                set_life(gamer, -0.05, True)
            elif type == 'decor3':
                set_life(gamer, 0.05, True)


##### Fin Collisions #####

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
    global fini, mx, my, gamers, partie_enCours, mort
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            fini = True
            partie_enCours = False

        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == MOUSE_LEFT:
                mx, my = pygame.mouse.get_pos()
            elif evenement.button == MOUSE_RIGHT:
                attack_enemy(gamers[0], pygame.mouse.get_pos(), time)

        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                active(gamers[0]['shield'])
            elif evenement.key == pygame.K_q:
                mort = True
        elif evenement.type == pygame.KEYUP:
            if evenement.key == pygame.K_SPACE:
                inactive(gamers[0]['shield'])


def traite_entrees_menu():
    global fini, partie_enCours, immortelle, gamers
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            fini = True
            partie_enCours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                partie_enCours = True
                fini = False

            elif evenement.key == pygame.K_r:
                partie_enCours = False
                fini = False

            elif evenement.key == pygame.K_i:
                partie_enCours = True
                fini = False
                immortelle = True

            elif evenement.key == pygame.K_q:
                fini = True
                partie_enCours = False


def draw_all(time):
    global gamers, enemies, decors

    # Fusionne les listes dans le bonne ordre
    entities = decors + enemies + gamers
    for entity in entities:
        draw(entity, fenetre, time)


def draw_intro_menu(fenetre):
    global font_title, font_small

    title_text = "The Dream Survivor"
    explanation_text = "Utiliser la souris et la barre d'espace"

    title = font_title.render(title_text, True, BLACK)
    # title = font_title.render(title_text, True, BLACK)
    title_width, title_height = font_title.size(title_text)

    explanation = font_small.render(explanation_text, True, BLACK)
    explanation_width, explanation_height = font_small.size(explanation_text)

    fenetre.fill(GREY)
    fenetre.blit(title, ((WINDOWS_SIZE[0] - title_width) // 2, WINDOWS_SIZE[1] // 3 - title_height // 2))
    fenetre.blit(explanation,
                 (WINDOWS_SIZE[0] // 2 - explanation_width // 2, 2 * WINDOWS_SIZE[1] // 3 - title_height // 2))


def draw_final_menu(fenetre):
    global font_title, font_small

    title_text = "Mort"
    exp1_text = "[R] pour recommencer une partie"
    exp2_text = "[I] pour devenir immortelle"
    exp3_text = "[Q] pour partir"

    marge = 10

    title = font_title.render(title_text, True, BLACK)
    title_width, title_height = font_title.size(title_text)
    title_position = ((WINDOWS_SIZE[0] - title_width) // 2, WINDOWS_SIZE[1] // 3)

    exp1 = font_small.render(exp1_text, True, BLACK)
    exp1_width, exp1_height = font_small.size(exp1_text)
    exp1_position = (((WINDOWS_SIZE[0] - exp1_width) // 2), WINDOWS_SIZE[1] // 3 + title_height + marge)

    exp2 = font_small.render(exp2_text, True, BLACK)
    exp2_width, exp2_height = font_small.size(exp2_text)
    exp2_position = (
        ((WINDOWS_SIZE[0] - exp2_width) // 2), WINDOWS_SIZE[1] // 3 + title_height + exp1_height + 2 * marge)

    exp3 = font_small.render(exp3_text, True, BLACK)
    exp3_width, exp3_height = font_small.size(exp3_text)
    exp3_position = (
        (WINDOWS_SIZE[0] - exp3_width) // 2,
        WINDOWS_SIZE[1] // 3 + title_height + exp1_height + exp2_height + 3 * marge)

    fenetre.blit(title, title_position)
    fenetre.blit(exp1, exp1_position)
    fenetre.blit(exp2, exp2_position)
    fenetre.blit(exp3, exp3_position)


def draw_level(fenetre):
    global font_small, nb_morts

    text = str(level()) + ' | ' + str(nb_morts)

    textRend = font_small.render(text, False, BLACK)
    text_width, text_height = font_small.size(text)
    text_position = GAUGE_POSITION[0] + GAUGE_SIZE[0] - text_width, GAUGE_POSITION[1] + GAUGE_SIZE[1] + 10

    fenetre.blit(textRend, text_position)


def level():
    '''
    Calcule le niveau du joueur

    :return: level [0-infinity[
    '''
    global nb_morts

    return nb_morts // 3


def lifeGamer():
    global gamers
    return get_life(gamers[0])


def createGamer():
    global gamers, anim_gamer_left, anim_gamer_right, anim_gamer_left_static, anim_gamer_right_static, images_gamer
    gamer = new_entity('gamer')

    animationsGamer = {
        'anim_gamer_left': anim_gamer_left,
        'anim_gamer_right': anim_gamer_right,
        'anim_gamer_left_static': anim_gamer_left_static,
        'anim_gamer_right_static': anim_gamer_right_static
    }

    create_animation(gamer, animationsGamer, images_gamer)

    set_position(gamer, WINDOWS_SIZE[0] / 2 - get_size(gamer)[0] / 2, WINDOWS_SIZE[1] / 2 - get_size(gamer)[1] / 2)
    visible(gamer)
    gamers.append(gamer)


##### OBJECTS INIT #####


pygame.init()

fenetre = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Batail des rêves")

font_title = pygame.font.SysFont('Manjari', 36, True)
# font_title = pygame.freetype.Font('Manjari-Regular.ttf', 36)
font_small = pygame.font.SysFont('Manjari', 24, True)

# Chargement des Images
path = 'img/'

gamer_right_static = pygame.image.load(path + 'Joueur_DS.png').convert_alpha(fenetre)
gamer_right_static = pygame.transform.scale(gamer_right_static, FIGURE_SIZE)
gamer_right_left = pygame.image.load(path + 'Joueur_DD.png').convert_alpha(fenetre)
gamer_right_left = pygame.transform.scale(gamer_right_left, FIGURE_SIZE)
gamer_right_right = pygame.image.load(path + 'Joueur_DG.png').convert_alpha(fenetre)
gamer_right_right = pygame.transform.scale(gamer_right_right, FIGURE_SIZE)

gamer_left_static = pygame.image.load(path + 'Joueur_GS.png').convert_alpha(fenetre)
gamer_left_static = pygame.transform.scale(gamer_left_static, FIGURE_SIZE)
gamer_left_left = pygame.image.load(path + 'Joueur_GD.png').convert_alpha(fenetre)
gamer_left_left = pygame.transform.scale(gamer_left_left, FIGURE_SIZE)
gamer_left_right = pygame.image.load(path + 'Joueur_GG.png').convert_alpha(fenetre)
gamer_left_right = pygame.transform.scale(gamer_left_right, FIGURE_SIZE)

enemy_right_static = pygame.image.load(path + 'Ennemis_DS.png').convert_alpha(fenetre)
enemy_right_static = pygame.transform.scale(enemy_right_static, FIGURE_SIZE)
enemy_right_left = pygame.image.load(path + 'Ennemis_DD.png').convert_alpha(fenetre)
enemy_right_left = pygame.transform.scale(enemy_right_left, FIGURE_SIZE)
enemy_right_right = pygame.image.load(path + 'Ennemis_DG.png').convert_alpha(fenetre)
enemy_right_right = pygame.transform.scale(enemy_right_right, FIGURE_SIZE)

enemy_left_static = pygame.image.load(path + 'Ennemis_GS.png').convert_alpha(fenetre)
enemy_left_static = pygame.transform.scale(enemy_left_static, FIGURE_SIZE)
enemy_left_left = pygame.image.load(path + 'Ennemis_GG.png').convert_alpha(fenetre)
enemy_left_left = pygame.transform.scale(enemy_left_left, FIGURE_SIZE)
enemy_left_right = pygame.image.load(path + 'Ennemis_GD.png').convert_alpha(fenetre)
enemy_left_right = pygame.transform.scale(enemy_left_right, FIGURE_SIZE)

imgDecor1 = pygame.image.load(path + 'Decor_1.png').convert_alpha(fenetre)
imgDecor1 = pygame.transform.scale(imgDecor1, DECOR_SIZE)

imgDecor2 = pygame.image.load(path + 'Decor_2.png').convert_alpha(fenetre)
imgDecor2 = pygame.transform.scale(imgDecor2, DECOR_SIZE)
imgDecor2b = pygame.image.load(path + 'Decor_2b.png').convert_alpha(fenetre)
imgDecor2b = pygame.transform.scale(imgDecor2b, DECOR_SIZE)
imgDecor2c = pygame.image.load(path + 'Decor_2c.png').convert_alpha(fenetre)
imgDecor2c = pygame.transform.scale(imgDecor2c, DECOR_SIZE)
imgDecor2d = pygame.image.load(path + 'Decor_2d.png').convert_alpha(fenetre)
imgDecor2d = pygame.transform.scale(imgDecor2d, DECOR_SIZE)

imgDecor3 = pygame.image.load(path + 'Decor_3.png').convert_alpha(fenetre)
imgDecor3 = pygame.transform.scale(imgDecor3, DECOR_SIZE)
imgDecor3b = pygame.image.load(path + 'Decor_3b.png').convert_alpha(fenetre)
imgDecor3b = pygame.transform.scale(imgDecor3b, DECOR_SIZE)

imgShield = pygame.image.load(path + 'Bouclier.png').convert_alpha(fenetre)
imgShield = pygame.transform.scale(imgShield, SHIELD_SIZE)

imgGun = pygame.image.load(path + 'Attaque.png').convert_alpha(fenetre)
imgGun = pygame.transform.scale(imgGun, GUN_SIZE)
imgGun = pygame.transform.rotate(imgGun, -90)
imgGunEnnemy = pygame.image.load(path + 'Attaque_Ennemy.png').convert_alpha(fenetre)
imgGunEnnemy = pygame.transform.scale(imgGunEnnemy, GUN_SIZE)
imgGunEnnemy = pygame.transform.rotate(imgGunEnnemy, -90)

# Listes d'images
images_gamer = {
    'gamer_right_static': gamer_right_static,
    'gamer_right_left': gamer_right_left,
    'gamer_right_right': gamer_right_right,
    'gamer_left_static': gamer_left_static,
    'gamer_left_left': gamer_left_left,
    'gamer_left_right': gamer_left_right
}

images_enemy = {
    'enemy_right_static': enemy_right_static,
    'enemy_right_left': enemy_right_left,
    'enemy_right_right': enemy_right_right,
    'enemy_left_static': enemy_left_static,
    'enemy_left_left': enemy_left_left,
    'enemy_left_right': enemy_left_right
}

images_decor1 = {
    'decor1': imgDecor1
}
images_decor2 = {
    'decor2': imgDecor2,
    'decor2b': imgDecor2b,
    'decor2c': imgDecor2c,
    'decor2d': imgDecor2d
}
images_decor3 = {
    'decor3': imgDecor3,
    'decor3b': imgDecor3b
}

# Animations
anim_gamer_right_static = [
    ('gamer_right_static', None)
]

anim_gamer_left_static = [
    ('gamer_left_static', None)
]

anim_gamer_right = [
    ('gamer_right_static', 100),
    ('gamer_right_right', 100),
    ('gamer_right_static', 100),
    ('gamer_right_right', 100)
]

anim_gamer_left = [
    ('gamer_left_static', 100),
    ('gamer_left_left', 100),
    ('gamer_left_static', 100),
    ('gamer_left_right', 100)
]

anim_enemy_right_static = (
    ('enemy_right_static', None),
)

anim_enemy_left_static = (
    ('enemy_left_static', None),
)

anim_enemy_right = (
    ('enemy_right_static', 300),
    ('enemy_right_right', 300),
    ('enemy_right_static', 300),
    ('enemy_right_left', 300)
)

anim_enemy_left = (
    ('enemy_left_static', 300),
    ('enemy_left_left', 300),
    ('enemy_left_static', 300),
    ('enemy_left_right', 300)
)
animationsEnemy = {
    'anim_enemy_left': anim_enemy_left,
    'anim_enemy_left_static': anim_enemy_left_static,
    'anim_enemy_right': anim_enemy_right,
    'anim_enemy_right_static': anim_enemy_right_static,
}

animationsDecor1 = {'anim_decor1': (('decor1', None), ('decor1', None))}
animationsDecor2 = {'anim_decor2': (('decor2', 80), ('decor2b', 80), ('decor2c', 80), ('decor2d', 80))}
animationsDecor3 = {'anim_decor3': (('decor3', 200), ('decor3b', 200))}

# Generateurs
enemiesGenerator = new_generator('enemy', 5 * 1000, 'edge', animationsEnemy, images_enemy)
decor1Generator = new_generator('decor1', 5 * 1000, 'all', animationsDecor1, images_decor1)
decor2Generator = new_generator('decor2', 10 * 1000, 'all', animationsDecor2, images_decor2)
decor3Generator = new_generator('decor3', 10 * 1000, 'all', animationsDecor3, images_decor3)

# Jauge de vie
gaugeLife = new_gauge(pygame.Rect(GAUGE_POSITION[0], GAUGE_POSITION[1], GAUGE_SIZE[0], GAUGE_SIZE[1]), lifeGamer)

##### OBJECTS INI FIN #####


##### VARIABLES #####
temps = pygame.time.Clock()
fini = False
partie_enCours = False
mort = False
immortelle = False

##### THE MAIN WHILE #####
while not fini:
    partie_enCours = False

    mx = WINDOWS_SIZE[0] / 2
    my = WINDOWS_SIZE[1] / 2

    nb_morts = 0
    mort = False

    # Liste des entitées selon le type
    gamers = []
    enemies = []
    decors = []
    createGamer()

    draw_intro_menu(fenetre)
    traite_entrees_menu()

    while partie_enCours:

        actualTime = pygame.time.get_ticks()
        levelGamer = level()

        if not mort or immortelle:
            traite_entrees(actualTime)

        fenetre.fill(GREY)

        # Déplacement
        for enemy in enemies:
            move_ennemy(enemy, actualTime)

        move_gamer(gamers[0], actualTime)

        auto_attack(enemies, gamers[0], actualTime)
        if is_active(gamers[0]):
            collision_decors(gamers[0])

        generate(enemiesGenerator, levelGamer, actualTime)
        generate(decor1Generator, levelGamer, actualTime)
        generate(decor2Generator, levelGamer, actualTime)
        generate(decor3Generator, levelGamer, actualTime)

        draw_all(actualTime)
        show_gauge(gaugeLife, fenetre)
        draw_level(fenetre)

        if get_life(gamers[0]) <= 0 and not immortelle:
            mort = True

        if immortelle:
            active(gamers[0])

        if mort and not immortelle:
            draw_final_menu(fenetre)
            traite_entrees_menu()

        pygame.display.flip()
        temps.tick(100)

    pygame.display.flip()
    temps.tick(100)

pygame.display.quit()
pygame.quit()
exit()
