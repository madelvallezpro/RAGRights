#!/usr/bin/env python
# coding: utf-8

# # Extraction des données et création de la base de donnée pour les autres notebooks

# In[1]:


from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from datasets import load_dataset
from tqdm import tqdm


# In[2]:


print("---Load Dataset & Embedder---")
db_size = 100000
batch_size = 5000
dataset = load_dataset("miracl/miracl-corpus", "fr", split="train", trust_remote_code=True, streaming=True)
model_name = "intfloat/e5-small"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)


# In[15]:


def transfer(start, end):
    data = list(dataset.skip(start).take(end-start))
    docs = []
    ids = []
    for idx in range(end-start):
        doc = Document(page_content=data[idx]['text'],
                    metadata={
                        'title': data[idx]['title']
                    })
        docs.append(doc)
        ids.append(data[idx]['docid'])
    return docs, ids


# In[16]:


print("---Docs extraction---")
docs, ids = transfer(0, batch_size)
persist_directory = "corpus_db"

vectordb = Chroma.from_documents(documents=docs, embedding=hf, ids = ids, persist_directory=persist_directory) 


# In[ ]:


def batch_process(batch_size):
    for i in tqdm(range(batch_size, db_size, batch_size)):
        docs, ids = transfer(i, i+batch_size)
        vectordb.add_documents(documents = docs, ids = ids)


# In[ ]:


print("---Batching Documents---")

batch_process(batch_size)


# In[ ]:


print("---Titles extraction---")

metadata = vectordb.get(include=['metadatas'], limit=20, offset=0)['metadatas']

title_set = set([doc['title'] for doc in metadata])

offset = len(title_set)
limit = batch_size
while len(title_set) == limit:
    metadata = vectordb.get(include=['metadatas'], limit=limit, offset=offset)['metadatas']
    title_set.update([doc['title'] for doc in metadata])
    # mise à jour des bornes d'extraction pour le batch suivant
    offset += len(title_set)


docs = []
for title in tqdm(title_set):
    doc = Document(page_content=title)
    docs.append(doc)
persist_directory = "title_db"
titledb = Chroma.from_documents(documents=docs, embedding=hf, persist_directory=persist_directory)

