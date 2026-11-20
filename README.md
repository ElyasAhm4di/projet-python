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

## Tests

```bash
python -m unittest -v
```
