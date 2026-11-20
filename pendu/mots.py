"""Liste des mots à deviner et tirage au hasard."""

import random

MOTS = [
    "python", "variable", "fonction", "boucle", "liste", "dictionnaire",
    "classe", "objet", "module", "exception", "algorithme", "terminal",
    "clavier", "ordinateur", "programme", "fichier", "universite",
    "etudiant", "examen", "bibliotheque", "cafeteria", "partiel",
]


def tirer_mot(mots=None, rng=random):
    """Renvoie un mot choisi au hasard (en minuscules)."""
    mots = mots or MOTS
    return rng.choice(mots).lower()
