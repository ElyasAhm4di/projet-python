import random
import unittest

from pendu.__main__ import jouer
from pendu.dessin import ETAPES, dessiner
from pendu.jeu import Partie
from pendu.mots import MOTS, tirer_mot


class TestPartie(unittest.TestCase):
    def test_masque_initial(self):
        self.assertEqual(Partie("chat").masque, "_ _ _ _")

    def test_bonne_lettre_revele_toutes_les_occurrences(self):
        p = Partie("examen")
        self.assertTrue(p.proposer("E"))
        self.assertEqual(p.masque, "e _ _ _ e _")
        self.assertEqual(p.erreurs, 0)

    def test_mauvaise_lettre_compte_une_erreur(self):
        p = Partie("chat")
        self.assertFalse(p.proposer("z"))
        self.assertEqual(p.erreurs, 1)
        self.assertEqual(p.lettres_fausses, ["z"])

    def test_lettre_deja_proposee(self):
        p = Partie("chat")
        p.proposer("z")
        with self.assertRaises(ValueError):
            p.proposer("z")
        self.assertEqual(p.erreurs, 1)

    def test_proposition_invalide(self):
        p = Partie("chat")
        for mauvais in ("", "ab", "3", "!"):
            with self.assertRaises(ValueError):
                p.proposer(mauvais)

    def test_mot_invalide(self):
        with self.assertRaises(ValueError):
            Partie("deux mots")

    def test_victoire(self):
        p = Partie("ici")
        p.proposer("i")
        p.proposer("c")
        self.assertTrue(p.gagnee)
        self.assertTrue(p.terminee)

    def test_defaite(self):
        p = Partie("a", erreurs_max=2)
        p.proposer("b")
        p.proposer("c")
        self.assertTrue(p.perdue)
        with self.assertRaises(RuntimeError):
            p.proposer("a")


class TestDessinEtMots(unittest.TestCase):
    def test_un_dessin_par_erreur(self):
        self.assertEqual(len(ETAPES), 7)
        for i in range(7):
            self.assertIn("+---+", dessiner(i))
        self.assertIn("/ \\", dessiner(6))

    def test_tirer_mot(self):
        self.assertIn(tirer_mot(rng=random.Random(0)), MOTS)
        self.assertEqual(tirer_mot(["Bonjour"]), "bonjour")


class TestBoucle(unittest.TestCase):
    def jouer_avec(self, mot, lettres):
        entrees = iter(lettres)
        sorties = []

        def entree(_):
            try:
                return next(entrees)
            except StopIteration:
                raise EOFError

        return jouer(Partie(mot), entree, sorties.append), sorties

    def test_partie_gagnee(self):
        gagne, sorties = self.jouer_avec("oui", ["x", "o", "o", "u", "i"])
        self.assertTrue(gagne)
        self.assertTrue(any("déjà proposée" in s for s in sorties))
        self.assertIn("Gagné", sorties[-1])

    def test_partie_perdue(self):
        gagne, sorties = self.jouer_avec("a", list("bcdefg"))
        self.assertFalse(gagne)
        self.assertIn("Perdu", sorties[-1])

    def test_abandon(self):
        gagne, sorties = self.jouer_avec("chat", [])
        self.assertFalse(gagne)
        self.assertIn("abandonnée", sorties[-1])


if __name__ == "__main__":
    unittest.main()
