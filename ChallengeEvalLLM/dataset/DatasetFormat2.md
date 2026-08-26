# Main V1 

Dataset issu des données du Challenge RAG de EvalLLM2026. 

## Construction
- Extraction du texte des pdf à l'aide de `pymupdf4llm`
- Découpe avec `MarkdownTextSplitter` de `langchain_text_splitter` (chunk_size=500, chunk_overlap=150)
- Documents extraits automatiquement à l'aide E5 et ChromaDB
- Selection des questions et documents à la main à partir des extraction automatiques

## Format
3 fichiers:
    - paires_mainV1.csv 
    - docs_mainV1.csv
    - queries_mainV1.csv

### paires_mainV1.csv
- q_id (int) : identifiant de question
- question (str) : texte de la question
- doc_id (int) : identifiant de ducument
- doc_name (str) : nom du fichier pdf d'origine
- page_number (int) : numéro (absolu) de la page d'origine
- chunk_id (int) : identifiant de l'extrait
- text (str) : texte de l'extrait
- pertinent (bool) : pertinent du document pour la question

Infos:
- 52 entrées
- Autant de documents pertinents que non pertinents
- 1 document pertinent/ non-pertinent par question
- 52 extraits
- 26 questions

### docs_mainV1.csv
- doc_id (int) : identifiant de ducument
- doc_name (str) : nom du fichier pdf d'origine
- page_number (int) : numéro (absolu) de la page d'origine
- chunk_id (int) : identifiant de l'extrait
- text (str) : texte de l'extrait

### queries_mainV1.csv
- q_id (int) : identifiant de question
- question (str) : texte de la question
