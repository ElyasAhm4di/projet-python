# Gestionnaire de tâches

Petit gestionnaire de tâches en ligne de commande écrit en Python (aucune dépendance externe).
Les tâches sont enregistrées dans `taches.json`, dans le dossier courant.

## Utilisation

```bash
python -m taches ajouter "Réviser le cours de Python"
python -m taches lister
python -m taches terminer 1
python -m taches supprimer 1
python -m taches stats
```

## Jeu du pendu

Le grand classique des pauses entre deux cours : deviner un mot lettre par lettre
avant que le bonhomme soit entièrement dessiné (6 erreurs maximum).

```bash
python -m pendu              # mot tiré au hasard
python -m pendu --mot examen # imposer le mot (pour jouer à deux)
```

## Jeu du plus ou moins

L'exercice incontournable des premiers TP : l'ordinateur choisit un nombre secret,
il faut le trouver en suivant les indices « plus » / « moins ».

| Niveau      | Nombres    | Essais |
|-------------|------------|--------|
| `facile`    | 1 à 50     | 10     |
| `moyen`     | 1 à 100    | 7      |
| `difficile` | 1 à 1000   | 10     |

```bash
python -m plusoumoins                      # niveau moyen
python -m plusoumoins --niveau difficile
```

## Jeu du morpion

Le tic-tac-toe des fonds d'amphi : aligner trois symboles sur une grille 3x3.
Les cases se choisissent avec leur numéro (1 en haut à gauche, 9 en bas à droite).
L'ordinateur en niveau `difficile` utilise l'algorithme minimax et ne perd jamais.

```bash
python -m morpion                                   # à deux sur le même clavier
python -m morpion --contre-ia --commencer           # contre l'ordinateur, tu joues X
python -m morpion --contre-ia --niveau facile       # ordinateur qui joue au hasard
```

## Tests

```bash
python -m unittest -v
```
