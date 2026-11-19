"""Point d'entrée : python -m taches <commande> ..."""

import argparse
import sys

from .gestion import Gestionnaire
from .modele import PRIORITES


def construire_parser():
    p = argparse.ArgumentParser(prog="taches", description="Gestionnaire de tâches")
    sous = p.add_subparsers(dest="commande", required=True)

    a = sous.add_parser("ajouter", help="ajouter une tâche")
    a.add_argument("titre")
    a.add_argument("-p", "--priorite", choices=PRIORITES, default="normale")
    a.add_argument("-e", "--echeance", metavar="AAAA-MM-JJ")

    li = sous.add_parser("lister", help="afficher les tâches")
    filtre = li.add_mutually_exclusive_group()
    filtre.add_argument("--a-faire", dest="statut", action="store_const", const="a_faire")
    filtre.add_argument("--faites", dest="statut", action="store_const", const="faites")
    sous.add_parser("stats", help="afficher la progression")

    for nom, aide in (("terminer", "marquer une tâche comme faite"),
                      ("supprimer", "supprimer une tâche")):
        s = sous.add_parser(nom, help=aide)
        s.add_argument("id", type=int)
    r = sous.add_parser("renommer", help="changer le titre d'une tâche")
    r.add_argument("id", type=int)
    r.add_argument("titre")
    return p


def main(argv=None):
    args = construire_parser().parse_args(argv)
    g = Gestionnaire()
    try:
        if args.commande == "ajouter":
            t = g.ajouter(args.titre, args.priorite, args.echeance)
            print(f"Tâche #{t.id} ajoutée : {t.titre}")
        elif args.commande == "lister":
            taches = g.lister(args.statut)
            retard = {t.id for t in g.en_retard()}
            if not taches:
                print("Aucune tâche.")
            for t in taches:
                case = "x" if t.terminee else " "
                marque = " (!)" if t.priorite == "haute" else ""
                if t.echeance:
                    marque += f" — pour le {t.echeance}"
                if t.id in retard:
                    marque += " EN RETARD"
                print(f"[{case}] #{t.id} {t.titre}{marque}")
        elif args.commande == "stats":
            s = g.stats()
            print(f"{s['terminees']}/{s['total']} tâches terminées "
                  f"({s['pourcentage']} %), {s['restantes']} restante(s).")
        elif args.commande == "terminer":
            t = g.terminer(args.id)
            print(f"Tâche #{t.id} terminée.")
        elif args.commande == "renommer":
            t = g.renommer(args.id, args.titre)
            print(f"Tâche #{t.id} renommée : {t.titre}")
        elif args.commande == "supprimer":
            t = g.supprimer(args.id)
            print(f"Tâche #{t.id} supprimée.")
    except (KeyError, ValueError) as e:
        print(f"Erreur : {e.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
