# Main V2 

Dataset issu des données du Challenge RAG de EvalLLM2026. 

## Construction
- Extraction du texte des pdf à l'aide de `pymupdf4llm`
- Découpe avec `MarkdownTextSplitter` de `langchain_text_splitter` (chunk_size=500, chunk_overlap=150)
- Documents extraits automatiquement à l'aide E5 et ChromaDB
- Selection des questions et documents à la main à partir des extraction automatiques

## Format
3 fichiers:
    - paires_mainV2.csv 
    - docs_mainV2.csv
    - queries_mainV2.csv

### paires_mainV2.csv
- q_id (int) : identifiant de question
- question (str) : texte de la question
- doc_id (int) : identifiant de document
- doc_name (str) : nom du fichier pdf d'origine
- page_number (int) : numéro (absolu) de la page d'origine
- chunk_id (int) : identifiant de l'extrait
- text (str) : texte de l'extrait
- pertinent (bool) : pertinent du document pour la question

Infos:
- 27 entrées
- Autant de documents pertinents que non pertinents
- Textes issus de 3 pdfs
- 28 extraits
- 1 question

### docs_mainV2.csv
- doc_id (int) : identifiant de ducument
- doc_name (str) : nom du fichier pdf d'origine
- page_number (int) : numéro (absolu) de la page d'origine
- chunk_id (int) : identifiant de l'extrait
- text (str) : texte de l'extrait

### queries_mainV2.csv
- q_id (int) : identifiant de question
- question (str) : texte de la question

## Contenu/ Stats
Construction des données:
- 1 question, 3 pdf (limitations matérielles du drone, code de la défense - matériel de guerre, fausses infos pdt les JO/JP)
- 50% de textes pertinents
- 28 paires

Question : 
> Quelles sont les trois principales catégories de limitations techniques affectant les systèmes de drones, et comment chacune influence-t-elle l'efficacité opérationnelle de ces vecteurs ?



|word      | freq | TF-IDF |
|----------|---|------------------|
|**matériel**  |16 |0.0627430130086598|
|**système**   |11 |0.0542242908052481|
|**limitation**|6  |0.0495565089630139|
|**drone**     |10 |0.0441649020535004|
|défense   |10 |0.0440955901918619|
|prendre   |6  |0.0425658179515979|
|compte    |5  |0.0404563824330286|
|action    |8  |0.0401684995180441|
|article   |9  |0.0400092952253956|
|ministre  |8  |0.03913497111578  |
|aérien    |7  |0.0366033210120314|
|acteur    |6  |0.0337084867312698|
|guerre    |8  |0.0336043799517422|


