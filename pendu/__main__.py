"""Point d'entrée : python -m pendu [--mot MOT]"""

import argparse

from .dessin import dessiner
from .jeu import Partie
from .mots import tirer_mot


def jouer(partie, entree=input, sortie=print):
    while not partie.terminee:
        sortie(dessiner(partie.erreurs))
        sortie(f"Mot : {partie.masque}")
        if partie.lettres_fausses:
            sortie("Lettres fausses : " + ", ".join(partie.lettres_fausses))
        try:
            lettre = entree("Ta lettre : ")
        except EOFError:
            sortie("\nPartie abandonnée.")
            return False
        try:
            ok = partie.proposer(lettre)
        except ValueError as e:
            sortie(f"⚠ {e}")
            continue
        sortie("Bien vu !" if ok else "Raté...")

    sortie(dessiner(partie.erreurs))
    if partie.gagnee:
        sortie(f"Gagné ! Le mot était « {partie.mot} » ({partie.erreurs} erreur(s)).")
    else:
        sortie(f"Perdu... Le mot était « {partie.mot} ».")
    return partie.gagnee


def main(argv=None):
    p = argparse.ArgumentParser(prog="pendu", description="Jeu du pendu")
    p.add_argument("--mot", help="imposer le mot à deviner (pour jouer à deux)")
    args = p.parse_args(argv)
    try:
        partie = Partie(args.mot or tirer_mot())
    except ValueError as e:
        p.error(str(e))
    jouer(partie)


if __name__ == "__main__":
    main()
