"""Opérations sur la liste des tâches."""

from datetime import date

from .modele import PRIORITES, Stockage, Tache


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

    def ajouter(self, titre, priorite="normale", echeance=None):
        titre = titre.strip()
        if not titre:
            raise ValueError("Le titre ne peut pas être vide")
        if priorite not in PRIORITES:
            raise ValueError(f"Priorité invalide : {priorite}")
        if echeance is not None:
            try:
                echeance = date.fromisoformat(echeance).isoformat()
            except ValueError:
                raise ValueError(f"Date invalide (format AAAA-MM-JJ) : {echeance}")
        tache = Tache(id=self._prochain_id(), titre=titre, priorite=priorite,
                      echeance=echeance)
        self.taches.append(tache)
        self.stockage.sauvegarder(self.taches)
        return tache

    def lister(self, statut=None):
        """statut : None (toutes), "a_faire" ou "faites"."""
        if statut == "a_faire":
            return [t for t in self.taches if not t.terminee]
        if statut == "faites":
            return [t for t in self.taches if t.terminee]
        return list(self.taches)

    def en_retard(self, aujourd_hui=None):
        jour = (aujourd_hui or date.today()).isoformat()
        return [t for t in self.taches
                if not t.terminee and t.echeance and t.echeance < jour]

    def terminer(self, id_tache):
        tache = self._trouver(id_tache)
        tache.terminee = True
        self.stockage.sauvegarder(self.taches)
        return tache

    def renommer(self, id_tache, nouveau_titre):
        nouveau_titre = nouveau_titre.strip()
        if not nouveau_titre:
            raise ValueError("Le titre ne peut pas être vide")
        tache = self._trouver(id_tache)
        tache.titre = nouveau_titre
        self.stockage.sauvegarder(self.taches)
        return tache

    def supprimer(self, id_tache):
        tache = self._trouver(id_tache)
        self.taches.remove(tache)
        self.stockage.sauvegarder(self.taches)
        return tache

    def nettoyer(self):
        """Supprime les tâches terminées et renvoie combien ont été retirées."""
        avant = len(self.taches)
        self.taches = [t for t in self.taches if not t.terminee]
        self.stockage.sauvegarder(self.taches)
        return avant - len(self.taches)

    def stats(self):
        total = len(self.taches)
        faites = sum(t.terminee for t in self.taches)
        pourcent = round(100 * faites / total) if total else 0
        return {"total": total, "terminees": faites, "restantes": total - faites,
                "pourcentage": pourcent}
