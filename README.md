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

## Tests

```bash
python -m unittest -v
```
