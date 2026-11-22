import random
import unittest

from morpion.__main__ import jouer
from morpion.ia import coup_difficile, coup_facile
from morpion.plateau import Plateau


def plateau_depuis(coups):
    p = Plateau()
    for c in coups:
        p.jouer(c)
    return p


class TestPlateau(unittest.TestCase):
    def test_alternance_des_joueurs(self):
        p = plateau_depuis([1, 5])
        self.assertEqual(p.cases[0], "X")
        self.assertEqual(p.cases[4], "O")
        self.assertEqual(p.trait, "X")

    def test_case_prise_ou_invalide(self):
        p = plateau_depuis([1])
        for mauvaise in (1, 0, 10):
            with self.assertRaises(ValueError):
                p.jouer(mauvaise)
        self.assertEqual(p.trait, "O")

    def test_victoire_ligne_colonne_diagonale(self):
        self.assertEqual(plateau_depuis([1, 4, 2, 5, 3]).gagnant, "X")
        self.assertEqual(plateau_depuis([1, 2, 4, 3, 7]).gagnant, "X")
        self.assertEqual(plateau_depuis([2, 1, 3, 5, 4, 9]).gagnant, "O")

    def test_match_nul(self):
        p = plateau_depuis([1, 2, 3, 5, 4, 6, 8, 7, 9])
        self.assertTrue(p.nul)
        self.assertIsNone(p.gagnant)
        with self.assertRaises(RuntimeError):
            p.jouer(1)

    def test_affichage(self):
        texte = str(plateau_depuis([5]))
        self.assertIn(" 4 | X | 6", texte)


class TestIA(unittest.TestCase):
    def test_facile_joue_une_case_libre(self):
        p = plateau_depuis([1, 2, 3])
        self.assertIn(coup_facile(p, random.Random(0)), p.coups_libres())

    def test_difficile_gagne_quand_possible(self):
        # X : 1, 2 ; O : 4, 5 ; au tour de X -> doit jouer 3
        self.assertEqual(coup_difficile(plateau_depuis([1, 4, 2, 5])), 3)

    def test_difficile_bloque(self):
        # X : 1, 2 ; O : 5 ; au tour de O -> doit bloquer en 3
        self.assertEqual(coup_difficile(plateau_depuis([1, 5, 2])), 3)

    def test_difficile_ne_perd_jamais(self):
        rng = random.Random(42)
        for _ in range(5):
            p = Plateau()
            while not p.terminee:
                coup = coup_facile(p, rng) if p.trait == "X" else coup_difficile(p)
                p.jouer(coup)
            self.assertNotEqual(p.gagnant, "X")


class TestBoucle(unittest.TestCase):
    def jouer_avec(self, saisies, **kwargs):
        it = iter(saisies)
        sorties = []

        def entree(_):
            try:
                return next(it)
            except StopIteration:
                raise EOFError

        return jouer(entree=entree, sortie=sorties.append, **kwargs), sorties

    def test_deux_joueurs(self):
        gagnant, sorties = self.jouer_avec(["1", "4", "abc", "1", "2", "5", "3"])
        self.assertEqual(gagnant, "X")
        self.assertTrue(any("numéro de case" in s for s in sorties))
        self.assertTrue(any("déjà prise" in s for s in sorties))
        self.assertEqual(sorties[-1], "X a gagné !")

    def test_contre_ia(self):
        p = plateau_depuis([1, 5, 2])  # au tour de O : l'ordinateur bloque en 3
        gagnant, sorties = self.jouer_avec([], plateau=p, ia="O")
        self.assertIn("L'ordinateur (O) joue en 3.", sorties)
        self.assertIsNone(gagnant)


if __name__ == "__main__":
    unittest.main()
