"""Point d'entrée : python -m taches <commande> ..."""

import argparse
import sys

from .gestion import Gestionnaire


def construire_parser():
    p = argparse.ArgumentParser(prog="taches", description="Gestionnaire de tâches")
    sous = p.add_subparsers(dest="commande", required=True)

    a = sous.add_parser("ajouter", help="ajouter une tâche")
    a.add_argument("titre")

    sous.add_parser("lister", help="afficher les tâches")
    sous.add_parser("stats", help="afficher la progression")

    for nom, aide in (("terminer", "marquer une tâche comme faite"),
                      ("supprimer", "supprimer une tâche")):
        s = sous.add_parser(nom, help=aide)
        s.add_argument("id", type=int)
    return p


def main(argv=None):
    args = construire_parser().parse_args(argv)
    g = Gestionnaire()
    try:
        if args.commande == "ajouter":
            t = g.ajouter(args.titre)
            print(f"Tâche #{t.id} ajoutée : {t.titre}")
        elif args.commande == "lister":
            if not g.taches:
                print("Aucune tâche.")
            for t in g.taches:
                case = "x" if t.terminee else " "
                print(f"[{case}] #{t.id} {t.titre}")
        elif args.commande == "stats":
            s = g.stats()
            print(f"{s['terminees']}/{s['total']} tâches terminées "
                  f"({s['pourcentage']} %), {s['restantes']} restante(s).")
        elif args.commande == "terminer":
            t = g.terminer(args.id)
            print(f"Tâche #{t.id} terminée.")
        elif args.commande == "supprimer":
            t = g.supprimer(args.id)
            print(f"Tâche #{t.id} supprimée.")
    except (KeyError, ValueError) as e:
        print(f"Erreur : {e.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
