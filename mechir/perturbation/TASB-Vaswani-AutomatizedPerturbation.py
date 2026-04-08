from mechir import Dot
from mechir.data import MechIRDataset, DotDataCollator
from mechir.perturb import perturbation
from mechir.plotting import plot_components

import torch
from torch.utils.data import DataLoader

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns


#Perturbations parametrées
def param_append(doc, mot="microwave"):
    return doc + " " + mot

def param_prepend(doc, mot="microwave"):
    return mot+ " " + doc

def param_replace(doc, mot_orig="microwave", mot_rempl="toaster"):
    return doc.replace(mot_orig, mot_rempl)

# génération des perturbations à produire
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
                print(f"{gauche}, {droite}")
                print(f"{mot_present}, {mot_remplacant}")
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
                transformations.append( ("prepend", mot))
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
def calculate_performance(model, dataloader, baseline_performance, perturbed_performance):
    for i, batch in enumerate(dataloader):
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
        baseline_performance += baseline_scores.flatten().tolist()
        perturbed_performance += perturbed_scores.flatten().tolist()

def plot_scores(baseline_scores, perturbed_scores, transformation_descr):
    fig, ax = plt.subplots(1, 1, figsize=(15, 4), sharey=True)
    fig.suptitle('Distribution of Baseline vs Perturbed Scores '+transformation_descr, fontsize=16)
    sns.kdeplot(baseline_scores, label='Baseline', color='#D55E00', fill=True, ax=ax, alpha=0.5)
    sns.kdeplot(perturbed_scores, label='Perturbed', color='#009E73', fill=True, ax=ax, alpha=0.5)
    ax.set_ylabel('Density')
    ax.legend()
    #plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make space for the title
    plt.savefig('res/'+ (transformation_descr.replace(">", ""))+'_scores.png')





# Récup du modèle
dot_model_name = "sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco"
dot_model = Dot(dot_model_name)

# Recup dataset
dataset = MechIRDataset("vaswani", query_id_subset=["1"])
print("Number of query,doc pairs in dataset:", len(dataset))
print("Query:", dataset._get_query("1"))

perts, perts_name = generer_transformations("perturbations.txt")
for i in range(len(perts)):
    if perts[i][0]=="replace":
        pert_fun = perturbation(lambda texte : param_replace(texte, perts[i][1], perts[i][2]))
    elif perts[i][0]=="prepend":
        pert_fun = perturbation(lambda texte : param_prepend(texte, perts[i][1]))
    else:
        pert_fun = perturbation(lambda texte : param_append(texte, perts[i][1]))
    param_pert_dot_collator = DotDataCollator(dot_model.tokenizer, pert_fun, q_max_length=None, d_max_length=None, perturb_type=perts[i][0])
    param_pert_dot_dataloader = DataLoader(dataset, batch_size=16, collate_fn=param_pert_dot_collator)

    param_pert_batch = next(iter(param_pert_dot_dataloader))
    print("PERTURBATION",i,":", perts_name[i])
    pretty_print_triplets(param_pert_batch, dot_model.tokenizer, num=2)

    baseline_perf = []
    perturbed_perf = []
    calculate_performance(dot_model, param_pert_dot_dataloader, baseline_perf, perturbed_perf)


    plot_scores(baseline_perf, perturbed_perf, perts_name[i])