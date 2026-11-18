"""Opérations sur la liste des tâches."""

from .modele import Stockage, Tache


class Gestionnaire:
    def __init__(self, stockage=None):
        self.stockage = stockage or Stockage()
        self.taches = self.stockage.charger()

    def _prochain_id(self):
        return max((t.id for t in self.taches), default=0) + 1

    def _trouver(self, id_tache):
        for t in self.taches:
            if t.id == id_tache:
                return t
        raise KeyError(f"Aucune tâche avec l'id {id_tache}")

    def ajouter(self, titre):
        titre = titre.strip()
        if not titre:
            raise ValueError("Le titre ne peut pas être vide")
        tache = Tache(id=self._prochain_id(), titre=titre)
        self.taches.append(tache)
        self.stockage.sauvegarder(self.taches)
        return tache

    def terminer(self, id_tache):
        tache = self._trouver(id_tache)
        tache.terminee = True
        self.stockage.sauvegarder(self.taches)
        return tache

    def supprimer(self, id_tache):
        tache = self._trouver(id_tache)
        self.taches.remove(tache)
        self.stockage.sauvegarder(self.taches)
        return tache

    def stats(self):
        total = len(self.taches)
        faites = sum(t.terminee for t in self.taches)
        pourcent = round(100 * faites / total) if total else 0
        return {"total": total, "terminees": faites, "restantes": total - faites,
                "pourcentage": pourcent}
