import tempfile
import unittest
from datetime import date
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

    def test_priorite_par_defaut(self):
        self.assertEqual(self.g.ajouter("A").priorite, "normale")

    def test_priorite_haute(self):
        self.assertEqual(self.g.ajouter("A", "haute").priorite, "haute")

    def test_priorite_invalide(self):
        with self.assertRaises(ValueError):
            self.g.ajouter("A", "urgente")

    def test_lister_filtres(self):
        self.g.ajouter("A")
        b = self.g.ajouter("B")
        self.g.terminer(b.id)
        self.assertEqual([t.titre for t in self.g.lister()], ["A", "B"])
        self.assertEqual([t.titre for t in self.g.lister("a_faire")], ["A"])
        self.assertEqual([t.titre for t in self.g.lister("faites")], ["B"])

    def test_renommer(self):
        t = self.g.ajouter("A")
        self.g.renommer(t.id, "  Nouveau titre ")
        self.assertEqual(self.g.taches[0].titre, "Nouveau titre")

    def test_renommer_titre_vide(self):
        t = self.g.ajouter("A")
        with self.assertRaises(ValueError):
            self.g.renommer(t.id, "")

    def test_echeance_invalide(self):
        with self.assertRaises(ValueError):
            self.g.ajouter("A", echeance="31/12/2026")

    def test_en_retard(self):
        self.g.ajouter("Passée", echeance="2026-01-01")
        self.g.ajouter("Future", echeance="2027-01-01")
        self.g.ajouter("Sans date")
        faite = self.g.ajouter("Passée mais faite", echeance="2026-01-01")
        self.g.terminer(faite.id)
        retard = self.g.en_retard(aujourd_hui=date(2026, 6, 1))
        self.assertEqual([t.titre for t in retard], ["Passée"])


if __name__ == "__main__":
    unittest.main()
