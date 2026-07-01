#!/usr/bin/env python
# coding: utf-8

# # Générateur de graphiques de performance pour l'analyse de perturbations textuelles

# ## Description

# Ce script permet d'évaluer l'impact de perturbations lexicales sur les scores produits par un modèle de retrieval dense. À partir d'un ensemble de couples *(requête, document)* et d'une liste de perturbations définies par l'utilisateur, il génère différentes statistiques et représentations graphiques comparant les performances obtenues sur les documents originaux et leurs versions perturbées.

# Les perturbations sont appliquées uniquement aux documents. Les scores de similarité entre les requêtes et les documents sont ensuite recalculés afin d'étudier la sensibilité du modèle à ces modifications.

# ## Format des perturbations

# Les perturbations doivent être décrites dans un fichier texte contenant une règle par ligne. Trois types de transformations sont supportés :

# * `mot1->mot2` : remplacement de `mot1` par `mot2` ;
# * `mot->` : suppression de `mot` ;
# * `mot+` : ajout de `mot` au début du document ;
# * `+mot` : ajout de `mot` à la fin du document.

# La perturbation spéciale `full_replace` correspond à l'application de toutes les perturbations `replace` fournies appliquées en une fois.

# Exemple :

# ```
# drone->aéronef
# militaire->
# important+
# +confidentiel
# ```

# ## Données d'entrée

# Le script nécessite :

# * un modèle de retrieval compatible avec MechIR ;
# * un jeu de données contenant des couples *(requête, document)* ;
# * un fichier décrivant les perturbations à appliquer.

# Les données peuvent provenir soit :

# * d'un fichier CSV ;
# * d'une collection compatible avec `ir_datasets`.


# ### Paramètres concernant les entrées

# * `dot_model_name` : nom du modèle dense utilisé pour le calcul des représentations dans la base HuggingFace;
# * `perturbations_path` : chemin vers le fichier de perturbations ;
# * `full_replace` : indique si les perturbations fournies doivent être appliquées comme une seule perturbation `full_replace`ou non (/!\ Dans ce cas, les perturbations décrites dans `perturbations_path` doivent être toutes de type replace.)
# * `data_path` : chemin vers le fichier CSV ou identifiant de la collection dans la librairie `ir_datasets`;
# * `is_irdata` : indique si les données proviennent d'`ir_datasets` ;

# Dans le cas où le dataset provient d'un CSV:

# * `query_field` : nom de la colonne contenant les requêtes ;
# * `text_field` : nom de la colonne contenant les documents ;

# Dans le cas où le dataset est présent dans `ir_datasets`:

# * `query_id_subset` : liste optionnelle des identifiants de requêtes à conserver.


# ## Résultats produits

# Selon les options activées, le script peut générer :

# * les distributions des scores avant et après perturbation ;
# * les matrices d'impact des perturbations pour chaque composant du modèle sous la forme :
#     * de moyennes des perturbations des paires ;
#     * les écarts-types associés ;

# ### Paramètres concernant les sorties

# * `gen_matrices` : calcule les matrices d'impact des perturbations sur les composants ;
# * `gen_mean` : génère les graphiques des moyennes ;
# * `gen_std` : génère les graphiques des écarts-types;
# * `res_path` : répertoire où enregistrer les graphiques.


# ## Sauvegarde

# Un fichier JSON permettant de sauvegarder les scores calculés pour éviter leur recomputation lors d'exécutions ultérieures.

# Pour conserver les résultats calculés lors d'une execution, définir `save_values = True`.

# Pour pour exploiter des résultats préalablement sauvegardés, définir `load_values = True`.

# Le fichier JSON est enregistré/ lu est défini par `load_path`.



## paramètres du document
dot_model_name = "intfloat/multilingual-e5-small"    # "sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco"

