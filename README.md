# Gestionnaire de tâches

Petit gestionnaire de tâches en ligne de commande écrit en Python (aucune dépendance externe).
Les tâches sont enregistrées dans `taches.json`, dans le dossier courant.

## Utilisation

```bash
# Ajouter (priorité et échéance facultatives)
python -m taches ajouter "Réviser le cours de Python"
python -m taches ajouter "Rendre le projet" --priorite haute --echeance 2026-12-01

# Afficher
python -m taches lister
python -m taches lister --a-faire
python -m taches lister --faites

# Modifier
python -m taches terminer 1
python -m taches renommer 2 "Rendre le projet final"
python -m taches supprimer 1
python -m taches nettoyer      # supprime toutes les tâches terminées

# Progression
python -m taches stats
```

Dans `lister`, `(!)` signale une priorité haute et `EN RETARD` une tâche non terminée
dont l'échéance est dépassée.

## Tests

```bash
python -m unittest -v
```
