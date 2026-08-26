# Spécification du CLI associé à GenericAutomatedPerturbation.py

## Action 1 : Calcul des valeurs (`values`)

Arguments obligatoires :

- modele (str) : nom du modèle (chemin ou adresse HuggingFace)
- dataset (str) : nom du dataset dans irdataset ou chemin dans l'arborescence
- dataset_origin (choices = ["irdatasets", "file"]) : Origine du dataset. indique comment obtenir le dataset
- perturbation (str) : chemin vers le fichier descriptif des perturbations


Arguments optionnels :

- query_field (str, default="question") : champ du fichier des paires correspondant aux questions
- docs_field (str, default="text") : champ du fichier des paires correspondant aux documents
- subdataset_condition (str, default=None) : critère de sélection d'une sous-partie du dataset
- gen_mean (bool, action = "store_true") : déclenche le calcul des matrices de moyennes de sensibilité
- gen_std (bool, action = "store_true") : déclenche le calcul des matrices d'écarts-types de sensibilité
- output (str, default=None) : spécifie le nom du fichier de sauvegarde des valeurs (Par défaut, le dossier des perturbations est utilisé et le fichier est nommé perts_values.json)


## Action 2 : Génération des graphiques (`graphs`)

Arguments obligatoires :

- input (str) : Fichier contenant les données à mettre sous graphe

Arguments optionnels:

- output (str, default=None) : spécifie le nom du dossier de sauvegarde des graphiques (Par défaut, le dossier de l'input)