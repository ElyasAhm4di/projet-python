# Hazine Avcısı : chasse au trésor en console

Un petit jeu en Python, dans le terminal. On explore une grille à la recherche de trésors, sans tomber sur trop de pièges. L'interface est en turc (« Hazine Avcısı » veut dire « chasseur de trésor »).

## Comment ça se joue

On choisit la taille de la carte, de 10×10 à 20×20. Le jeu y place au hasard des pièges (20 % des cases) et des trésors (15 % des cases) :

- trésor **petit** (`s`) : 1 point, la moitié des trésors ;
- trésor **moyen** (`o`) : 3 points, 30 % des trésors ;
- trésor **grand** (`b`) : 5 points, 20 % des trésors.

À chaque tour on indique une ligne et une colonne pour ouvrir une case. Un trésor rapporte ses points. Un piège (`X`) coûte une vie sur les trois. Une case vide affiche le nombre de pièges (`T`) et de trésors (`H`) dans les huit cases voisines, ce qui permet de déduire où creuser ensuite.

La partie s'arrête quand on a trouvé tous les trésors ou perdu ses trois vies. Le score final est `points - 2 × vies perdues`. On peut ensuite rejouer.

Au début, deux modes : le mode ouvert montre toute la carte (pratique pour tester), le mode caché la masque derrière des `?`.

## Lancer

Il faut Python 3 et aucune bibliothèque externe.

```bash
python src/hazine_avcisi/main.py
```

## Les tests

```bash
python tests/test_regles.py
```

Il vérifie trois choses : les proportions de pièges et de trésors pour les tailles 10, 15 et 20, le comptage des voisins sur une petite grille de contrôle, et la formule du score.

Limite à connaître : ce test recalcule ces règles de son côté, il n'importe pas `main.py`, parce que le jeu s'exécute dès qu'on charge le fichier. Il confirme donc que les règles sont cohérentes, pas que le jeu les applique sans erreur. Pour le tester vraiment, il faudrait d'abord ranger la logique de `main.py` dans des fonctions.

## État du code

Le jeu fonctionne, mais le code est écrit « à plat » : une grande boucle, des noms de variables en turc et beaucoup de répétitions (les trois types de trésors sont placés par trois boucles presque identiques). Un découpage en fonctions (création de la carte, ouverture d'une case, calcul du score) est la prochaine étape logique, et elle rendrait le test plus utile.

## Organisation

```
src/hazine_avcisi/main.py   le jeu
tests/test_regles.py        vérification des règles
```
