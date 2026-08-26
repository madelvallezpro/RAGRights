# Main V3 

Dataset issu des données du Challenge RAG de EvalLLM2026. 

## Construction
- Extraction du texte des pdf à l'aide de `pymupdf4llm`
- Découpe avec `MarkdownTextSplitter` de `langchain_text_splitter` (chunk_size=500, chunk_overlap=150)
- Documents extraits automatiquement à l'aide E5 et ChromaDB
- Selection des questions et documents à la main à partir des extraction automatiques

## Format
3 fichiers:
    - paires_mainV3.csv 
    - docs_mainV3.csv
    - queries_mainV3.csv

### paires_mainV3.csv
- q_id (int) : identifiant de question
- question (str) : texte de la question
- doc_id (int) : identifiant de ducument
- doc_name (str) : nom du fichier pdf d'origine
- page_number (int) : numéro (absolu) de la page d'origine
- chunk_id (int) : identifiant de l'extrait
- text (str) : texte de l'extrait
- pertinent (bool) : pertinent du document pour la question

Infos:
- 20 entrées
- Autant de documents pertinents que non pertinents
- Textes issus de 3 pdfs
- 20 extraits
- 1 question

### docs_mainV3.csv
- doc_id (int) : identifiant de ducument
- doc_name (str) : nom du fichier pdf d'origine
- page_number (int) : numéro (absolu) de la page d'origine
- chunk_id (int) : identifiant de l'extrait
- text (str) : texte de l'extrait

### queries_mainV3.csv
- q_id (int) : identifiant de question
- question (str) : texte de la question

## Analyse 
### Question
1 question : 
> Quels sont les défis majeurs liés à l’utilisation d’une intelligence artificielle auto-apprenante dans les systèmes d’armes, et en quoi ces défis remettent-ils en cause les méthodes traditionnelles de développement et de validation des technologies militaires ?

### Thématique
Sujet pas spécifique à la défense mais appliqué à la défense : Intelligence Artificielle appliquée aux outils et pratiques de la défense et notamment à la guerre.

Thèmatique des 3 pdf:
- IA pour la défense : enjeux
- Aviation civile
- usage des ballons (aérostats et dirigeables) dans l'histoire et rebond de l'usage

### Statistique
| Mot     | Fréquence| TF-IDF         |
|------------|---|--------------------|
|système     |13 |0.06480086088326986 |
|transport   |9  |0.05957370634266266 |
|militaire   |9  |0.0488148141908528  |
|force       |8  |0.048789708865220195|
|aérien      |8  |0.05223144426877953 |
|automatiser |7  |0.04028923862758367 |
|artificiel  |6  |0.04046189336007796 |
|intelligence|6  |0.04046189336007796 |
|emploi      |6  |0.03775763430881781 |
|domaine     |6  |0.03862181838643274 |

_Système_ est essentielement issu de l'expression _système autonome_ dans les documents positofs (issus du numéro sur l'emploi des Ia et systèmes automatisés du Centre interarmées de concepts, de doctrines et d’expérimentations). La seule exception est pour _système High Altitude pseudo-satellite (HAPS)_ issu du document sur les ballons.

L'entièreté des occurences de _transport_ sont issues du document sur l'aviation civile.

Les occurences de _militaire_ sont issues des documents sur les sytèmes autonomes et les ballons.