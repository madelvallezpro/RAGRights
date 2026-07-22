# Notes des idées et choses à intégrer pour le rapport

## À mentionner dans le rapport
- Génération de questions pour l'entraînement : biais dans les questions (temps) et dans les sujet (lecture rapide des données)
- Les constantes de rerank et chunking ont été choisies arbitrairement ou par contrainte technique. Il serai intéressant de les optimiser. Ça n'a pas été fait faut de temps et pas choix de s'intéresser à d'autres choses
- les éléments pris en compte pour l'extraction du vocabulaire caractéristique (quand commencer, quand s’arrêter, quel biais de compréhension)
- présentation de l'archi utilisée (+ présentation de RAG4HN??)
- justifier utilisation de Md comme format de texte
- dans les mesure d'effet d'une perturbation, la baseline change un peu de forme (dû à kde ?). Les petites perturbations pourraient être des artefacts liés à l'**affichage** de kde 

## Éléments bibliographiques
- E5
- Cohere
- RAG
- llama3
- explicabilité rapidement


# Récapitulatif du stage

## Introduction

### Contexte du stage
- LIFO
- Challenge RAG@EvalLLM 
- Sorties et Événements au cours du stage
  - TransIA à Tours [Cahier Minerve]
  - Journée GDR TAL-I (Jussieu) [Cahier Minerve]
  - 2nd Symposium on Mental Health and AI [R16/02]
  - Place du Numérique (ambassadrice)
  - Journée CA (présentation) [Cahier Minerve]

### Outils utilisés
- CaSciModOT et Mirev pour l'execution des architectures et protocoles long/lourds
- HuggingFace, PyTorch, TransformerLens
- Scripts python et Notebooks Python
- git, gogit
- IA : reformulation, exploration de la littérature, traduction, rédaction de scripts simple (parfois améliorés à la main)

### Difficultés Techniques
- Contraintes d'outil de CaSciModOT (conda-forge)
- Reprendre le code de qq1 
  - pas de contact (code recherche)
  - montée en version nécessaire pour l'exploitation des librairies (conda-forge)
- Conflit de requirements entre deux pans du projet (difficultés à installer un environnement fonctionnel)
- Modèles entrainés sur des données anglophone -> données à traiter francophones

### Introduction du sujet
TODO

## État de l'art

### RAG et RALLM
- définition, enjeux visés
- RAG vs RALLM [Fan+23]
- Architecture RAG (intuition et archi complete) [Fan+23, R9/02]
  - extraction (base à préparer si bi-encodeur)
  - generation
  - amélioration
  - intégration
- Tâches associées (QA, IR) [Git-Csv]
- Quelques approches vues [R16/02]
  - Multimodal [Lui+25]
  - Chain of Thought [Xu+24]
  - Gestion BDD dynamique
  - BDD sparse et interprétable
- Archis et modèle pour la suite [R24/04]
  - E5 [Wang+24a], mE5 [Wang+24b]
  - RAG4HN [Tran+25]


### Trustworthy RAG [R9/02] 
- Définition et composantes de Trustworthy 
- 2 temps pour le RAG (Extraction et Génération)
- Métriques
- Interprétation et Explication
  - Paysage [Somvanshi+2026] + se situer
  - Activation Patching [Chen+24] [R30/03]
  - MechIR [Parry+25]
    - Perturbation
    - Interprétation des graphiques/ données


## Construction d'un dataset [R5/05, R20/05]
- Données dont on dispose
- Structure de données visée (motivations à cette structure : taille des documents/textes, format une question, 50% de +/-) [RAGRIGHTS-Specs]
- Outils d'extraction et mise en forme du texte (PyMuPDF4LLM, Langchain-text-splitter)

## Adaptation de RAG4HN [R20/05, Tran+25]
- Présentation de l'Archi (si pas déjà fait)
- Motivation des modifications (morceaux inutiles, format de données différent, reranking)

## Cartographie d'un modèle d'extraction d'information (nom à trouver)
### Méthodologie
- rappel de l'objectif
- Méthode perturbation [ragrights-protocole]
  - stats
  - langue de spécialité
  - niveaux de perturbation
  - type de perturbation
  - questionner les biais à la construction (dû à la compréhension humaine inconsciente)
- Méthode application de activation patching [ragrights-protocole]

