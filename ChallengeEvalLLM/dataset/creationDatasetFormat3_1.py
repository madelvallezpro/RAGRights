#!/usr/bin/env python
# coding: utf-8

# # Construction à la min d'un petit dataset maitrisé issu de challenge

# In[48]:


import pandas as pd


# In[49]:


docsV2 = pd.read_csv("../docsV2.csv")


# In[30]:


tmp = docsV2[ docsV2.doc_name.str.contains("Guide_sensi")]
tmp #[tmp.page_number==3]
#docsV2.iloc[9200].text


# ## Creation DB

# In[64]:


db = pd.DataFrame(columns=["q_id", "question", "doc_id", "doc_name", "page_number", "chunk_id", "text", "pertinent"])


# In[65]:


tmp = pd.DataFrame({
               "q_id" : [100]*(27679 - 27665),
               "question" : ["Quelles sont les trois principales catégories de limitations techniques affectant les systèmes de drones, et comment chacune influence-t-elle l'efficacité opérationnelle de ces vecteurs ?"]*(27679 - 27665),
               "doc_id" : list(docsV2.iloc[27665:27679].doc_id),
               "doc_name" : list(docsV2.iloc[27665:27679].doc_name),
               "page_number" :list(docsV2.iloc[27665:27679].page_number),
               "chunk_id" :list(docsV2.iloc[27665:27679].chunk_number),
               "text" : list(docsV2.iloc[27665:27679].text),
               "pertinent" : [True]*(27679 - 27665)
           })
db = pd.concat([db,tmp], axis=0)
db


# In[66]:


tmp = pd.DataFrame({
               "q_id" : [100]*(37065 - 37059),
               "question" : ["Quelles sont les trois principales catégories de limitations techniques affectant les systèmes de drones, et comment chacune influence-t-elle l'efficacité opérationnelle de ces vecteurs ?"]*(37065 - 37059),
               "doc_id" : list(docsV2.iloc[37059:37065].doc_id),
               "doc_name" : list(docsV2.iloc[37059:37065].doc_name),
               "page_number" :list(docsV2.iloc[37059:37065].page_number),
               "chunk_id" :list(docsV2.iloc[37059:37065].chunk_number),
               "text" : list(docsV2.iloc[37059:37065].text),
               "pertinent" : [False]*(37065 - 37059)
           })
db = pd.concat([db,tmp], axis=0)
db


# In[67]:


tmp = pd.DataFrame({
               "q_id" : [100]*(3606 - 3598),
               "question" : ["Quelles sont les trois principales catégories de limitations techniques affectant les systèmes de drones, et comment chacune influence-t-elle l'efficacité opérationnelle de ces vecteurs ?"]*(3606 - 3598),
               "doc_id" : list(docsV2.iloc[3598:3606].doc_id),
               "doc_name" : list(docsV2.iloc[3598:3606].doc_name),
               "page_number" :list(docsV2.iloc[3598:3606].page_number),
               "chunk_id" :list(docsV2.iloc[3598:3606].chunk_number),
               "text" : list(docsV2.iloc[3598:3606].text),
               "pertinent" : [False]*(3606 - 3598)
           })
db = pd.concat([db,tmp], axis=0)
db


# In[70]:


db.reset_index(drop=True, inplace=True)


# In[71]:


db.to_csv("paires_mainV2.csv", index=True)


# ## Generation docs et queries

# In[73]:


new_paires = pd.read_csv("paires_mainV2.csv", index_col=0)
new_paires


# In[74]:


docs = new_paires[["doc_id", "doc_name", "page_number", "chunk_id", "text"]]
docs.head()


# In[75]:


queries = new_paires[["q_id", "question"]]
queries.drop_duplicates(inplace=True, ignore_index=True)
queries.head()


# In[76]:


docs.to_csv("docs_mainV2.csv", index=True)
queries.to_csv("queries_mainV2.csv", index=True)

