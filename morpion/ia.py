"""Adversaire ordinateur.

- facile : joue une case libre au hasard ;
- difficile : algorithme minimax, ne perd jamais.
"""

import random


def coup_facile(plateau, rng=random):
    return rng.choice(plateau.coups_libres())


def _minimax(plateau, moi):
    """Score du plateau pour `moi` : positif si gagné, 0 si nul, négatif si perdu."""
    if plateau.gagnant is not None:
        # le nombre de cases vides favorise les victoires rapides
        bonus = 1 + plateau.cases.count(" ")
        return bonus if plateau.gagnant == moi else -bonus
    if plateau.nul:
        return 0
    scores = []
    for case in plateau.coups_libres():
        suivant = plateau.copie()
        suivant.jouer(case)
        scores.append(_minimax(suivant, moi))
    return max(scores) if plateau.trait == moi else min(scores)


def coup_difficile(plateau):
    moi = plateau.trait
    meilleur, meilleur_score = None, None
    for case in plateau.coups_libres():
        suivant = plateau.copie()
        suivant.jouer(case)
        score = _minimax(suivant, moi)
        if meilleur_score is None or score > meilleur_score:
            meilleur, meilleur_score = case, score
    return meilleur


def choisir_coup(plateau, niveau="difficile", rng=random):
    if niveau == "facile":
        return coup_facile(plateau, rng)
    return coup_difficile(plateau)
