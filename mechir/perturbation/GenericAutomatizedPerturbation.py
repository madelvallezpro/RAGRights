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

perturbations_path = "perturbations_mainV2_elephantrose.txt"
gen_matrices = True
gen_mean = True
gen_std = True
res_path = "res/mE5-MainV2/elephants-roses/" 

load_values = True # default = False
load_path = "res/mE5-MainV2/elephants-roses/perts_values.json"
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


#Perturbations parametrées
def param_append(doc, mot="microwave"):
    return doc + " " + mot

def param_prepend(doc, mot="microwave"):
    return mot+ " " + doc

def param_replace(doc, mot_orig="microwave", mot_rempl="toaster"):
    return doc.replace(mot_orig, mot_rempl)


# génération des perturbations à produire à partir du document
def generer_transformations(fichier_regles):
    transformations = []
    perts_name=[]

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
                # print(f"{gauche}, {droite}")
                # print(f"{mot_present}, {mot_remplacant}")
                transformations.append( ("replace", mot_present, mot_remplacant)
                )
                perts_name.append(ligne)

            # Cas 2 : ajout en début (mot+)
            elif ligne.endswith("+"):
                mot = ligne[:-1].strip()
                transformations.append( ("prepend", mot))
                perts_name.append(ligne)

            # Cas 3 : ajout en fin (+mot)
            elif ligne.startswith("+"):
                mot = ligne[1:].strip()
                transformations.append( ("append", mot))
                perts_name.append(ligne)

            else:
                raise ValueError(f"Règle non reconnue : {ligne}")

    return transformations, perts_name

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
    with open(filepath, 'r', encoding="utf-8") as load_file:
        perts_values = json.load(load_file)
    for pert_name in perts_values:
        if  "patching_mean" in perts_values[pert_name] :
            perts_values[pert_name]["patching_mean"] = np.asarray(perts_values[pert_name]["patching_mean"])
        if "patching_std" in perts_values[pert_name]:
            perts_values[pert_name]["patching_std"] = np.asarray(perts_values[pert_name]["patching_std"])

    return perts_values


def save_pertubs_values(result_file, save_path):
    save_values = {}
    for pert_name in result_file:
        save_values[pert_name] = {}
        save_values[pert_name]["baseline_perf"] = result_file[pert_name]["baseline_perf"]
        save_values[pert_name]["perturbed_perf"] = result_file[pert_name]["perturbed_perf"]
        if  "patching_mean" in result_file[pert_name] :
            save_values[pert_name]["patching_mean"] = result_file[pert_name]["patching_mean"].tolist()
        if "patching_std" in result_file[pert_name]:
            save_values[pert_name]["patching_std"] = result_file[pert_name]["patching_std"].tolist()
    with open(save_path, 'w', encoding="utf-8") as result_file:
            json.dump(save_values, result_file, indent=2)

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
    if gen_mean :
        mean_head_outputs = torch.mean(torch.stack([tens.nan_to_num() for tens,_ in patching_head_outputs]), axis=0).detach().to("cpu").numpy()
    if gen_std :
        std_head_outputs = torch.std(torch.stack([tens.nan_to_num() for tens,_ in patching_head_outputs]), axis=0).detach().to("cpu").numpy()

    return mean_head_outputs, std_head_outputs

def load_dataset(data_path, is_irdata, query_id_subset = None, query_field = "text", text_field ="text"):
    if is_irdata:
        dataset = MechIRDataset(data_path, query_id_subset=query_id_subset)
        # print("Number of query,doc pairs in dataset:", len(dataset))
    else:
        data = pd.read_csv(data_path)
        dataset = MechDataset(data, query_field=query_field, text_field=text_field)
        # print("Number of query,doc pairs in dataset:", len(dataset))
    return dataset

# Calcul ou extraction des valeurs
if load_values:
    perts_values = load_pert_result(load_path)
    # print(perts_values)
