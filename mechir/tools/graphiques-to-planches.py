#!/usr/bin/env python

import subprocess
from pathlib import Path

import argparse

def image_ou_blanche(chemin, taille):
    """
    Retourne les arguments ImageMagick correspondant soit à une image
    existante, soit à une image blanche de substitution.

    Parameters
    ----------
    chemin : Path
        Chemin de l'image recherchée.

    taille : str
        Taille de l'image blanche (ex. "1000x600").

    Returns
    -------
    list[str]
        Arguments à insérer dans la commande ImageMagick.
    """
    if chemin.exists():
        return [str(chemin)]
    else:
        print(f"Image absente : {chemin.name}")
        return ["-size", taille, "xc:white"]

def perturbation_type(pert):
    if "->" in pert:
        return "replace"
    elif pert[0] == "+":
        return "append"
    elif pert[-1] =="+":
        return "prepend" 
    elif pert == "full_replace":
        return "full_replace"
    raise RuntimeWarning("Unreachable")


def generer_planche(
    dossier,
    sortie="planche_globale.png",
    nb_colonnes=3,
    keep_temp=False,
    pert_type = "all"
):
    """
    Génère une grande planche récapitulative.

    Chaque perturbation donne lieu à une tuile :
        - score en haut ;
        - mean et std côte à côte ;
        - meanV2 et stdV2 si disponibles.

    Parameters
    ----------
    dossier : str
        Dossier contenant les images.

    sortie : str
        Nom de l'image finale.

    nb_colonnes : int
        Nombre de tuiles par ligne dans la planche finale.
    """

    dossier = Path(dossier)

    prefix = "PerturbationScore_"

    perturbations = sorted(
        f.stem[len(prefix):]
        for f in dossier.glob(f"{prefix}*.png")
    )

    tuiles = []

    for pert in perturbations:

        if pert_type == "all" or perturbation_type(pert) == pert_type:

            score = dossier / f"PerturbationScore_{pert}.png"

            mean = dossier / f"ComponentPatching-mean_{pert}.png"
            std = dossier / f"ComponentPatching-std_{pert}.png"

            mean_v2 = dossier / f"ComponentPatching-mean_{pert}V2.png"
            std_v2 = dossier / f"ComponentPatching-std_{pert}V2.png"

            tuile = dossier / f"__tuile_{pert}.png"

            # Ligne mean/std
            cmd = [
                "magick",

                "(",
                *image_ou_blanche(mean, "1000x600"),
                "-resize", "x600",
                ")",

                "(",
                *image_ou_blanche(std, "1000x600"),
                "-resize", "x600",
                ")",

                "+append",
            ]

            if mean_v2.exists() or std_v2.exists():

                ligne_v2 = dossier / f"__ligneV2_{pert}.png"

                subprocess.run(
                    [
                        "magick",

                        "(",
                        *image_ou_blanche(mean_v2, "1000x600"),
                        "-resize", "x600",
                        ")",

                        "(",
                        *image_ou_blanche(std_v2, "1000x600"),
                        "-resize", "x600",
                        ")",

                        "+append",
                        str(ligne_v2),
                    ],
                    check=True,
                )   

                ligne_bas = dossier / f"__bas_{pert}.png"

                subprocess.run(
                    cmd + [str(ligne_bas)],
                    check=True,
                )

                subprocess.run(
                    [
                        "magick",
                        str(score),
                        "-resize", "1500x400",
                        str(ligne_bas),
                        str(ligne_v2),
                        "-append",
                        str(tuile),
                    ],
                    check=True,
                )

                ligne_v2.unlink()
                ligne_bas.unlink()

            else:

                ligne_bas = dossier / f"__bas_{pert}.png"

                subprocess.run(
                    cmd + [str(ligne_bas)],
                    check=True,
                )

                subprocess.run(
                    [
                        "magick",
                        str(score),
                        "-resize", "1500x400",
                        str(ligne_bas),
                        "-append",
                        str(tuile),
                    ],
                    check=True,
                )

                ligne_bas.unlink()

            tuiles.append(tuile)

    if not tuiles:
        raise RuntimeError("Aucune perturbation trouvée.")

    # Construction de la planche globale
    lignes = []

    for i in range(0, len(tuiles), nb_colonnes):

        ligne = dossier / f"__planche_ligne_{i}.png"

        subprocess.run(
            ["magick"] +
            [str(t) for t in tuiles[i:i+nb_colonnes]] +
            ["+append", str(ligne)],
            check=True,
        )

        lignes.append(ligne)

    subprocess.run(
        ["magick"] +
        [str(l) for l in lignes] +
        ["-append", sortie],
        check=True,
    )

    print(f"Planche enregistrée dans : {sortie}")

    # nettoyage
    if not keep_temp:
        for f in tuiles + lignes:
            f.unlink()



def main():
    parser = argparse.ArgumentParser(
        description=(
            "Génère une planche récapitulative à partir des "
            "graphiques produits lors des expériences de perturbation."
        )
    )

    parser.add_argument(
        "input_dir",
        help="Dossier contenant les images à regrouper.",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="planche_globale.png",
        help=(
            "Nom du fichier image généré "
            "(défaut : planche_globale.png)."
        ),
    )

    parser.add_argument(
        "-c",
        "--cols",
        type=int,
        default=4,
        help=(
            "Nombre de triplets affichés par ligne "
            "dans la planche finale (défaut : 4)."
        ),
    )

    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help=(
            "Conserve les images intermédiaires "
            "créées pendant l'assemblage."
        ),
    )

    parser.add_argument(
        "-p",
        "--pert_type",
        choices=["all", "replace", "append", "prepend", "full_replace"],
        default="all",
        help=(
            "Restreindre la place à un certain type de perturbation."
        ),
    )

    args = parser.parse_args()

    generer_planche(
        dossier=args.input_dir,
        sortie=args.output,
        nb_colonnes=args.cols,
        keep_temp=args.keep_temp,
        pert_type= args.pert_type
    )


if __name__ == "__main__":
    main()