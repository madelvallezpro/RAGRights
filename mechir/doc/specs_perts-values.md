# Spécification de la représentation des données calculées pour un lot de perturbations

## Perturbation
Les perturbations ont décrites à l'aide du même système que décrit dans `specs_perturbations.md`.

## Données obtenues

On peut obtenir jusqu'à 4 ensembles de valeurs différents:
- `baseline_perf` (liste de `float`) : les scores (distance entre les représentations) des paires (question document) lorsqu'on n'applique pas la perturbation
- `perturbed_perf` (liste de `float`)  : les scores distance entre les représentations) des paires (question document) lorsqu'on applique la perturbation
- `patching_mean` (tableau au format du modèle de `float`)  : matrice de sensibilité (moyennes pour chaque composant des sensibilités obtenues pour chaque paires)
- `patching_std` (tableau au format du modèle de `float`) : écarts-types pour chaque composant des sensibilités obtenues pour chaque paires

Si `patching_mean` et/ou `patching_std` ne sont pas calculés, ils valent null

## Spécification globale

Les valeurs sont regroupées dans une liste ou chaque objet contient:
- La description de la perturbation correspondante
- Dans un objet `results` les quatre données attendues 

## Ancienne représentation
L'ancienne représentation des résultats pour les perturbations append, prepend et replace était de la forme
```{json}
{
    "nom_perturbation" : {
        "baseline_perf" : ...
        "perturbed_perf": ...
        "patching_mean" : ...
        "patching_std" : ...
    },
    "nom_perturbation2" : {
        "baseline_perf" : ...
        "perturbed_perf": ...
        "patching_mean" : ...
        "patching_std" : ...
    }
    ...
}
``` 

Dans le cas des perturbations full_replace. Il n'y avait les résultats que d'une perturbation dans le fichier. Le nom de la perturbation était systématiquement "full_replace" et les reste de la structure du fichier est la même pour les autres types de perturbations.