else:
    # Récup du modèle
    dot_model = Dot(dot_model_name)


    # Recup dataset
    dataset = load_dataset(data_path, is_irdata, query_id_subset, query_field, text_field)


    perts, perts_name = generer_transformations(perturbations_path)
    perts_values = {}
    for i in range(len(perts)):
        print(perts[i], "="*50)
        if perts[i][0]=="replace":
            pert_fun = perturbation(lambda texte : param_replace(texte, perts[i][1], perts[i][2]))
        elif perts[i][0]=="prepend":
            pert_fun = perturbation(lambda texte : param_prepend(texte, perts[i][1]))
        elif perts[i][0]=="append":
            pert_fun = perturbation(lambda texte : param_append(texte, perts[i][1]))
        else:
            raise RuntimeError("Unreachable")
        param_pert_dot_collator = DotDataCollator(dot_model.tokenizer, pert_fun,  perturb_type=perts[i][0])
        param_pert_dot_dataloader = DataLoader(dataset, collate_fn=param_pert_dot_collator)

        # param_pert_batch = next(iter(param_pert_dot_dataloader))
        # print("PERTURBATION",i,":", perts_name[i])
        # pretty_print_triplets(param_pert_batch, dot_model.tokenizer, num=2)

        baseline_perf = []
        perturbed_perf = []
        calculate_performance(dot_model, param_pert_dot_dataloader, baseline_perf, perturbed_perf, diags=True)

        # plot_scores(baseline_perf, perturbed_perf, perts_name[i], save_path=res_path+"PerturbationScore_"+perts_name[i]+".png")

        if gen_matrices:
            mean_head_outputs, std_head_outputs = calculate_components(param_pert_dot_dataloader, gen_mean, gen_std)
            # if mean_head_outputs is not None:
            #     plot_components_V2(mean_head_outputs, title="Components Patching Results (mean) for "+ perts_name[i], save_path=res_path+"ComponentPatching-mean_"+perts_name[i]+"V2.png")
            # if std_head_outputs is not None:
            #     plot_components_V2(std_head_outputs, title="Components Patching Results (std) for "+ perts_name[i], save_path=res_path+"ComponentPatching-std_"+perts_name[i]+"V2.png")


        # Sauvegarde des valeurs pour la i^eme perturbation

        perts_values[perts_name[i]] = {"baseline_perf": baseline_perf, "perturbed_perf": perturbed_perf}
        if gen_matrices and mean_head_outputs is not None :
            perts_values[perts_name[i]]["patching_mean"] = mean_head_outputs
        if gen_matrices and std_head_outputs is not None:
            perts_values[perts_name[i]]["patching_std"] = std_head_outputs

    if save_values:
         save_pertubs_values(perts_values, f"{res_path}/perts_values.json")



# Génération des graphiques
print("Génération des graphiques")
for pert_name, pert_values in perts_values.items():
    plot_scores(pert_values["baseline_perf"], pert_values["perturbed_perf"], pert_name, save_path=res_path+"PerturbationScore_"+pert_name+".png")
    if "patching_mean" in pert_values and pert_values["patching_mean"] is not None:
        plot_components_V2(pert_values["patching_mean"], title="Components Patching Results (mean) for "+ pert_name, save_path=res_path+"ComponentPatching-mean_"+pert_name+".png", view_style="base_adapt")
        plot_components_V2(pert_values["patching_mean"], title="Components Patching Results (mean) for "+ pert_name, save_path=res_path+"ComponentPatching-mean_"+pert_name+"V2.png", view_style="base_resc")

    if "patching_std" in pert_values and pert_values["patching_std"] is not None:
        plot_components_V2(pert_values["patching_std"], title="Components Patching Results (std) for "+ pert_name, save_path=res_path+"ComponentPatching-std_"+pert_name+".png", view_style="std_adapt")
        plot_components_V2(pert_values["patching_std"], title="Components Patching Results (std) for "+ pert_name, save_path=res_path+"ComponentPatching-std_"+pert_name+"V2.png", view_style="std_resc")
