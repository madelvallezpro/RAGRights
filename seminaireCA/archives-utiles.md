---
marp: true
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
  .small {
    font-size: 20px
  }
  .midsize{
    font-size: 25px
  }
math: mathjax
paginate: true
---

# Séminaires CA - Explicabilité mécanistique pour l'amélioration des modèles profonds de RAG

---
# RAG
---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Extraction - Types
- **Types d'Extracteur**
    - **Sparse retrieval** : au niveau des mots (TF-IDF, BM25)
        - pas entraîné
        - grosse dépendance à la qualité de la BDD et requête
    - **Dense retrieval** : plonger dans un espace 
        - 1ere couche de générateur pour projeter
        - encodeur spécifique ([Contriever](https://github.com/facebookresearch/contriever) - [[Izacard et al. 2022]](https://arxiv.org/pdf/2112.09118) )
        - bi-encodeur (Dense Passage Retrieval - [[Karpukhin et al. 2020]](https://aclanthology.org/2020.emnlp-main.550/))

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Extraction - Granularité
- **Granularité de d'Extraction** : taille de découpe des extraits
  - **chunk retieval** - le plus répandu
  - **token retrieval** - plus fin mais plus lourd en calcul
  - **entity retrieval** - perspective du langage (Entities as Experts - [[Févry et al. 2020]](https://aclanthology.org/2020.emnlp-main.400/))

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Extraction - Amélioration pré-retrieval
- **Pre-Retrieval Enhancement** : réduire la charge du retriever en *complétant la requête*
  - **query expansion** - générer des docs fictifs, compléter la query avec les infos pertinentes ~> désambiguïser (Query2Doc - [[Wang et al. 2023]](https://aclanthology.org/2023.emnlp-main.585/))
  - **query rewrite** - reformuler l'entrée à l'aide données supplémentaires (Rewrite-Retrieve-Read - [[Ma et al. 2023]](https://arxiv.org/abs/2305.14283))
  - **query augmentation** - compléter l'entrée avec une réponse sans données extraites (ReFeed - [[Yu et al. 2023]](https://arxiv.org/pdf/2305.14002))

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Extraction - Amélioration post-retrieval
- **Post-Retrieval Enhancement** : réduire la charge sur l'extracteur en *affinant les informations extraites*
  - **ajustement du classement** des extraits (PRCA - [[Yang et al. 2023]](https://aclanthology.org/2023.emnlp-main.326/))
  - **réduction du bruit** dans les extraits
  - assembler **plusieurs extracteurs** (R<sup>2</sup>G : Retrieve  Rerank Generate - [[Glass et al., 2022]](https://aclanthology.org/2022.naacl-main.194/))
  - **ajouter la query** aux données
  - utiliser des **reasoning paths** ([Search-in-the-Chain](https://github.com/xsc1234/Search-in-the-Chain) - [[Xu et al. 2024]](https://arxiv.org/abs/2304.14732))
  - **compression/synthèse** des (gros) extraits 

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Extraction - Base de données
Nature et source des données différentes
- **closed source** - locale
- **domain specific**
- **open-source** - utilisation de moteurs de recherche public

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Générateurs - Familles
Différents modèles de langues ~> Dépends de la tâche tierce

- **Parameter accessible** - peut être affiné
- **Parameter inaccessible** - via API sans accès aux paramètres 

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Intégration - Stratégies
- **Input Layer Integration** - Combiner Requête et Extraits en entrée du Générateur
  - tous les documents **en même temps** ([In-Context RALM](https://github.com/AI21Labs/in-context-ralm/tree/main) - [[Ram et al., 2023]](https://aclanthology.org/2023.tacl-1.75.pdf))
  - un document **à la fois** ([ATLAS](https://github.com/facebookresearch/atlas) - [[Izacard et al. 2023]](https://dl.acm.org/doi/epdf/10.5555/3648699.3648950), REPLUG [reproduction](https://github.com/SashaBoguraev/REPLUG) - [[Shi et al., 2024]](https://aclanthology.org/2024.naacl-long.463/))
- **Output Layer Integration** - Fournir les données et le texte généré séparément (ou petit traitement pour unir) (ReFeed - [[Yu et al. 2023]](https://arxiv.org/pdf/2305.14002))
- **Intermediate Layer Integration** - intégrer les documents extraits au milieu de la génération (du modèle)

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Intégration - Fréquence et Nécessité
Extraction non pertinente $\implies$ hallucination / bruit
=> Définir des critères de recours ou non au Retrieval

<div class="columns"><div>

- **Coté RA-LLM**
  - token spécifique
  - prompt itéré
  - modèles annexes entraînés pour déclencher
  - définition de logit déclencheurs

</div><div>

- **Coté RAG "traditionnels"** : fréquence fixée
  - one-time
  - every-n-token
  - every-token

</div></div>

---
<div class="small"> 

*Survey on RAG Meeting LLM: Towards Retrieval-Augmented Large Language Models [Fan et al., 2023]*

</div>

## Entraînement - Stratégies
Affiner les composants sur la tâche tierce
- **Training free** 
  - **prompt engineering based method** : injection des données dans le prompt
  - **retrieval guided token generation method** : calibrer la génération à l'aide des données
- **Independent Training** : hors pipeline
- **Sequential Training** : le 2<sup>nd</sup> au sein du pipeline (2 ordres possibles)
- **Join Training** : les deux en même temps dans le pipeline

---

# XAI

---
## Modèle boite noire

**Modèles pour lesquels les processus de décision ne sont pas transparents pour l’humain**

Problème : Perte de confiance pour certains usages

---
## Définitions centrales de l'XAI

- **Explicabilité de l’IA** : Rendre humainement compréhensible les raisons pour lesquelles un
modèle effectue une certaine prédiction. [Garouani et al., 2024, Bell et al., 2022]
- **Comprendre** : Être capable d’anticiper et/ou justifier le comportement du modèle. [Bell et al., 2022]
- **Explication** : Tout support rendant le processus de décision d’un modèle humainement intelligible.

---
## Formes d'explication
- attribution
- saliency map (image ou texte)
- règles

---
## Temps de l'explicabilité

![](../images/VieModele-TempsXAI.drawio.pdf)

<div class="columns"><div>

Interprétabilité  
_Comment ?_

</div><div>

Explicabilité  
_Pourquoi ?_

</div></div>

---

# MechIR

---
## [[Parry et al., 2025](https://arxiv.org/abs/2501.10165)] MechIR: A Mechanistic Interpretability Framework for Information Retrieval
**Activation Patching** : Observer la réaction d'un composant à une caractéristique d'une entrée
- Relevé des valeurs intermédiaires du modèle sur l'entrée $i$ 
- Relevé des valeurs intermédiaires du modèle sur l'entrée perturbée $i'$ 
- Fixer les valeurs du/des noeuds observés avec celles observées (meilleure perf)
- Observer les output sur l'entrée fournie (moins bonne perf)

---
## [[Parry et al., 2025](https://arxiv.org/abs/2501.10165)] MechIR: A Mechanistic Interpretability Framework for Information Retrieval
<div class="columns"><div>

MechIR : Propose une implem pour les modèles encoder-based 


Difficultés : 
- Lourd en calcul
- Problèmes d'installation

</div><div>

![exemple de heatmap obtenue](../images/ActivationPatchingAllHeadExempleMechIR.png)

</div></div>

---
---
## [[Chen et al., 2024](https://dl.acm.org/doi/10.1145/3626772.3657841)] Axiomatic Causal Interventions for Reverse Engineering Relevance Computation in Neural Retrieval Models
Étends la méthode proposée par [[Geiger et al., 2021](https://dl.acm.org/doi/10.5555/3540261.3540994)]  
Méthode implémentée par MechIR [[Parry et al., 2025](https://arxiv.org/abs/2501.10165)]

*Pourquoi prendre comme référence les données avec meilleur pref et pas données baseline? (Contrairement à la méthode originale)*  
> "This modification accounts for axiomatic perturbations that may either add or remove crucial relevance concepts from a document"

*Quelle métrique utilisée?* 
> "To assess the patch’s effect on model performance, we evaluate using the normalized difference in ranking scores"

---
## [[Chen et al., 2024](https://dl.acm.org/doi/10.1145/3626772.3657841)] Axiomatic Causal Interventions for Reverse Engineering Relevance Computation in Neural Retrieval Models

![](../images/Ill-activationPatching_Chen-et-al2024.png)

---