#!/usr/bin/env python3.12


# # À partir d'une liste de requêtes et d'une liste de documents (tous deux des strings) fourni dans deux csv
# # Extraction du vocabulaire présent dans les queries (df.vocab) et des statistiques suivantes pour chaque mot:
# # - mot : le mot
# # - idf : log10((nombre de documents + 1)/(nombre de documents contenant le mot+1))
# # - query_freq2 : nombre d'occurrence du mot dans les queries (2 occurrences dans une même query compte pour 2)
# # - docs_freq : nombre d'occurrence du mot dans les documents (2 occurrences dans un même documents compte pour 1)



import sys
import csv
import re
from collections import Counter
import pandas as pd
from math import log10

def extraire_csv(fichier_csv):
    phrases = []

    with open(fichier_csv, newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f, fieldnames=["entrees"])
        for ligne in lecteur:
            phrases.append(ligne["entrees"])

    return phrases

def queries_vocab_freq(queries):
    # Extraire les mots (lettres + chiffres)
    mots = re.findall(r"(\b\w+\b)|([-+]?[0-9]+)", ' '.join(queries).lower())

    # Compter les occurrences
    compteur = Counter(mots)

    # Trier du plus fréquent au moins fréquent
    tableau = pd.DataFrame(columns=["mot", "query_freq2"])
    for mot, count in compteur.most_common():
        tableau.loc[len(tableau)] = {"mot":mot[0], "query_freq2":count}

    return tableau


def calcul_idf(docs, vocab):
    idfs = pd.DataFrame(columns=["mot", "idf", "docs_freq"])
    vocab_size = len(vocab)
    for i_mot in range(vocab_size):
        nb_occ = 0
        for doc in docs:
            if vocab[i_mot] in doc:
                nb_occ += 1
        if nb_occ==0:
            print(f"mot : {vocab[i_mot]}")
        idfs.loc[i_mot] = {"mot":vocab[i_mot], "idf":log10((len(docs)+1)/(nb_occ+1)), "docs_freq":nb_occ}
    return idfs




def main(docs_path, query_path, csv_path, sort_criteria):
    docs = extraire_csv(docs_path)
    queries = extraire_csv(query_path)

    freqs = queries_vocab_freq(queries)
    idfs = calcul_idf(docs, freqs.mot)

    dt = pd.merge(freqs, idfs, how='outer', on='mot')

    dt["query_freq2/docs_freq"] = dt.query_freq2*dt.docs_freq

    if sort_criteria != "alpha":
        if sort_criteria in ['query_freq2', 'idf', 'docs_freq', 'query_freq2/docs_freq']:
            dt = dt.sort_values(by=sort_criteria)
        else:
            raise ValueError("Les critères de tri possibles sont",str(['query_freq2', 'idf', 'docs_freq', 'query_freq2/docs_freq']))


    dt.to_csv(csv_path, index=False)





if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage : generation_idf.py <fichier_docs.csv> <fichier_query.csv> <out_path.csv> <sort_criteria> \n where sort_criteria = 'query_freq2' or 'idf' or 'docs_freq' or 'alpha' or 'query_freq2/docs_freq'")
        
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])