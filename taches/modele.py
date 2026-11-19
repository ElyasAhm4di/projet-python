"""Modèle de données et stockage JSON des tâches."""

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path


PRIORITES = ("basse", "normale", "haute")


@dataclass
class Tache:
    id: int
    titre: str
    terminee: bool = False
    priorite: str = "normale"
    creee_le: str = field(default_factory=lambda: date.today().isoformat())


class Stockage:
    """Lit et écrit la liste des tâches dans un fichier JSON."""

    def __init__(self, chemin="taches.json"):
        self.chemin = Path(chemin)

    def charger(self):
        if not self.chemin.exists():
            return []
        with self.chemin.open(encoding="utf-8") as f:
            return [Tache(**d) for d in json.load(f)]

    def sauvegarder(self, taches):
        with self.chemin.open("w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in taches], f, ensure_ascii=False, indent=2)
