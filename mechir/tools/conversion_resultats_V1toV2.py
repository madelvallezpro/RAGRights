#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convertit un ancien fichier de résultats MechIR vers le nouveau format.

Cas gérés :
    - replace
    - prepend
    - append
    - full_replace

Dans le cas d'une perturbation full_replace, un fichier décrivant les
perturbations (nouveau format JSON) doit être fourni.
"""

import argparse
import json
from pathlib import Path

# ----------------------------------------------------------------------
# Lecture
# ----------------------------------------------------------------------

def charger_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



# ----------------------------------------------------------------------
# Parsing d'une perturbation simple (pas full_replace)
# ----------------------------------------------------------------------

def perturbation_depuis_nom(name):

    name = name.strip()

    if "->" in name:

        gauche, droite = name.split("->", 1)

        return {
            "type": "replace",
            "from": gauche.strip(),
            "to": droite.strip(),
            "name": name
        }

    if name.endswith("+"):

        return {
            "type": "prepend",
            "word": name[:-1].strip(),
            "name": name
        }

    if name.startswith("+"):

        return {
            "type": "append",
            "word": name[1:].strip(),
            "name": name
        }

    raise ValueError(f"Impossible d'interpréter : {name}")



# ----------------------------------------------------------------------
# Chargement de la description d'une perturbation full_replace
# ----------------------------------------------------------------------

def charger_full_replace(path, n_occ_full_replace):

    perts = charger_json(path)

    if not isinstance(perts, list):
        raise ValueError("Le fichier de description de perturbation est mal formé.")


    full = [p for p in perts if p["type"] == "full_replace"]

    if len(full) == 0:
        raise ValueError("Aucune perturbation full_replace trouvée.")

    if len(full) > 1 :
        if n_occ_full_replace is None:
            raise ValueError(
                "Plusieurs perturbations full_replace présentes. "
                "Le script ne sait pas laquelle utiliser."
            )
        
        if n_occ_full_replace >= len(full):
            raise ValueError("Aucune perturbation full_replace ne correspond au numéro d'occurence donné")
        
        return full[n_occ_full_replace]

    return full[0]



# ----------------------------------------------------------------------
# Conversion
# ----------------------------------------------------------------------

def convertir(ancien, full_replace=None):

    nouveau = []

    for nom, valeurs in ancien.items():

        if nom == "full_replace":

            if full_replace is None:
                raise ValueError(
                    "Le fichier contient une perturbation full_replace.\n"
                    "Veuillez fournir le fichier de description correspondant."
                )

            perturbation = full_replace

        else:

            perturbation = perturbation_depuis_nom(nom)

        nouveau.append({

            "perturbation": perturbation,

            "results": {

                "baseline_perf":
                    valeurs.get("baseline_perf"),

                "perturbed_perf":
                    valeurs.get("perturbed_perf"),

                "patching_mean":
                    valeurs.get("patching_mean"),

                "patching_std":
                    valeurs.get("patching_std")
            }
        })

    return nouveau


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
# Main
# ----------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
        help="Ancien fichier JSON"
    )

    parser.add_argument(
        "-p",
        "--perturbations",
        help="Fichier JSON des perturbations (nécessaire pour full_replace)"
    )

    parser.add_argument(
        "-n",
        "--perturbation_number",
        help="Si plusieurs perturbations full_replace sont présentes dans le fichier JSON décrivant les pertubations, numéro d'occurence de la perturbation full_replace à considérer."
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Fichier de sortie"
    )

    args = parser.parse_args()

    ancien = charger_json(args.input)

    full_replace = None

    if "full_replace" in ancien:

        if args.perturbations is None:
            parser.error(
                "Le fichier contient une perturbation full_replace.\n"
                "Veuillez fournir --perturbations."
            )

        full_replace = charger_full_replace(args.perturbations,n_occ_full_replace = args.perturbation_number)

    output = (
        Path(args.output)
        if args.output
        else Path(args.input).with_name(
            Path(args.input).stem + "_v2.json"
        )
    )

    nouveau = convertir(
        ancien,
        full_replace=full_replace
    )

    sauvegarder(nouveau, output)

    print(f"Fichier créé : {output}")


if __name__ == "__main__":
    main()