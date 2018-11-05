# PPI-Jeu
Projet de jeu pour le cours INFO2056 de ULiège

## Attaque dans le Vide
(Faut trouver un meilleur titre)

### Fonctionnement

#### Déplacement
Utilise les déplacement doux, câd que l'on ne déplace pas directement le personnage mais on agmente son accélération plus la souris est loin du personnage ce qui modifie sa vitesse donc sa position.
L'idée est de faire comme si le personnage vollait. Ceci nous évite d'animer ses pied et d'autres choses...
(voir le Labo MathPys)

Lorsque le personnage se déplace vers la droite on garde l'image mais lorsque il va vers la gauche il suffit de faire une transformation avec `pygame.transform.flip()`

Ne peux jamais sortir de la zone de jeu. (facilite la création, mais on pourrais après décider d'amélioer cela)

#### Apparition des ennemis
La position de l'apparition se fait sur un bord, et ils convergent vers le joueur.
Le nombre d'apparition dépend du hasard et du nombre d'ennemis déjà morts.

#### Apparition des décorts.
Apparaissent et dissparaissent au fur et a mesur de la partie de manière aléatoir.

Le Decor_1 n'a aucun effect sur le joueur
Le Decor_2 diminue la vie de joueur
Le Decor_3 restaure la vie de joueur

#### Perte de vie
Le joueur principal ne doit endurer les attaque des ennemis ou du décor 2 de la même manière

> Je ne sais pas encore comment on va gérér la vie ni les attaque
> Je vois 2 choix simple :
> - chaque entité aurait une force de frappe
> - chaque entité a une résistance aux attaque

### Varables & Constantes
- Entitées
    * type "joueur", "ennemis", "decor1", "decor2", "decor3"
    * position [x,y]
    * vitesse [x,y]
    * images [nom:image]
    * imageActuel "nom"
    * vie

- DEGRADATION_VIE
- PUISSANCE_ATTAQUE
- FORCE_FROTTEMENT

- nb_morts

(à complèter au fur et à mesur)

#### Arborescence
- idee : contient les croquis et fichiers de travail divers
- img : contient les images néccesaire au jeu
- Le code python sera à la racine.

## Auteurs :
Jakub Duchateau && Raul Talmacel