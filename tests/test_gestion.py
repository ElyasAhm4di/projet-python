import tempfile
import unittest
from pathlib import Path

from taches.gestion import Gestionnaire
from taches.modele import Stockage


class TestGestionnaire(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.chemin = Path(self.dossier.name) / "taches.json"
        self.g = Gestionnaire(Stockage(self.chemin))

    def tearDown(self):
        self.dossier.cleanup()

    def test_ajouter_attribue_des_id_croissants(self):
        self.assertEqual(self.g.ajouter("A").id, 1)
        self.assertEqual(self.g.ajouter("B").id, 2)

    def test_titre_vide_refuse(self):
        with self.assertRaises(ValueError):
            self.g.ajouter("   ")

    def test_terminer(self):
        t = self.g.ajouter("A")
        self.g.terminer(t.id)
        self.assertTrue(self.g.taches[0].terminee)

    def test_supprimer(self):
        t = self.g.ajouter("A")
        self.g.supprimer(t.id)
        self.assertEqual(self.g.taches, [])

    def test_id_inconnu(self):
        with self.assertRaises(KeyError):
            self.g.terminer(42)

    def test_persistance(self):
        self.g.ajouter("A")
        recharge = Gestionnaire(Stockage(self.chemin))
        self.assertEqual(recharge.taches[0].titre, "A")

    def test_stats(self):
        self.g.ajouter("A")
        t = self.g.ajouter("B")
        self.g.terminer(t.id)
        self.assertEqual(self.g.stats(),
                         {"total": 2, "terminees": 1, "restantes": 1, "pourcentage": 50})

    def test_stats_liste_vide(self):
        self.assertEqual(self.g.stats()["pourcentage"], 0)


if __name__ == "__main__":
    unittest.main()
