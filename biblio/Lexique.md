# Lexique et définitions rencontrées dans la bibliographie

## Continual Learning
[Hou et al., 2025] "Continual learning refers to the capability of a machine learning model to learn and adapt to new
information, without compromising its performance on previously learned tasks"

## Continuous Learning
N'existe pas !

## Extraction d'information
[Saez 2023] Information Retrieval (IR) is about finding relevant documents for
a specific user’s information need from a corpus of documents.

## Interprétabilité

## Interprétabilité mécanique
"Mechanistic interpretability is an emerging diagnostic approach for neural models that has gained traction in broader natural language processing domains. This paradigm aims to provide attribution to components of neural systems" [Parry et al., 2025]

## Question Answering (et variantes)
Tâche d'extraction de document (IR) et de RAG qui vise à répondre à une question à l'aide des documents de la base de données. On retrouve plusieurs définitions et différentes variantes

([Petroni et al., 2020] - KILT) "extractive question answering, can copy the output directly from a Wikipedia page"
([Lewis et al., 2020]) "extractive QA paradigm, where answers are extracted spans from retrieved documents"

### Long-form QA
([Petroni et al., 2020] - KILT à propos de ELI5) "ELI5 (Fan et al., 2019b) is a collection of question-answer-evidence triples where the questions are complex, and the answers are long, explanatory, and free-form."

### Multi-hop QA
([Xu et al., 2024] - SearChain) "first plan each sub-question and then solve them, they are not suitable for scenarios where the next sub-question needs the answer of the previous sub-questions to generate, which is common for complex knowledge-intensive tasks"

### Open Domain QA
([Thakur et al., 2021] - BEIR) "Retrieval in open domain question answering [8] is the task of retrieving the correct answer for a question, without a predefined location for the answer. In open-domain tasks, model must retrieve over an entire knowledge source (such as Wikipedia). We consider the question as input and the passage containing the answer as output"
([Lewis et al., 2020]) "“Closed-Book QA” approaches [52], which, like RAG, generate answers, but which do not exploit retrieval, instead relying purely on parametric knowledge"
([Petroni et al., 2020] - KILT) 
- "in open-domain question answering (Chen et al.,2017) models need to find answers within a large corpus of text"
- "Open domain Question Answering (Chen et al., 2017) is the task of producing the correct answer
for a question, without a predefined location for the answer."