# PPI-Jeu
Projet de jeu pour le cours INFO2056 de ULiège

## Attaque dans le Vide
(Faut trouver un meilleur titre)

### Fonctionnement

#### Déplacement
Utilise les déplacement doux, câd que l'on ne déplace pas directement le personnage mais on agmente son accélération plus la souris est loin du personnage ce qui modifie sa vitesse donc sa position.
(voir le Labo MathPys)

Ne peux jamais sortir de la zone de jeu. (facilite la création)

#### Apparition des ennemis
La position de l'apparition se fait sur un bord, et ils convergent vers le joueur.
Le nombre d'apparition dépend du hasard et du nombre d'ennemis déjà morts.

#### Apparition des décorts.
Apparaissent et dissparaissent au fur et a mesur de la partie de manière aléatoir.

Le Decor_1 n'a aucun effect sur le joueur
Le Decor_2 diminue la vie de joueur
Le Decor_3 restaure la vie de joueur

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

- nb_morts

(à complèter au fur et à mesur)

#### Arborescence
- idee : contient les croquis et fichiers de travail divers
- img : contient les images néccesaire au jeu
- Le code python sera à la racine.

## Auteurs :
Jakub Duchateau && Raul Talmacel