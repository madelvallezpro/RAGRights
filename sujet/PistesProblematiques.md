# Pistes de problématiques scientifiques

## Représentation des données
### Des données multimodales ?
**PB** : BDD avec texte (page web, description), infographie (image&texte), représentations logiques


**Biblio**:
- [Liu et al., 2025](https://dl.acm.org/doi/10.1145/3746027.3754761)  HM-RAG :Hierarchical Multi-Agent Multimodal Retrieval Augmented Generation


### Variabilité de la BDD - base de données dynamique
**PB** : 
- Des données nouvelles et nouvellement périmées régulièrement.
- Changement partiel du contenu de la BDD 
    - coût de calcul associé (si dense)
    - représentation plus ou moins adaptée pour les nouvelles données (si dense)

*Lorsque le contenu de la base de donnée est soumis à un changement régulier, l'espace de représentation adéquat peu aussi varier (notamment dans le cas du retrieval dense).*

**Biblio**:
- [[Prouteau et al. 2021](https://hal.science/hal-03197434v1)] SINr: Fast Computing of Sparse Interpretable Node Representations is not a Sin!
    - Séminaire 23/04/2025  - Nicolas Dugué
    - Comment l'ajout après construction de l'espace l'impacte-t-il?
- [[Zhu 2025](https://arxiv.org/abs/2508.05662)] From Static to Dynamic: A Streaming RAG Approach to Real-time Knowledge Base
    - traite l'entretien de BDD issu streams de données à fort débit (peu intéressant pour nous)
    - peu d'autres propositions


### Représentation permettant une bonne capture de la validité des données
**PB** : La pertinence des données dépends du contenu mais aussi du public visé. Comment capturer ces éléments rare dans la donnée mais important?

**Biblio**:
- [Prouteau et al. 2021](https://hal.science/hal-03197434v1) SINr: Fast Computing of Sparse Interpretable Node Representations is not a Sin!
- [Guillot et al. 2023](https://hal.science/hal-04321407v1)  Sparser is better: one step closer to word embedding interpretability
    - des axes pour le temps, l'espace, selon plusieurs niveau de granularité de l'espace (ville, département,...), les types de problématique,...


**Parallèle**:
- identification d'essai clinique pour un patient (Clinical-Trial dans BIRCO)
- article (défini par la pub) intéressant pour un profil client


### Frugalité

**PB**:
- exploitation de plusieurs LLM (extraction + génération) : est-il envisageable d'exploiter la représentation de l'extracteur pour la génération ?

**Biblio**



## Explicabilité pour les systèmes à base de RAG
**PB** : 
- besoin de récupérer les données qui ont servi à la production de la sortie
- besoin de justifier le résultat 
    - les données extraites
    - fiabilité de la generation
- faible présence de raisonnement dans l'outil -> comment exploiter les graphs dans ce contexte? 

**Biblio**:
- [[Prouteau et al. 2021](https://hal.science/hal-03197434v1)] SINr: Fast Computing of Sparse Interpretable Node Representations is not a Sin!
- [Guillot et al. 2023](https://hal.science/hal-04321407v1)  Sparser is better: one step closer to word embedding interpretability

