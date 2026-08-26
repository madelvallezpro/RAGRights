#!/usr/bin/env python
# coding: utf-8

# # Construction à la min d'un petit dataset maitrisé issu de challenge

# In[1]:


import pandas as pd


# In[2]:


docsV2 = pd.read_csv("../docsV2.csv")


# In[18]:


tmp = docsV2[ docsV2.doc_name.str.contains("20180719")]
tmp[tmp.page_number==19] 
docsV2.iloc[13620].text


# ## Creation DB

# In[8]:


db = pd.DataFrame(columns=["q_id", "question", "doc_id", "doc_name", "page_number", "chunk_id", "text", "pertinent"])


# In[ ]:


tmp = pd.DataFrame({
               "q_id" : [200]*(2),
               "question" : ["Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?"]*2,
               "doc_id" : list(docsV2.iloc[13591:13593].doc_id),
               "doc_name" : list(docsV2.iloc[13591:13593].doc_name),
               "page_number" :list(docsV2.iloc[13591:13593].page_number),
               "chunk_id" :list(docsV2.iloc[13591:13593].chunk_number),
               "text" : list(docsV2.iloc[13591:13593].text),
               "pertinent" : [True]*(2)
           })
db = pd.concat([db,tmp], axis=0)
db


# In[12]:


tmp = pd.DataFrame({
               "q_id" : [200]*(2),
               "question" : ["Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?"]*2,
               "doc_id" : list(docsV2.iloc[13593:13595].doc_id),
               "doc_name" : list(docsV2.iloc[13593:13595].doc_name),
               "page_number" :list(docsV2.iloc[13593:13595].page_number),
               "chunk_id" :list(docsV2.iloc[13593:13595].chunk_number),
               "text" : list(docsV2.iloc[13593:13595].text),
               "pertinent" : [True]*(2)
           })
db = pd.concat([db,tmp], axis=0)
db


# In[14]:


tmp = pd.DataFrame({
               "q_id" : [200]*4,
               "question" : ["Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?"]*4,
               "doc_id" : list(docsV2.iloc[13609:13613].doc_id),
               "doc_name" : list(docsV2.iloc[13609:13613].doc_name),
               "page_number" :list(docsV2.iloc[13609:13613].page_number),
               "chunk_id" :list(docsV2.iloc[13609:13613].chunk_number),
               "text" : list(docsV2.iloc[13609:13613].text),
               "pertinent" : [True]*4
           })
db = pd.concat([db,tmp], axis=0)
db


# In[16]:


tmp = pd.DataFrame({
               "q_id" : [200],
               "question" : ["Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?"],
               "doc_id" : [docsV2.iloc[13616].doc_id],
               "doc_name" : [docsV2.iloc[13616].doc_name],
               "page_number" :[docsV2.iloc[13616].page_number],
               "chunk_id" :[docsV2.iloc[13616].chunk_number],
               "text" : [docsV2.iloc[13616].text],
               "pertinent" : [True]
           })
db = pd.concat([db,tmp], axis=0)
db


# In[19]:


tmp = pd.DataFrame({
               "q_id" : [200],
               "question" : ["Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?"],
               "doc_id" : [docsV2.iloc[13620].doc_id],
               "doc_name" : [docsV2.iloc[13620].doc_name],
               "page_number" :[docsV2.iloc[13620].page_number],
               "chunk_id" :[docsV2.iloc[13620].chunk_number],
               "text" : [docsV2.iloc[13620].text],
               "pertinent" : [True]
           })
db = pd.concat([db,tmp], axis=0)
db


# In[ ]:


tmp = pd.DataFrame({
               "q_id" : [200]*(2),
               "question" : ["Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?"]*2,
               "doc_id" : list(docsV2.iloc[13591:13593].doc_id),
               "doc_name" : list(docsV2.iloc[13591:13593].doc_name),
               "page_number" :list(docsV2.iloc[13591:13593].page_number),
               "chunk_id" :list(docsV2.iloc[13591:13593].chunk_number),
               "text" : list(docsV2.iloc[13591:13593].text),
               "pertinent" : [False]*(2)
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