### Résultats et analyse
- comportements observés & interprétation
- Préconisations d'usage
  - couverture de la perturbation
  - activation des dernières couches 
  - définition du critère de sensibilité
  - les moyens/ méthodes de visualisation des données
  - utiliser la question comme document pour avoir un témoin ???


## Perspectives
- Reprendre les expériences avec les préconisations
- Généraliser le protocole pour les dataset à plusieurs questions ??
- Élargir les préconisations et le protocole pour la langue de spécialité (pas juste le vocabulaire)
- Proposer un protocole d'évaluation de l'importance d'un noeud identifié
- Transformer ces résultats en explication 
  - formulation
  - exploitation lors de l'usage
- Intégration des explications dans l'architecture
  - mise en perspective des explications dans le modèle
  - explicabilité sur les autres composants du modèle
- Exploitation des explications pour l'affinement/ amélioration du modèle d'extraction




--------------------------------------------------------------------------------------

# Plan (gros grain)
Introduction
- Environnement du stage
- Outils utilisés
- **Difficultés techniques** (à placer autrement)
- Sujet du stage
État de l'art
- RAG & RALLM
- Le problème de la confiance pour les systèmes de RAG
Travaux réalisés
- Construction d'un dataset
- Adaptation du modèle RAG4HN
- Cartographie d'un modèle d'extraction d'information
  - Méthodologie
  - Résultats et Analyse
  - Perspectives ?
- Conclusion et Perspectives



# Détail des sous parties
## Environnement du stage
- Stage à lieu au LIFO, dans l'équipe CA, encadré par ...
- Stage de fin de master d'informatique Minerve GPEx
- Challenge@EvalLLM comme cas d'usage, participation envisagée mais timing pas OK
- différents événements et sorties organisées pendant le stage 
  - TransIA : Tours, Présentations pluridisciplinaires sur l'intégration de l'IA (sous toutes ses formes) dans la société
  - TAL-I : journée du GDR TaL-I à Paris (Jussieu) sur les travaux portant sur l'interprétabilité et l'explicabilité dans le contexte des tâches de traitement de la langue naturelle
  - 2nd Symposium on Mental Health and AI : deux jours de conférence (suivi en pointillé en distanciel) présentation des travaux à la croisée entre santé mentale et intelligence artificielle (impact, outils de détection, de prise en charge)
  - Place du Numérique : événement public de sensibilisation et de communication sur le Numérique organisé place du Martoi à Orléans (Des événements similaires organisés dans chaque département de la région CVL) J'ai participé à la tenue du stand de l'université, été ambassadrice de l'événement et ai joué le rôle d'un témoin dan sle tribunal des génération futures portant sur "L'IA nous contrôle-t-elle?
  - Présentation aux journées d'équipe CA

## Outils utilisés au cours du stage
- Développement de l'architecture et réalisation des expérimentations en python dans 3 formats (script, implémentation d'un CLI, notebook)
- Principales librairies python utilisées : PyTorch, TransformerLens, HuggingFace, PyMuPDF4LLM,...
- Utilisation de plusieurs git pour assurer le suivi des versions des outils développé lors du stage
- Pour l'execution de tâches demandantes en charge de calcul (Génération de la base de représentation des données, execution des différentes architectures explorées et/ou implémentées) : utilisation des grappes de calcul accessibles aux chercheurs du LIFO CaSciModOT et Mirev
- utilisation d'outils à base d'IA très modérée et pour les tâches de l'ordre de reformulation (ChatGPT), traduction (DeepL), exploration de la littérature (LitMaps, Perplexity), rédaction de petites fonctions et outils python (ChatGPT)

## Introduction du sujet du stage
TODO

## Générateurs et Modèles de Langue Augmentés par l'Extraction (RAG et RALLM)
- **Besoin et définition**
  - Les modèles profonds apprennent sur les données [ref à récupérer de Lewis+20]
  - Le problème des modèles génératifs : hallucination et connaissance bornée dans le temps [ref à récupérer de Lewis+20]
  - Il y a quelques années, on a cherché à associer un base de connaissances à ces modèles [Lewis+20] (= définition de RAG)
  - Parmis ces approches, on retrouve le cas des modèles de langue : RALLM
