#!/usr/bin/env python

import json
import numpy as np
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from itertools import combinations


def compter_noeuds_sensibles(json_path, pert_type):
    """
    Compte le nombre de perturbations pour lesquelles chaque noeud
    est considéré comme sensible.

    Parameters
    ----------
    json_path : str
        Chemin du fichier JSON.

    est_sensible : callable
        Fonction prenant (mean, std) et renvoyant True ou False.

    Returns
    -------
    np.ndarray
        Matrice des comptes.
    """

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    premiere_perturbation = next(iter(data.values()))
    shape = np.array(premiere_perturbation["patching_mean"]).shape

    compteurs = np.zeros(shape, dtype=int)
    compteur_pert =  {}

    for perturbation, valeurs in data.items():

        if pert_type == "all" or pert_type == perturbation_type(perturbation):
            mean = np.array(valeurs["patching_mean"])
            std = np.array(valeurs["patching_std"])
            resc_mean = (np.sign(mean) / np.absolute(mean).max()) * np.absolute(mean)
            resc_std = (np.sign(std) / np.absolute(std).max()) * np.absolute(std)

            compteur_pert[perturbation] ={}
            compteur_pert[perturbation]["carte"] = ((np.abs(mean) > 0.1) & (np.abs(resc_mean) > 0.5)) | (resc_std > 0.5)

            compteur_pert[perturbation]["noeuds_sensibles"] = []
            for i in range(mean.shape[0]):
                for j in range(mean.shape[1]):
                    if compteur_pert[perturbation]["carte"][i,j]:
                        compteur_pert[perturbation]["noeuds_sensibles"].append((i,j,mean[i,j], std[i,j], resc_mean[i,j], resc_std[i,j]))


            compteur_pert[perturbation]["total"] = np.sum(compteur_pert[perturbation]["carte"])

            compteurs += compteur_pert[perturbation]["carte"]

    return compteurs, compteur_pert

def plot_noeuds_sensibles(noeuds_sensibles, title, save_path):
    ax = sns.heatmap(
        noeuds_sensibles,
        cmap="Reds", 
        vmin=0,
        vmax=noeuds_sensibles.max(),
        xticklabels=True,
        yticklabels=True,
        annot=True,
        annot_kws={"size": 8},
    )


    plt.title(title)
    plt.xlabel("Head")
    plt.ylabel("Layer")

    if save_path:
        plt.savefig(save_path)
        plt.close()

    else:
        plt.show()

def perturbation_type(pert):
    if "->" in pert:
        return "replace"
    if pert[0] == "+":
        return "append"
    if pert[-1] =="+":
        return "prepend" 
    raise RuntimeWarning("Unreachable")

def stats(noeuds_perts, path):
    s = "Nombre de noeuds relevés par perturbation"
    for pert, values in noeuds_perts.items():
        s+=f"\n{pert} : {values["total"]}"
    for pert, values in noeuds_perts.items():
        s+=f"\n{pert} : "
        for i,j,mean,std,rmean,rstd in values["noeuds_sensibles"]:
            s += f"\n\t({i}, {j}) {mean:.2f}, {std:.2f} | {rmean:.2f}, {rstd:.2f}"
    print(s)
    if path:
        with open(path,'w') as f:
            f.write(s)
    


def cli():
    parser = argparse.ArgumentParser(
        description=(
            "Génère une matrice récapitulative des noeuds "
            "sensibles pour le lot de matrices de sensibilité à des"
            " perturbations fourni."
        )
    )
    parser.add_argument(
        "input_json",
        help="Fichier JSON contennant les matrices de sensibilité aux perturbation.",
    )
    parser.add_argument(
        "-t",
        "--title",
        default="Noeuds sensibles",
        help=(
            "Titre du graphique généré "
            "(défaut : pNoeuds sensibles)."
        ),
    )
    parser.add_argument(
        "-s",
        "--save",
        default=False,
        type=Path,
        help=(
            "Chemin de répertoire pour la sauvegarde des informations"
            "(défaut : False (affiche mais ne sauvegarde pas))."
        ),
    )
    parser.add_argument(
        "-p",
        "--perturbationtype",
        default="all",
        choices=['all', 'replace', 'append', 'prepend'],
        help=(
            "Chemin de sauvegarde du graphique"
            "(défaut : False (affiche mais ne sauvegarde pas))."
        ),
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = cli()
    noeuds_sensibles, noeuds_perts = compter_noeuds_sensibles(args.input_json, pert_type = args.perturbationtype)
    save_path = False if not args.save else Path(args.save)
    save_stats_path = False if not args.save else save_path/f"StatsSensibiliteNoeuds-{args.perturbationtype}.txt"
    save_plot_path = False if not args.save else save_path/f"SensibiliteNoeuds-{args.perturbationtype}.png"
    stats(noeuds_perts, save_stats_path)
    plot_noeuds_sensibles(noeuds_sensibles, 
                          title=args.title,
                          save_path=save_plot_path)
