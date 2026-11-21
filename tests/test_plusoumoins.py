import random
import unittest

from plusoumoins.__main__ import jouer
from plusoumoins.jeu import MOINS, NIVEAUX, PLUS, TROUVE, Partie


class TestPartie(unittest.TestCase):
    def test_indices(self):
        p = Partie(100, 7, secret=42)
        self.assertEqual(p.proposer(10), PLUS)
        self.assertEqual(p.proposer(90), MOINS)
        self.assertEqual(p.proposer(42), TROUVE)
        self.assertTrue(p.gagnee)
        self.assertEqual(p.essais, 3)

    def test_defaite_apres_tous_les_essais(self):
        p = Partie(10, 2, secret=5)
        p.proposer(1)
        p.proposer(2)
        self.assertTrue(p.terminee)
        self.assertFalse(p.gagnee)
        with self.assertRaises(RuntimeError):
            p.proposer(5)

    def test_hors_bornes_ne_compte_pas(self):
        p = Partie(10, 3, secret=5)
        for n in (0, 11):
            with self.assertRaises(ValueError):
                p.proposer(n)
        self.assertEqual(p.restants, 3)

    def test_secret_aleatoire_dans_les_bornes(self):
        rng = random.Random(1)
        for _ in range(50):
            self.assertTrue(1 <= Partie(20, 5, rng=rng).secret <= 20)

    def test_parametres_invalides(self):
        with self.assertRaises(ValueError):
            Partie(0, 5)
        with self.assertRaises(ValueError):
            Partie(10, 5, secret=11)

    def test_niveaux(self):
        for nom, (maximum, essais) in NIVEAUX.items():
            p = Partie.depuis_niveau(nom, secret=1)
            self.assertEqual((p.maximum, p.essais_max), (maximum, essais))


class TestBoucle(unittest.TestCase):
    def jouer_avec(self, partie, saisies):
        it = iter(saisies)
        sorties = []

        def entree(_):
            try:
                return next(it)
            except StopIteration:
                raise EOFError

        return jouer(partie, entree, sorties.append), sorties

    def test_victoire(self):
        gagne, sorties = self.jouer_avec(Partie(100, 7, secret=30), ["50", "30"])
        self.assertTrue(gagne)
        self.assertIn("C'est moins !", sorties)
        self.assertIn("2 essai(s)", sorties[-1])

    def test_saisie_invalide_puis_defaite(self):
        gagne, sorties = self.jouer_avec(Partie(10, 1, secret=3), ["abc", "7"])
        self.assertFalse(gagne)
        self.assertTrue(any("pas un nombre" in s for s in sorties))
        self.assertIn("était 3", sorties[-1])

    def test_abandon(self):
        gagne, sorties = self.jouer_avec(Partie(10, 3, secret=3), [])
        self.assertFalse(gagne)
        self.assertIn("abandonnée", sorties[-1])


if __name__ == "__main__":
    unittest.main()