- **L'architecture RAG** Description de l'archi de façon plus avancée
  - Ces modèles peuvent être utilisés pour différents types de tâches (voir tableau csv sur RAGRights)
  - Avec le temps, l'idée de [Lewis+20] a été adaptée et augmentée de composants supplémentaires
  - [Fan+23] propose la structure générique ... (exploiter slides Séminaire CA)
- **RAG amélioré**??? Au delà de l'innovation de l'architecture, on retrouve des innovations sur plusieurs caratéristiques de ces modèles : [R24/04] [R16/02]
  - Multimodal [Liu+25]
  - Chain of Thought [Xu+24]
  - Gestion BDD dynamique [ref à trouver dans R24/05]
  - BDD sparse et interprétable [Prouteau]???
- **Modèle et Architecture utilisées durant le stage** Dans le cadre du stage, 
  - travailler sur une adaptation du modèle RAG4HN. [Tran+25] 
  - _description de l'architecture RAG4HN_ + parallèle avec l'architecture générique de [Fan+23]
  - L'extracteur de RAG4HN est mE5 [Wang+25b] (version multilingue de E5 [Whang+25a])

## Construire des systèmes RAG de confiance
- **Trustworthy AI** La définition d'IA de confiance (Trustworthy AI) tend à varier en fonction des situation et des utilisations de cette expression. Danss le contexte du Machine Learning, on désigne l'IA de confiance comme l'ensembles des systèmes d'IA dans lesquels il est légitime (dans le sens humainement entendable) d'avoir confiance. Le NIST (National Institute of Standards and Technology (US)) propose différents axes ou composantes de l'IA de confiance : ...
- **Explicabilité dans le contexte du RAG** Dans la suite, nous nous concentrons sur l'explicabilité dans le contexte du RAG. [Ni+25] distingue deux temps pour l'explicabilité : Extraction et génération ... (prévoir la question de l'association/intégration des deux)
  - Métrique ??
- **Interprétabilité Mécaniste** [Somvanshi+25]
  - Interprétabilité vs Explicabilité
  - Définition d'Interprétabilité Mécaniste et approches (Manual Circuit Tracing, *Intervention-based technique*, Representation analysis, Toy Model and synthetic tasks)
- **Activation patching**
  - Définition de activation patching [Chen+24] [R30/04] [Séminaire CA]
  - MechIR [Parry+25] 
    - Perturbation
    - Données produites, visualisation et interprétation des graphiques



---

# Reprise locale du plan
- Construction préalable des outils /!\ à reformuler
  - Construction d'un dataset
  - Architecture visée
  - Objectif de l'expérience
    - Localiser le vocabulaire/ la langue de spécialité dans le modèle
    - j
- Contribution méthodologique
  - Construction de perturbations

# Remarques et éléments à prendre en compte
## 2026-07-17
- Gestion de la traduction des concepts : ???
- et ce papier de l'autre jour, qu'en faire
- 


- Rester théorie et résultats
- Prévoir annexe pour les résultats 
- Prévoir annexe pour difficultés techniques (librairie, prise en main CaSciModOT)
- Placer "on ne dispose pas de données gold"
- Prouteau : dans Explicabilité RAG
- [x] 2.2 Système de RAG de confiance -> Interprétabilité pour les systèmes de RAG
- Développer le Challenge dans dataset :
  - Le challenge la tache
  - Les données fournies
  - ce qui nous manque
  - --
  - Le format de dataset visé
  - tous les dérouler V0, V1 et format V2 (à chaque fois: format, ce qui manque, les modifications proposées)
- [à rédiger] 1.3 la progression du stage en bref et le glissement du sujet
- 1.4 placer problématique résultats du cheminement
- garder l'évolution du sujet dans le bilan [personnel]  ou intro (pas dans le mémoire)
- 3, 4 et 5 => reformulation
  - 3 : prérequis à l'éxpé
    - datset
    - reprise d'un modèle 
  - 4 : ce qui était le 5.2 (Construction des pert, Estimation pertinence des pert, interprétation de activation Patching) _contribution méthodologique_
  - 5 : résultat expérimentaux (ancinement 5.3)
    - liste des perturbations choisies
- Ajouter touts les graphiques avec un texte succin => tri plus tart












---
# Typos à pister
- mécanistique -> mécaniste
- toin, iton,....
- pertuabtion



