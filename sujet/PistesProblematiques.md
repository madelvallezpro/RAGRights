# Pistes de problématiques scientifiques

## Base de données dynamique et apprentissage continu

**Contexte et problématique** : Lorsqu'on manipule des bases de données dynamique, on est confronté à la *suppression et l'ajout régulier d'éléments* dans cette base qui peut impacter significativement sa représentation <font color="red">**à justifier par citation**</font>. Un espace de représentation de telles bases de données calculé à l'aide des données contenue à un instant fixé T peut perdre en pertinence au fur à mesure des ajouts et suppressions dans la base de données. Pour que cet espace continue à capturer au mieux la base de documents, ce dernier doit *aussi s'adapter à ces changements*. Mettre en place une représentation compatible avec le *continual learning* permettrait de conserver une bonne capture de l'espace des documents disponibles.

**Bibliographie**:
- [[Gracianne 2023](https://theses.hal.science/tel-04633635v2)] Exploration de micro-posts d'actualité : représentation, structuration et description
- [[Zhu 2025](https://arxiv.org/abs/2508.05662)] From Static to Dynamic: A Streaming RAG Approach to Real-time Knowledge Base


## Interprétabilité

**Contexte et problématique** : Les récents outils d'extraction de connaissances actuels qui utilisent des *approches denses* sont souvent entraînés à l'aide de *méthodes opaques* <font color="red">citations</font>. Dans certaines situations, il est problématique d'exploiter une telle représentation car il y a un fort *besoin d'accessibilité des processus de décision* afin de légitimer ou modérer par l'humain les résultats obtenus. Les approches *interprétables* proposent des modèles dont le fonctionnement est humainement accessible ce qui permet de justifier le choix des données extraites ainsi que leur traitement et exploitation.

**Bibliographie** : 
- [[Prouteau et al. 2021](https://hal.science/hal-03197434v1)] SINr: Fast Computing of Sparse Interpretable Node Representations is not a Sin!
- [Guillot et al. 2023](https://hal.science/hal-04321407v1)  Sparser is better: one step closer to word embedding interpretability


## Frugalité

**Contexte et problématique** : Les architectures de RAG récentes exploitant des LLM se composent généralement de plusieurs LLMs. Ces modèles de grande taille sont assez demandant en calcul et donc en énergie lors de leur entraînement et de leur utilisation. Leur présence multiple dans une architecture pose des problème d'un point de vue matériel (besoin d'ordinateurs très puissant) et en terme de consommation. Mettre en commun les représentations des différents modèles présent dans un système RAG pourrait permette de réduire le coût d'entraînement et d'utilisation. 

**Bibliographie**: