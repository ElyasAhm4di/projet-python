"""Grille 3x3, coups joués et détection de la fin de partie.

Les cases sont numérotées de 1 à 9, comme un pavé numérique de téléphone :

    1 | 2 | 3
    4 | 5 | 6
    7 | 8 | 9
"""

VIDE = " "
JOUEURS = ("X", "O")
LIGNES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
    (0, 4, 8), (2, 4, 6),             # diagonales
]


class Plateau:
    def __init__(self):
        self.cases = [VIDE] * 9
        self.trait = "X"  # joueur dont c'est le tour

    def copie(self):
        p = Plateau()
        p.cases = self.cases[:]
        p.trait = self.trait
        return p

    def coups_libres(self):
        return [i + 1 for i, c in enumerate(self.cases) if c == VIDE]

    def jouer(self, case):
        """Place le symbole du joueur courant sur la case (1 à 9)."""
        if self.terminee:
            raise RuntimeError("La partie est terminée")
        if not 1 <= case <= 9:
            raise ValueError("Choisis une case entre 1 et 9")
        if self.cases[case - 1] != VIDE:
            raise ValueError(f"La case {case} est déjà prise")
        self.cases[case - 1] = self.trait
        self.trait = "O" if self.trait == "X" else "X"

    @property
    def gagnant(self):
        for a, b, c in LIGNES:
            if self.cases[a] != VIDE and self.cases[a] == self.cases[b] == self.cases[c]:
                return self.cases[a]
        return None

    @property
    def nul(self):
        return self.gagnant is None and VIDE not in self.cases

    @property
    def terminee(self):
        return self.gagnant is not None or self.nul

    def __str__(self):
        c = [v if v != VIDE else str(i + 1) for i, v in enumerate(self.cases)]
        lignes = [f" {c[i]} | {c[i + 1]} | {c[i + 2]}" for i in (0, 3, 6)]
        return "\n---+---+---\n".join(lignes)
