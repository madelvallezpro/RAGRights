# Overview du projet pour le Challenge RAG@EvalLLM
## Biblio
### Dataset
Pas de dataset générique en français pour IR et/ou QA

Dataset multilingue avec une partie en français:
- mC4 (dataset d'entraînement de mT5) : textes notamment en français (/!\ pas IR)
- **MIRACL** (IR)
    - page web : https://project-miracl.github.io/
    - github : https://github.com/project-miracl/miracl
    - papier : https://arxiv.org/abs/2210.09984
    - huggingface : https://huggingface.co/datasets/miracl/miracl
    - un split par langue :-)
- MKQA : QA dataset /!\ pas de documents fournis /!\
    - papier : https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00433/108607/MKQA-A-Linguistically-Diverse-Benchmark-for
    - 10 000 requêtes dans 25 langues chacune, 
    - HF : https://huggingface.co/datasets/apple/mkqa
    - github : https://github.com/apple/ml-mkqa/tree/main
- BERGEN : Rag Bench focus on QA
    - papier : https://arxiv.org/abs/2407.01102
    - github : https://github.com/naver/bergen
    - ensemble de datasets préexistants dont deux multilingues : MKQA et XOR-TyDi QA
    - 
- XOR-QA : Cross-lingual Open-Retrieval QA
    - multilingual
    - papier : https://aclanthology.org/2021.naacl-main.46/
    - code & data : https://nlp.cs.washington.edu/xorqa/
    - /!\ *"This work extends open-retrieval question answering to a cross-lingual setting enabling questions from one language to be answered via answer content from another language."*
    - Extension de TyDi QA en ne restreignant pas la recherche dans une langue en particulier (les corrections ont été adaptées en conséquence)
- [Clark et al., 2020] TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages
    - papier : https://arxiv.org/abs/2003.05002
    - La question doit être répondue à l'aide des documents de la langue cible. L'objectif est de ne pas reposer sur des capacités de traduction. 
    - github : https://github.com/google-research-datasets/tydiqa
- [Welbl et al., 2017] SCIQ : Crowdsourcing Multiple Choice Science Questions
    - Question (Physique, Chimie Biologie) niveau collège-début fac
    - Anglais
    - HF : https://huggingface.co/datasets/allenai/sciq
    - les explications rédigées pourraient servir de documents, on peut alors se passer des 4 réponses possibles (dont la bonne réponse) (c'est un QCM à l'origine)



Travaux de RAG en français de spécialité (introduisant un dataset):
- [Mnassri et al., 2025] RAG and Recall: Multilingual Hate Speech Detection with Semantic Memory
    - Multilingual hate speech detection (Fr, Arabic, En) ~> classification !!
    - deux modèles : HS-RAG et HS-MemRAG (pour réduire les retrievals redondants)
    - LLaMA-3-8B + Langchain&Chroma
    - training free
    - papier : https://aclanthology.org/2025.woah-1.20/
    - pas de code/ modèle accessible
    - dataset utilisé : https://huggingface.co/datasets/manueltonneau/french-hate-speech-superset ~> assez loin de ce qu'on cherche...

### IR/ ID
À partir du survey [Fan et al. 2024]:
- [Lewis et al 2020] DPR+BART
    - DPR pas compatible avec MechIR
    - facebook/dpr-question_encoder-single-nq-base, facebook/rag-token-nq
- [Khandelwal et al. 2019] Generalization through Memorization: Nearest Neighbor Language Models
    - https://arxiv.org/abs/1911.00172
    - code : https://github.com/urvashik/knnlm (/!\ entraînement à refaire!!!)
- [Borgeaud et al., 2022] Improving Language Models by Retrieving from Trillions of Tokens  
    - papier https://proceedings.mlr.press/v162/borgeaud22a/borgeaud22a.pdf
    - RETRO
    - Modèle InstructRETRO basé sur RETRO : https://huggingface.co/nvidia/retro-8b-instruct-4k
