"""Point d'entrée : python -m morpion [--contre-ia] [--niveau NIVEAU] [--commencer]"""

import argparse

from .ia import choisir_coup
from .plateau import Plateau


def jouer(plateau=None, ia=None, niveau="difficile", entree=input, sortie=print):
    """Lance une partie. `ia` est le symbole joué par l'ordinateur (ou None).

    Renvoie le gagnant ("X" ou "O") ou None en cas de match nul / abandon.
    """
    plateau = plateau or Plateau()
    while not plateau.terminee:
        sortie(f"\n{plateau}\n")
        if plateau.trait == ia:
            case = choisir_coup(plateau, niveau)
            sortie(f"L'ordinateur ({ia}) joue en {case}.")
            plateau.jouer(case)
            continue
        try:
            texte = entree(f"Joueur {plateau.trait}, ta case (1-9) : ")
        except EOFError:
            sortie("\nPartie abandonnée.")
            return None
        try:
            plateau.jouer(int(texte))
        except ValueError as e:
            message = str(e)
            if "invalid literal" in message:
                message = "Tape un numéro de case"
            sortie(f"⚠ {message}")

    sortie(f"\n{plateau}\n")
    if plateau.gagnant:
        sortie(f"{plateau.gagnant} a gagné !")
    else:
        sortie("Match nul !")
    return plateau.gagnant


def main(argv=None):
    p = argparse.ArgumentParser(prog="morpion", description="Jeu du morpion")
    p.add_argument("--contre-ia", action="store_true", help="jouer contre l'ordinateur")
    p.add_argument("--niveau", choices=("facile", "difficile"), default="difficile",
                   help="niveau de l'ordinateur (défaut : difficile)")
    p.add_argument("--commencer", action="store_true",
                   help="contre l'ordinateur : jouer en premier (X)")
    args = p.parse_args(argv)
    ia = None
    if args.contre_ia:
        ia = "O" if args.commencer else "X"
    jouer(ia=ia, niveau=args.niveau)


if __name__ == "__main__":
    main()