data_path = "../challenge_data/mainV2/paires_mainV2.csv" # "vaswani" "../../../data/data_challenge/pairesV2_generees_1pourcent.csv"
query_field = "question"        # default : "text"
text_field = "text"             # default : "text"
is_irdata = False
query_id_subset=["1"] # default : None
sub_dataset_criteria = "pertinent" # default None

perturbations_path = "res/mE5-MainV2/test/new_pert_test.json"
full_replace = True
gen_matrices = True
gen_mean = False
gen_std = True
res_path = "res/mE5-MainV2/test/" 

load_values = True # default = False
load_path = "res/mE5-MainV2/test/perts_values.json"
save_values = False # default = False


from mechir import Dot
from mechir.data import MechIRDataset, MechDataset, DotDataCollator
from mechir.perturb import perturbation
from mechir.plotting import plot_components

import torch
from torch.utils.data import DataLoader

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

import pandas as pd
import numpy as np

from tqdm import tqdm
import json
from copy import deepcopy


#Perturbations parametrées
def param_append(doc, mot="microwave"):
    return doc + " " + mot

def param_prepend(doc, mot="microwave"):
    return mot+ " " + doc

def param_replace(doc, mot_orig="microwave", mot_rempl="toaster"):
    return doc.replace(mot_orig, mot_rempl)

def param_full_replace(doc, replacmts):
    res = doc
    for replacemt in replacmts["compo"]:
        assert replacemt["type"] == "replace" , "Les perturbations de type full-replace doivent se composer de perturbations de type replace seulement"
        res = res.replace(replacemt["from"], replacemt["to"])
    return res