- [Glass et al. 2022] 
    - modele : https://huggingface.co/ibm-research/re2g-reranker-triviaqa
    - ibm-research/re2g-reranker-nq
    - code? https://github.com/IBM/kgi-slot-filling
    - l'extraction est elle compatible avec notre projet??
- [Shi et al., 2024] RePlug (pour les concpets mis pas compatible MechIR car Contriver)
    - papier : https://aclanthology.org/2024.naacl-long.463/


### RAG
- [Bellart & Deleruyelle 2025] TalanSeeker : Application de l'architecture RAG pour la sélection de profils en conseil
    - FR
    - papier : https://editions-rnti.fr/?inprocid=1003045
    - Outil RAG complet pour selection de CV étant donné une requête
    - Archi partiellement dispo sur Github (https://github.com/TalanRecherche/Talanseeker-Backend) **pour utilisation** (pas appropriation)
    - dataset : base de CV synthétiques ~> pas ce qu'on cherche
- [Tran et al., 2025] Génération augmentée de récupération pour les journaux historiques
    - FR
    - papier : https://inrap.hal.science/INSA-CVL/hal-04796088v1
    - résumé : https://talnarchives.atala.org/ateliers/2025/CORIA/37.html
    - Embeddings par mE5-small, stockés avec Chroma, cosine-similarity. Première extraction sur les titres puis 2e extraction sur les documents (si on a obtenu des titres avec pertinence suffisante, sinon, recherche web). Reranking des résultats obtenus. Le tout est envoyé dans LLaMA3 ~> Beaucoup d'outils !!! Archi assez élaborée!!
    - GitHub : https://github.com/trungv28/Retrieval-Augmented-Generation-for-historical-newspapers/tree/main 
    - **Compatible MechIR**
- [Xiao et al., 2022] RetroMAE: Pre-Training Retrieval-oriented Language Models Via Masked Auto-Encoder
    - **EN ?**
    - github : https://github.com/staoxiao/RetroMAE
    - papier /!\ À LIRE /!\ : https://arxiv.org/abs/2205.12035
- [Nouali et al., 2025] Exploration du RAG pour la génération de réponses à des questions en contexte éducatif: étude sur les données SCIQ
    - Opposer LLM seul à LLLM+IR sur les données SciQ
    - LLM seuls : Llama 3 8b, Mistral 7b
    - Archi RAG : Moteur ElasticSearch avec BM25 + les mêmes LLMs, prompt engineering pour l'augmentation, extraction des k=10 meilleurs passages, 
    - **/!\ anglais**
    - /!\ pas de code accessible
- RESSOURCE TRÈS INTERESSANTE 
    - /!\ vigilance sur les droit 
    - /!\ compatible MechIR???
    - https://github.com/OpenClassrooms-Student-Center/8532116-mettez-en-place-un-rag-pour-un-llm/tree/main
- [Izacard & Grave 2020] DPR&BM25 + T5 pour OpenDomain QA
    - papier : https://aclanthology.org/2021.eacl-main.74.pdf
    - code : https://github.com/facebookresearch/fid
    - /!\ pas de modèle pré-entrainé!! 

### LLM
Multilingue:
- E5 multilingue (encodeur)
    - HF : https://huggingface.co/intfloat/multilingual-e5-small
    - papier mE5 : https://arxiv.org/abs/2402.05672
    - papier E5 (archi) : https://arxiv.org/abs/2212.03533
    - github : https://github.com/microsoft/unilm/tree/master/e5
- [Xue et al., 2021] mT5 multilingue text2text (basé T5)
    - papier : https://aclanthology.org/2021.naacl-main.41/
    - entraînement de l'archi T5 avec une extension du dataset d’entraînement de T5 (C4 devient mC4)
    - github : https://github.com/google-research/multilingual-t5
    - doc HF : https://huggingface.co/docs/transformers/model_doc/mt5
    - model HF : https://huggingface.co/google/mt5-base
- [Le Scao et al., 2022] BLOOM: A 176B-Parameter Open-Access Multilingual Language Model
    - décoduer only
    - multilingue
    - modèle : https://huggingface.co/bigscience/bloom
    - papier : https://arxiv.org/abs/2211.05100

Français:
- Mistral7B 2023
- [Zhang et al. 2025] Vers une optimisation de RAG en français : conception d'un reranker open source, fine-tuning et évaluation (https://hal.science/hal-05133472v1)
    - juste rerank
    - impem et entraînement d'un reranker à la sortie d'un distillRoBERTa
    - code limité mais disponible et plutôt commenté
- [Segonne et al. 2024] Jargon: A Suite of Language Models and Evaluation Tasks for French Specialized Domains
    - https://hal.science/hal-04535557
    - code : https://github.com/PantagrueLLM/Jargon/
    - modèle : https://huggingface.co/PantagrueLLM
    - Français et spécialisation (law, health, speech detection)
    - classifictaion (juste utilisable pour IR)


### Évaluation
- [Zhou & Mulhem & Schwab 2026] TempPerturb-Eval: On the Joint Effects of Internal Temperature and External Perturbations in RAG Robustness
    - évaluer l'impact de la température et des perturbations sur la qualité d'un modèle RAG et les interactions entre les variations de ces deux paramètres
    - RAGs étudiés : gpt-3.5-turbo, gpt-4o, Llama-3.1-8B-Instruct, Llama-3.2-1B-Instruct, deepseek-reasoner
    - papier : https://arxiv.org/abs/2512.01183
- [Park & Lee 2025] Investigating Language Preference of Multilingual RAG Systems 
    - multilingual
    - papier : https://aclanthology.org/2025.findings-acl.295/
    - Retriever analysés:
        - BGE-m3 [Chen et al., 2024]
        - paraphrase-multilingual-MiniLM-L12-v2
        -  paraphrase-multilingual-mpnet-base-v2
    - Générateurs analysés
        - aya-expanse-8b [Dang et al., 2024]
        - qwen 2.5-7B Instruct [Team 2024]
        - Phi-4 14B [Abdin et al., 2024]
        -  Llama-3.1-8B-Instruct [Dubey et al., 2024]
    - github : https://github.com/jeonghyunpark2002/LanguagePreference
- [Bouchiba 2025] Vers des RAGs intégrant véracité, subjectivité et explicabilité
    - papier : https://talnarchives.atala.org/ateliers/2025/IAEDU/208.html
    - projet de thèse "Explainable Retrieval Augmented Generation that supports Veracity and Subjectivity : X-RAG-VS". Pas de code ni de détail disponible pour l'instant

### Explicabilité
- [Zhou & Mulhem & Schwab 2025] Explicabilité par Perturbations pour les Systèmes RAG
    - Overview des méthodes d'explication générales puis pour le RAG
    -> *Gradient Guided Prompt Perturbation [Hu et al., 2024] pourrai être intéressant à exploiter avec MechIR*
    - Catégorisation des perturbations pour l'IR -> *apporter des idées de perturbations pour MechIR*
    - papier : https://talnarchives.atala.org/ateliers/2025/DIAGLLM/193.html
- [Vast et al., 2025] Comprendre la Nature des Signaux de Correspondance dans les Modèles Neuronaux pour la RI
    - Étude de la façon dont les modèles de RI construisent et traitent les signaux. Par masking des matrices d'attention
    - modèle utilisé/ analysé : MonoBERT (entraîné sur le RI avec MS-MARCO)
    - papier : https://talnarchives.atala.org/ateliers/2025/CORIA/1.html

## Structure
### Dataset
À construire à partir de la biblio : MIRACL et TyDi-QA

### Architecture
Objectif : faire simple (IR + LLM sans augmentation pour l'instant)
#### Extraction d'information / de document

#### Génération de réponse

### Audit avec MechIR

### Corrections issues de l'audit avec MechIR

### Comparaison du modèle avant et après

### Évaluation dans le cadre du Challenge RAG@EvalLLM