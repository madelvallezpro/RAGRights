#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_tavily import TavilySearch
from langchain_cohere import CohereRerank
from langchain_core.output_parsers import StrOutputParser
from typing_extensions import TypedDict
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
# from rank_bm25 import BM25Okapi
from flair.data import Sentence
from flair.models import SequenceTagger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langgraph.graph import StateGraph

from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

import os


# In[2]:


local_llm = 'llama3'


# In[3]:


# Création des retriver pour les titre/summary et pour les documents
model_name = "intfloat/e5-small"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)
vectordb = Chroma(persist_directory="corpus_db", embedding_function = hf)
titledb = Chroma(persist_directory="title_db", embedding_function=hf)
top_retrieve = 20

# Définition documents
retriever = vectordb.as_retriever(search_type="mmr",
        search_kwargs={'k': top_retrieve, 'lambda_mult': 0.25}
)
title_retriever = titledb.as_retriever() # retriever titre/summary


# Outils pour le reranking
compressor = CohereRerank(model = 'rerank-multilingual-v3.0', top_n = top_retrieve, cohere_api_key=os.getenv("COHERE_API_KEY"))

vectorizer = TfidfVectorizer()
tagger = SequenceTagger.load("hmbert/flair-hipe-2022-newseye-fr")


# In[ ]:





# In[4]:


# Implem du reranker
def rerank(docs, question):
    rerank_docs = compressor.compress_documents(docs, question)
    texts = [doc.page_content for doc in rerank_docs]
    print(rerank_docs[0].metadata)
    ners = [doc.metadata['title'] for doc in rerank_docs]
    sentence = Sentence(question)
    tagger.predict(sentence)
    sen_dict = sentence.to_dict(tag_type='ner')
    aner = " ".join([ner['labels'][0]['value'] for ner in sen_dict['entities']] + ['O'])

    all_ner = ners + [aner]
    tfidf_matrix = vectorizer.fit_transform(all_ner)
    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]
    ner_scores = cosine_similarity(query_vector, doc_vectors).flatten()
    co_scores = np.array([float(doc.metadata['relevance_score']) for doc in rerank_docs])

    scores = 0.8 * co_scores + 0.2 * ner_scores
    max_idx = np.argsort(-scores)
    final_docs = []
    for idx in max_idx[:3]:
        if scores[idx] > 0.5:
            final_docs.append(texts[idx])
    return final_docs


# In[5]:


# Définition du LLM et du prompt à compléter
prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
    Question: {question} 
    Context: {context} 
    Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "document"],
)

llm = ChatOllama(model=local_llm, temperature=0.3)

rag_chain = prompt | llm | StrOutputParser()


# In[ ]:


# Assemblage des éléments
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents 
    """
    question : str
    generation : str 
    title: List[str]
    documents : List[str]


def title_retrieve(state):
    """
    Retrieve titles from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---TITLE RETRIEVE---")
    question = state['question']

    titles = title_retriever.invoke(question)
    title = [t.page_content for t in titles]
    print(f"{len(title)} titles retrieved")
    return {'title': title, 'question': question}
    # return {'question': question}
    

def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    title = state['title']
    docs = retriever.invoke(question)
    
    print(f"T{len(docs)} titles retieved")
    print("---RERANK---")
    refined_docs = rerank(docs, question)
    return {"documents": refined_docs, "question": question}

def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}
    


# In[7]:


workflow = StateGraph(GraphState)

workflow.add_node("title_retrieve", title_retrieve)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)


# In[8]:


# On ajoute les lien entre les différentes étapes/noeuds
workflow.set_entry_point("title_retrieve")
workflow.add_edge("title_retrieve", "retrieve")
workflow.add_edge("retrieve", "generate")


# In[9]:


app = workflow.compile()

inputs = {"question": "Qui est Antoine Meillet"}
print(inputs)
for output in app.stream(inputs):
    for key, value in output.items():
        pprint(f"Finished running: {key}:")
pprint(value["generation"])


# In[ ]:




