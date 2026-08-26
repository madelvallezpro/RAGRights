# Récupération et mise en forme des données pour le challenge RAG @ evalLLM¶

import pymupdf4llm
import pandas as pd
from langchain_text_splitters import MarkdownTextSplitter
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

md_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=150) # le choix de la taille et de l'overlap est justifié par les contraintes de E5 (entrée de 512 token) affiner ces hyperparamètres pourrait parfaire le modèle
doc_df = pd.DataFrame( columns=["doc_id","doc_name", "page_number", "chunk_number", "text"])


mypath = "./data_challenge/Corpus_raw"
onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and ".pdf" in f)]


doc_id = 0
for file in tqdm(onlyfiles):
    chunk_number = 0
    doc = pymupdf4llm.to_markdown(
        join(mypath,file),
        page_chunks = True, # "output will be a list of Document.page_count dictionaries (one per page)"
        # header = False, # ne traite pas le header
        # footer = False, # ne traite pas le footer
        #pages = range(1)
        )
    for page in doc:
        textes = md_splitter.split_text(text=page["text"])
        n = len(textes)
        doc_df = pd.concat([doc_df,
                        pd.DataFrame({
                            "doc_id" : [int(doc_id)]*n,
                            "doc_name" : [page["metadata"]["file_path"]]*n,
                            "page_number" : [int(page["metadata"]["page"])]*n,
                            "chunk_number" : [int(i+chunk_number) for i in range(n)],
                            "text" : textes
                        })], ignore_index=True)
        chunk_number += len(textes)
    doc_id+=1

doc_id_str = [str(doc_id) for doc_id in doc_df["doc_id"]]
page_nb_str = [str(page_nb) for page_nb in doc_df["page_number"]]
chunk_nb_str = [str(chunk_nb) for chunk_nb in doc_df["chunk_number"]]

ids = ["#".join([doc_id_str[i], page_nb_str[i], chunk_nb_str[i]]) for i in range(len(doc_id_str))]

doc_id_str = [str(doc_id) for doc_id in doc_df["doc_id"]]
page_nb_str = [str(page_nb) for page_nb in doc_df["page_number"]]
chunk_nb_str = [str(chunk_nb) for chunk_nb in doc_df["chunk_number"]]

ids = ["#".join([doc_id_str[i], page_nb_str[i], chunk_nb_str[i]]) for i in range(len(doc_id_str))]

doc_df.insert(0,"id",pd.Series(ids))

doc_df.to_csv("data_challenge/docs.csv")