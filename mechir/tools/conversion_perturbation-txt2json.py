#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convertit un fichier texte décrivant des perturbations vers le format JSON.

Le fichier texte peut contenir :
    mot1 -> mot2     : replace
    mot1 ->          : suppression (replace vers chaîne vide)
    mot+             : prepend
    +mot             : append

Si le fichier ne contient que des perturbations replace, l'utilisateur
peut choisir de les interpréter comme :
    - une liste de perturbations indépendantes
    - une unique perturbation full_replace
"""

import argparse
import json
from pathlib import Path


# ----------------------------------------------------------------------
# Lecture du fichier texte
# ----------------------------------------------------------------------

def lire_perturbations(path):
    """Lit le fichier texte et renvoie la liste des perturbations."""

    perturbations = []

    with open(path, "r", encoding="utf-8") as f:

        for ligne in f:

            ligne = ligne.strip()

            if not ligne:
                continue

            if "->" in ligne:
                gauche, droite = ligne.split("->", 1)

                perturbations.append({
                    "type": "replace",
                    "from": gauche.strip(),
                    "to": droite.strip(),
                    "name": ligne
                })

            elif ligne.endswith("+"):

                mot = ligne[:-1].strip()

                perturbations.append({
                    "type": "prepend",
                    "word": mot,
                    "name": ligne
                })

            elif ligne.startswith("+"):

                mot = ligne[1:].strip()

                perturbations.append({
                    "type": "append",
                    "word": mot,
                    "name": ligne
                })

            else:
                raise ValueError(f"Perturbation inconnue : {ligne}")

    return perturbations


# ----------------------------------------------------------------------
# Détection du cas full_replace
# ----------------------------------------------------------------------

def uniquement_replace(perturbations):
    return all(p["type"] == "replace" for p in perturbations)


def demander_mode():
    print()
    print("Le fichier ne contient que des perturbations replace.")
    print()
    print("Comment souhaitez-vous l'interpréter ?")
    print("  1 - Liste de perturbations indépendantes")
    print("  2 - Une perturbation full_replace")
    print()

    while True:

        choix = input("Votre choix (1/2) : ").strip()

        if choix in ("1", "2"):
            return choix

        print("Veuillez répondre 1 ou 2.")


# ----------------------------------------------------------------------
# Construction du JSON
# ----------------------------------------------------------------------

def construire_json(perturbations, full_replace, descr):

    if not uniquement_replace(perturbations):
        return perturbations

    if not full_replace:
        return perturbations

    return [{
        "type": "full_replace",
        "name": descr,
        "compo": perturbations
    }]


# ----------------------------------------------------------------------
# Sauvegarde
# ----------------------------------------------------------------------

def sauvegarder(obj, path):

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            obj,
            f,
            ensure_ascii=False,
            indent=4
        )


# ----------------------------------------------------------------------
# Programme principal
# ----------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Convertit un fichier txt de perturbations en JSON."
    )

    parser.add_argument(
        "input",
        help="Fichier texte d'entrée"
    )

    parser.add_argument(
        "output",
        nargs="?",
        help="Fichier JSON de sortie (défaut : même nom)"
    )

    parser.add_argument(
        "--full_replace",
        action="store_true",
        help="Traite le fichier fourni comme une perturbation full_replace. Le fichier ne doit donner que des perturbations replace."
    )

    parser.add_argument(
        "--name",
        help="Description de la perturbation full_replace"
    )
    args = parser.parse_args()

    input_path = Path(args.input)

    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_suffix(".json")
    )

    perturbations = lire_perturbations(input_path)

    json_obj = construire_json(perturbations, args.full_replace, args.name)

    sauvegarder(json_obj, output_path)

    print(f"\nJSON enregistré dans : {output_path}")


if __name__ == "__main__":
    main()