"""Dessins ASCII du pendu, un par nombre d'erreurs (0 à 6)."""

ETAPES = [
    "",
    " O",
    " O\n |",
    " O\n/|",
    " O\n/|\\",
    " O\n/|\\\n/",
    " O\n/|\\\n/ \\",
]


def dessiner(erreurs):
    corps = ETAPES[min(erreurs, len(ETAPES) - 1)].split("\n")
    corps += [""] * (3 - len(corps))
    lignes = ["  +---+", "  |   |"]
    lignes += [f"  |  {c}" for c in corps]
    lignes += ["  |", "=====\n"]
    return "\n".join(l.rstrip() for l in lignes)
