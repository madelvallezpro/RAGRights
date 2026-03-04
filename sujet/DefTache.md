# Tâche de l'IA du projet du CRIJ
## Biblio - Tâches existantes
- Extraction de documents & synthèse 
    - Outils
        - [PaperQA2](https://github.com/Future-House/paper-qa) - [[Skarlinski et al., 2024](https://arxiv.org/abs/2409.13740)]
    - Bench
        - 
- Extraction de d'informations/ de passage 
- *Open Domain* Question Answer
- Entity linking

## Pistes des attendus
### Entrée
- documents hautement hétérogènes (JO, comm publique)


### Action - Attendu
- pas du reasoning -> laissé à l'humain
- extraction de document
- résumé de document (et du dispositifs décrit)

### Sortie
- bon retour de document (rappel > précision)
    - répond au problème
    - correspond au profil 
    - est une approx du profil (des paramètres possible à adapter différents [demandeur d'emploi, lieu de résidence,...])
- détection de contradiction/ complémentarité des dispositifs / incitation au changement de situation (être suffisamment flou / hors sujet pour inciter à proposition d'un changement de situation (demande d'emploi, déménagement, établissement d'inscription,...))

- cartographie des documents en sortie
    - situer les dispositifs les uns par rapports aux autres
    - situer le dispositifs dans l'ensemble des dispositifs (problématique traitées, problématiques connexes)

- résumé de dispositif

## Démarche de résolution
1. Selection de documents/dispositifs correspondant à la problématique [Doc Extraction]
    - Peut être traité via bonne représentation interprétable
2. Écartement des dispositifs dont le profil est non-éligible (sauf à un critère souple prêt)
    - besoin de trouver les infos dans le(s) descriptif(s) [Summary]
    - besoin de les comparer [Fact Checking??]
    - Récapitulatif des dispositifs trouvés