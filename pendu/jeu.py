"""Logique d'une partie de pendu (sans entrées/sorties)."""

ERREURS_MAX = 6


class Partie:
    def __init__(self, mot, erreurs_max=ERREURS_MAX):
        mot = mot.strip().lower()
        if not mot.isalpha():
            raise ValueError("Le mot doit contenir uniquement des lettres")
        self.mot = mot
        self.erreurs_max = erreurs_max
        self.proposees = set()
        self.erreurs = 0

    def proposer(self, lettre):
        """Propose une lettre. Renvoie True si elle est dans le mot."""
        lettre = lettre.strip().lower()
        if len(lettre) != 1 or not lettre.isalpha():
            raise ValueError("Propose une seule lettre")
        if lettre in self.proposees:
            raise ValueError(f"Lettre « {lettre} » déjà proposée")
        if self.terminee:
            raise RuntimeError("La partie est terminée")
        self.proposees.add(lettre)
        if lettre in self.mot:
            return True
        self.erreurs += 1
        return False

    @property
    def masque(self):
        return " ".join(c if c in self.proposees else "_" for c in self.mot)

    @property
    def gagnee(self):
        return set(self.mot) <= self.proposees

    @property
    def perdue(self):
        return self.erreurs >= self.erreurs_max

    @property
    def terminee(self):
        return self.gagnee or self.perdue

    @property
    def lettres_fausses(self):
        return sorted(self.proposees - set(self.mot))
