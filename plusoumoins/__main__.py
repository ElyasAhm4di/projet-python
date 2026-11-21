"""Point d'entrée : python -m plusoumoins [--niveau NIVEAU]"""

import argparse

from .jeu import MOINS, NIVEAUX, PLUS, Partie

MESSAGES = {PLUS: "C'est plus !", MOINS: "C'est moins !"}


def jouer(partie, entree=input, sortie=print):
    sortie(f"J'ai choisi un nombre entre 1 et {partie.maximum}. "
           f"Tu as {partie.essais_max} essais.")
    while not partie.terminee:
        try:
            texte = entree(f"[{partie.restants} essai(s) restant(s)] Ton nombre : ")
        except EOFError:
            sortie("\nPartie abandonnée.")
            return False
        try:
            resultat = partie.proposer(int(texte))
        except ValueError as e:
            message = str(e)
            if "invalid literal" in message:
                message = "Ce n'est pas un nombre entier"
            sortie(f"⚠ {message}")
            continue
        if resultat in MESSAGES:
            sortie(MESSAGES[resultat])

    if partie.gagnee:
        sortie(f"Bravo ! Trouvé en {partie.essais} essai(s).")
    else:
        sortie(f"Perdu ! Le nombre était {partie.secret}.")
    return partie.gagnee


def main(argv=None):
    p = argparse.ArgumentParser(prog="plusoumoins", description="Jeu du plus ou moins")
    p.add_argument("--niveau", choices=NIVEAUX, default="moyen",
                   help="difficulté (défaut : moyen)")
    args = p.parse_args(argv)
    jouer(Partie.depuis_niveau(args.niveau))


if __name__ == "__main__":
    main()
