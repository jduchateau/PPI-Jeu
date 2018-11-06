import pygame
import math
print(math.exp(1))
############ STATIC VARIABLES ############
FENETRE_HAUTEUR = 700
FENETRE_LARGEUR = 900
GREY = (198,186,183)
BLACK_PERS = (52, 51, 50)
BOUTON_SOURIS_GAUCHE = 1
####VITESSE
VITESSE_MAX = 10
VITESSE_MIN = 5
DIST_MAX = 200
############ FONCTIONC ############
#### ENTITE
def nouvelle_entite():
	return{
		'visible':True,
		'position':[0, 0],
		'size':[0, 0],
		'color':None,
		'actualImg':None
	}
def visible(entite):
	entite['visible'] = True

def invisible(entite):
	entite['visbile'] = False

def place(entite, x, y):
	entite['position'][0] = x
	entite['position'][1] = y
def set_size(entite, w, h):
	entite['size'][0] = w
	entite['size'][1] = h

def set_color(entite, c):
	entite['color'] = c

def dessine(ecran, entite, number):
	#ecran.bilt(entite['actualImg'], entite['position'])
	if(number == 0):
		pygame.draw.rect(ecran, entite['color'], (entite['position'], entite['size']))
	elif(number == 1):
		pygame.draw.circle(ecran, entite['color'], entite['position'], entite['size'][0]//2)

def vitesse(entite,v, m, axe):
	######## on utilise la fonction sigmoide pour calculer la vitesse
	dist_min = entite['size'][0] //2
	dist = abs((entite['position'][axe] + entite['size'][axe]//2)  - m)
	if(dist >= dist_min and dist <= DIST_MAX):
		# v = k*entite['position'][axe] + t
		v = int(1/(1 + math.exp(-(dist*6/DIST_MAX))) * VITESSE_MAX)
	elif(dist > DIST_MAX):
		v = VITESSE_MAX
	else:
		if((entite['position'][axe] + entite['size'][axe]//2) != m):
			v = 1
		else:
			v = 0
	return v;
	
def move_pers(entite, vx, vy):
	global mx, my
	## verifie vitese (  compare si la x > ou < xmouse et si y > ou < que ymouse) et modifier la vitesse
	vx = vitesse(entite, vx, mx, 0)
	vy = vitesse(entite, vy, my, 1)

	if((entite['position'][0] + entite['size'][0]//2)  > mx ):
		if(vx > 0):
			vx *=-1
	elif((entite['position'][0] + entite['size'][0]//2) < mx ):
		if(vx < 0):
			vx *=-1
	if((entite['position'][1] + entite['size'][1]//2) > my ):
		if(vy > 0):
			vy *=-1
	elif((entite['position'][1] + entite['size'][1]//2) < my ):
		if(vy < 0):
			vy *=-1
	## verifie vitese fin
	
	if((entite['position'][0] + entite['size'][0]//2) != mx ):
		entite['position'][0] += vx
	if((entite['position'][1] + entite['size'][1]//2) != my ):
		entite['position'][1] += vy
	#print(" dx: ", diff_vx)
#### FIN ENTITE
def traite_entrees():
    global fini, mouse_clicked, mx, my
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == BOUTON_SOURIS_GAUCHE:
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
pers_location = ((FENETRE_LARGEUR//2 - pers_size[0]//2), (FENETRE_HAUTEUR//2- pers_size[1]//2))
pers = nouvelle_entite()
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
fini = False;

############ THE MAIN WHILE ############
while not fini :
	traite_entrees()
	fenetre.fill(GREY)
	draw()
	if(mouse_clicked == True):
		move_pers(pers, 3, 3)
	pygame.display.flip()
	temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()