# génération des perturbations à produire à partir du document txt
def generer_transformations_txt(fichier_regles):
    transformations = []

    with open(fichier_regles, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()

            if not ligne:
                continue

            # Cas 1 : remplacement ou suppression (mot->mot ou mot->)
            if "->" in ligne:
                gauche, droite = ligne.split("->", 1)
                mot_present = gauche.strip()
                mot_remplacant = droite.strip()
                transformations.append({"type":"replace", "from":mot_present, "to":mot_remplacant, "name":ligne})

            # Cas 2 : ajout en début (mot+)
            elif ligne.endswith("+"):
                mot = ligne[:-1].strip()
                transformations.append({"type":"prepend", "word":mot, "name":ligne})

            # Cas 3 : ajout en fin (+mot)
            elif ligne.startswith("+"):
                mot = ligne[1:].strip()
                transformations.append({"type":"append", "word":mot, "name":ligne})

            else:
                raise ValueError(f"Règle non reconnue : {ligne}")

    return transformations

def generer_transformations_json(fichier_regles):
    with open(fichier_regles, "r") as f:
        raw_regles = json.load(f)
    return raw_regles

# Helper function to print query/baseline document/perturbed document triplets
def pretty_print_triplets(batch, tokenizer, num=1):
    """
    Pretty prints triplets of queries, documents, and their corresponding perturbed documents from a batch.

    Args:
        batch (dict): A dictionary containing 'queries', 'documents', and 'perturbed_documents' from a DataLoader.
        tokenizer: The tokenizer used to decode the input IDs.
        num (int): Number of examples to show per batch.
    """
    # Get the queries, documents, and perturbed documents from the batch
    queries = batch["queries"]
    documents = batch["documents"]
    perturbed_documents = batch["perturbed_documents"]

    # Loop through number of examples to show in batch
    for i in range(len(documents["input_ids"][:num])):
        # Get the input IDs
        query_ids = queries["input_ids"][i]
        original_ids = documents["input_ids"][i]
        perturbed_ids = perturbed_documents["input_ids"][i]

        # Decode the input IDs to text
        query_decoded = tokenizer.decode(query_ids.tolist(), skip_special_tokens=False).replace("[PAD]", "").strip()
        original_doc_decoded = tokenizer.decode(original_ids.tolist(), skip_special_tokens=False).replace("[PAD]", "").strip()
        perturbed_doc_decoded = tokenizer.decode(perturbed_ids.tolist(), skip_special_tokens=False).replace("[PAD]", "").strip()

        # Pretty print
        # print(f"Triplet {i + 1}:")
        print("Query:", query_decoded)
        print("Baseline Document:", original_doc_decoded)
        print("Perturbed Document:", perturbed_doc_decoded)
        print("=" * 50)  # Separator for clarity

# Helper function to calculate and store performances
def calculate_performance(model, dataloader, baseline_performance, perturbed_performance, diags=False):
    for _, batch in tqdm(enumerate(dataloader)):
        # Get the queries, documents, and perturbed documents from the batch
        queries = batch["queries"]
        documents = batch["documents"]
        perturbed_documents = batch["perturbed_documents"]
        
        # Encode queries, baseline, and perturbed documents
        queries_encoded = model.forward(**queries)  # [batch_size x hidden_dim]
        baseline_encoded = model.forward(**documents)  # [batch_size x hidden_dim]
        perturbed_encoded = model.forward(**perturbed_documents)  # [batch_size x hidden_dim]


        # Calculate scores
        baseline_scores = torch.sum(queries_encoded.unsqueeze(1) * baseline_encoded.unsqueeze(0), dim=2)
        perturbed_scores = torch.sum(queries_encoded.unsqueeze(1) * perturbed_encoded.unsqueeze(0), dim=2)

        # Append flattened scores to the performance lists
        if diags:
            baseline_performance += baseline_scores.diag().tolist()
            perturbed_performance += perturbed_scores.diag().tolist()
        else:
            baseline_performance += baseline_scores.flatten().tolist()
            perturbed_performance += perturbed_scores.flatten().tolist()

def plot_scores(baseline_scores, perturbed_scores, transformation_descr, save_path = None):
    fig, ax = plt.subplots(1, 1, figsize=(15, 4), sharey=True)
    fig.suptitle('Distribution of Baseline vs Perturbed Scores '+transformation_descr, fontsize=16)
    sns.kdeplot(baseline_scores, label='Baseline', color='#D55E00', fill=True, ax=ax, alpha=0.5)
    sns.kdeplot(perturbed_scores, label='Perturbed', color='#009E73', fill=True, ax=ax, alpha=0.5)
    ax.set_ylabel('Density')
    ax.set_xlabel('Distances between R(q) and R(d)')
    ax.legend()
    #plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make space for the title
    
    if save_path is not None:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def plot_score_dists_mult(all_baseline_scores, all_perturbed_scores, plot_type="hist", save_path = None):
    # Number of subplots (one per perturbation type)
    num_plots = len(all_baseline_scores)

    # Set up the figure to hold multiple subplots in a single row
    fig, axs = plt.subplots(1, num_plots, figsize=(15, 4), sharey=True)
    fig.suptitle('Distribution of Baseline vs Perturbed Scores', fontsize=16)

    for idx, (perturb_type, ax) in enumerate(zip(all_baseline_scores.keys(), axs)):
        baseline_scores = all_baseline_scores[perturb_type]
        perturbed_scores = all_perturbed_scores[perturb_type]

        if plot_type == "hist":
            ax.hist(baseline_scores, label='Baseline', color='blue', alpha=0.5, bins=15)
            ax.hist(perturbed_scores, label='Perturbed', color='orange', alpha=0.5, bins=15)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_ylabel('Frequency')
            ax.legend()
        elif plot_type == "kde":
            # Use seaborn for KDE plot, smoother distribution representation
            sns.kdeplot(baseline_scores, label='Baseline', color='#D55E00', fill=True, ax=ax, alpha=0.5)
            sns.kdeplot(perturbed_scores, label='Perturbed', color='#009E73', fill=True, ax=ax, alpha=0.5)
            ax.set_ylabel('Density')
            ax.legend()
        elif plot_type == "box":
            ax.boxplot([baseline_scores, perturbed_scores], tick_labels=['Baseline', 'Perturbed'])
            ax.set_ylabel('Scores')

        ax.set_xlabel('Distances between R(q) and R(d)')
        ax.set_title(f'{perturb_type.capitalize()}')

     #plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make space for the title
    if save_path is not None:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

    return


VIEW_STYLES = {
    "base" : {
        "cmap" :"RdBu_r",
        "vmin" : -1,
        "vmax" : 1,
    },
    "base_adapt" : {
        "cmap" :"RdBu_r",
        "vmin" : -1,
        "vmax" : 1,
    },
    "base_extr" : {
        "cmap" :"RdBu_r",
        "vmin" : -50,
        "vmax" : 50,
    },
    "base_abs" : {
        "cmap" : "Reds",
        "vmin" : 0,
        "vmax" : 1,
    },
    "base_resc" : {
        "cmap" : "RdBu_r",
        "vmin" : -1,
        "vmax" : 1,
    },
    "std" : {
        "cmap" : "magma_r",
        "vmin" : 0,
        "vmax" : 1,
    },
    "std_adapt" : {
        "cmap" : "magma_r",
        "vmin" : 0,
        "vmax" : 1,
    },
    "std_max" : {
        "cmap" : "magma_r",
        "vmin" : 0,
        "vmax" : 50,
    },
    "std_resc" : {
        "cmap" : "magma_r",
        "vmin" : 0,
        "vmax" : 1,
    },
    "norm" : {
        "cmap" : "RdBu_r",
        "vmin" : -1,
        "vmax" : 1,
    },
    "std_norm" : {
        "cmap" : "magma_r",
        "vmin" : 0,
        "vmax" : 1,
    },
    "abs" : {
        "cmap" : "magma_r",
        "vmin" : 0,
        "vmax" : 50,
    },
}

def plot_components_V2(
    data,  # shape: (num_layers, num_heads) or (num_layers, num_heads + 1) if include_mlp=True
    save_path=None,
    title="Component Patching Results",
    include_mlp=False,
    view_style = "base"
):

    
    data = data.astype(float)
    plt.figure(figsize=(10, 6))

    printed_data = data
    view_params = VIEW_STYLES[view_style].copy()
    if "norm" in view_style:
        # printed_data = printed_data / np.linalg.norm(data)
        printed_data = (printed_data - printed_data.mean()) /printed_data.std()
    if "abs" in view_style:
        printed_data = printed_data.absolute()
    if "extr" in view_style:
        view_params["vmax"] = (abs(printed_data.max())+abs(printed_data.min())) /2
        view_params["vmin"] = - view_params["vmax"]
    if "max" in view_style:
        view_params["vmax"] = (abs(printed_data.max())+abs(printed_data.min())) /2
        view_params["vmin"] = 0
    if "adapt" in view_style:
        if (printed_data > 20).any() :
            view_params["vmax"] = 50
        else:
            view_params["vmax"] = 1
        view_params["vmin"] = (VIEW_STYLES[view_style]["vmin"] * view_params["vmax"]) # si vmin est déjà à 0 ça reste 0, si vmin est -1, on obtient -vmax
    if "resc" in view_style:
        printed_data = (np.sign(printed_data) / np.absolute(printed_data).max()) * np.absolute(printed_data)

    ax = sns.heatmap(
        printed_data,
        cmap=view_params["cmap"], 
        vmin=view_params["vmin"],
        vmax=view_params["vmax"],
        xticklabels=True,
        yticklabels=True,
        fmt=".2f",
        annot=True,
        annot_kws={"size": 8},
    )

    if include_mlp:
        new_labels = list(map(str, range(data.shape[1] - 1)))
        new_labels.append("MLP")
        ax.set_xticklabels(new_labels)

    plt.title(title)
    plt.xlabel("Head")
    plt.ylabel("Layer")

    if save_path:
        plt.savefig(save_path)
        plt.close()

    else:
        plt.show()

def load_pert_result(filepath):
    # chargement du contenu
    with open(filepath, 'r', encoding="utf-8") as load_file:
        perts_values = json.load(load_file)
    #conversion des listes de listes en ndarray de numpy
    for pert in perts_values:
        if  "patching_mean" in pert["results"] :
            pert["results"]["patching_mean"] = np.asarray(pert["results"]["patching_mean"])
        if "patching_std" in pert["results"]:
            pert["results"]["patching_std"] = np.asarray(pert["results"]["patching_std"])

    return perts_values


def save_pertubs_values(results_values, save_path):
    # copie et conversion des array numpy en liste de liste
    save_values = deepcopy(results_values)
    for pert in save_values:
        if  "patching_mean" in pert["results"] :
            pert["results"]["patching_mean"] = pert["results"]["patching_mean"].tolist()
        if "patching_std" in pert["results"] :
            pert["results"]["patching_std"] = pert["results"]["patching_std"].tolist()
    # sauvegarde
    with open(save_path, 'w', encoding="utf-8") as file:
            json.dump(save_values, file, indent=2)

def calculate_components(param_pert_dot_dataloader, gen_mean, gen_std):
    patching_head_outputs = []
    nan_cpt = 0
    for _, batch in tqdm(enumerate(param_pert_dot_dataloader)):
        queries = batch["queries"]
        documents = batch["documents"]
        perturbed_documents = batch["perturbed_documents"]

        patch_head_out = dot_model.patch(queries, documents, perturbed_documents, patch_type="head_all")

        nan_cpt += patch_head_out[0].isnan().sum()

        # # Interruption du calcul si la matrice contient un NaN
        # if patch_head_out[0].isnan().any().item() : 
        #     print("Component Patching Result non calculé : contient au moins un NaN")
        #     return None, None
        patching_head_outputs.append(patch_head_out)
    print(f"Nombre de NaN trouvés : {nan_cpt}")
    mean_head_outputs, std_head_outputs = None, None
    patching_head_outputs_cleaned = torch.stack([tens.nan_to_num() for tens,_ in patching_head_outputs])
    if gen_mean :
        mean_head_outputs = torch.mean(patching_head_outputs_cleaned, axis=0).detach().to("cpu").numpy()
    if gen_std :
        std_head_outputs = torch.std(patching_head_outputs_cleaned, axis=0).detach().to("cpu").numpy()

    return mean_head_outputs, std_head_outputs, patching_head_outputs_cleaned

def load_dataset(data_path, is_irdata, query_id_subset = None, query_field = "text", text_field ="text"):
    if is_irdata:
        dataset = MechIRDataset(data_path, query_id_subset=query_id_subset)
        # print("Number of query,doc pairs in dataset:", len(dataset))
    else:
        data = pd.read_csv(data_path)
        if sub_dataset_criteria is not None:
            data = data.query(sub_dataset_criteria)
        dataset = MechDataset(data, query_field=query_field, text_field=text_field)
        # print("Number of query,doc pairs in dataset:", len(dataset))
    return dataset

def one_pert_traitement(
        pert,
        dot_model, 
        dataset, 
        gen_matrices = False, 
        gen_mean=False, 
        gen_std=False
    ):
    if pert["type"] == "full_replace":
        pert_fun = perturbation(lambda texte : param_full_replace(texte, pert))
        pert_type = "replace"
    elif pert["type"]=="replace":
        pert_fun = perturbation(lambda texte : param_replace(texte, pert["from"], pert["to"]))
        pert_type = pert["type"]
    elif pert["type"]=="prepend":
        pert_fun = perturbation(lambda texte : param_prepend(texte, pert["word"]))
        pert_type = pert["type"]
    elif pert["type"]=="append":
        pert_fun = perturbation(lambda texte : param_append(texte, pert["word"]))
        pert_type = pert["type"]
    else:
        raise RuntimeError("Unreachable")
    param_pert_dot_collator = DotDataCollator(dot_model.tokenizer, pert_fun,  perturb_type=pert_type)
    param_pert_dot_dataloader = DataLoader(dataset, collate_fn=param_pert_dot_collator)

    # param_pert_batch = next(iter(param_pert_dot_dataloader))
    # print("PERTURBATION",i,":", pert_name)
    # pretty_print_triplets(param_pert_batch, dot_model.tokenizer, num=2)

    baseline_perf = []
    perturbed_perf = []
    calculate_performance(dot_model, param_pert_dot_dataloader, baseline_perf, perturbed_perf, diags=True)

    if gen_matrices:
        mean_head_outputs, std_head_outputs, _ = calculate_components(param_pert_dot_dataloader, gen_mean, gen_std)

    # Sauvegarde des valeurs pour la  perturbation
    pert_values = {"baseline_perf": baseline_perf, "perturbed_perf": perturbed_perf}
    if gen_matrices and mean_head_outputs is not None :
        pert_values["patching_mean"] = mean_head_outputs
    if gen_matrices and std_head_outputs is not None:
        pert_values["patching_std"] = std_head_outputs

    return pert_values

# Calcul ou extraction des valeurs
if load_values:
    perts_values = load_pert_result(load_path)
    # print(perts_values)
else:
    # Récup du modèle
    dot_model = Dot(dot_model_name)

    # Recup dataset
    dataset = load_dataset(data_path, is_irdata, query_id_subset, query_field, text_field)

    match perturbations_path.split(".")[-1].strip():
        case "txt":
            print("Appel à generer_transformations_txt")
            perts = generer_transformations_txt(perturbations_path)
        case "json":
            print("Appel à generer_transformations_json")
            perts = generer_transformations_json(perturbations_path)
        case _:
            raise RuntimeError("Unreachable")
    
    perts_values = []
    for pert in perts:
        print(pert["name"], "="*50)
        perts_values.append({
            "pert" : pert,
            "results" : one_pert_traitement(
                pert, 
                dot_model, 
                dataset,
                gen_matrices= gen_matrices,
                gen_mean= gen_mean,
                gen_std = gen_std)
        })

    if save_values:
         save_pertubs_values(perts_values, f"{res_path}/perts_values.json")



# Génération des graphiques
print("Génération des graphiques")
for pert_values in perts_values:
    plot_scores(pert_values["results"]["baseline_perf"], pert_values["results"]["perturbed_perf"], pert_values["pert"]["name"], save_path=res_path+"PerturbationScore_"+pert_values["pert"]["name"]+".png")
    if "patching_mean" in pert_values["results"] and pert_values["results"]["patching_mean"] is not None:
        plot_components_V2(pert_values["results"]["patching_mean"], title="Components Patching Results (mean) for "+ pert_values["pert"]["name"], save_path=res_path+"ComponentPatching-mean_"+pert_values["pert"]["name"]+".png", view_style="base_adapt")
        plot_components_V2(pert_values["results"]["patching_mean"], title="Components Patching Results (mean) for "+ pert_values["pert"]["name"], save_path=res_path+"ComponentPatching-mean_"+pert_values["pert"]["name"]+"V2.png", view_style="base_resc")

    if "patching_std" in pert_values["results"] and pert_values["results"]["patching_std"] is not None:
        plot_components_V2(pert_values["results"]["patching_std"], title="Components Patching Results (std) for "+ pert_values["pert"]["name"], save_path=res_path+"ComponentPatching-std_"+pert_values["pert"]["name"]+".png", view_style="std_adapt")
        plot_components_V2(pert_values["results"]["patching_std"], title="Components Patching Results (std) for "+ pert_values["pert"]["name"], save_path=res_path+"ComponentPatching-std_"+pert_values["pert"]["name"]+"V2.png", view_style="std_resc")
