"""Logique du jeu, indépendante des entrées/sorties."""

import random

# niveau -> (borne max, nombre d'essais)
NIVEAUX = {
    "facile": (50, 10),
    "moyen": (100, 7),
    "difficile": (1000, 10),
}

PLUS, MOINS, TROUVE = "plus", "moins", "trouvé"


class Partie:
    def __init__(self, maximum=100, essais_max=7, secret=None, rng=random):
        if maximum < 1 or essais_max < 1:
            raise ValueError("Le maximum et le nombre d'essais doivent être positifs")
        self.maximum = maximum
        self.essais_max = essais_max
        self.secret = secret if secret is not None else rng.randint(1, maximum)
        if not 1 <= self.secret <= maximum:
            raise ValueError("Le nombre secret est hors des bornes")
        self.historique = []

    @classmethod
    def depuis_niveau(cls, niveau, **kwargs):
        maximum, essais = NIVEAUX[niveau]
        return cls(maximum, essais, **kwargs)

    def proposer(self, nombre):
        """Renvoie PLUS, MOINS ou TROUVE."""
        if self.terminee:
            raise RuntimeError("La partie est terminée")
        if not 1 <= nombre <= self.maximum:
            raise ValueError(f"Choisis un nombre entre 1 et {self.maximum}")
        self.historique.append(nombre)
        if nombre < self.secret:
            return PLUS
        if nombre > self.secret:
            return MOINS
        return TROUVE

    @property
    def essais(self):
        return len(self.historique)

    @property
    def restants(self):
        return self.essais_max - self.essais

    @property
    def gagnee(self):
        return self.secret in self.historique

    @property
    def terminee(self):
        return self.gagnee or self.restants <= 0
