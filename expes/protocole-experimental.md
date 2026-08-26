# Protocole Expérimental construit et appliqué lors du stage

## Introduction
- [Résultat préalable] L'activation patching construit une cartographie de LLM.
- [Cas d'usage] Localisation de la langue de spécialité

## Hypothèse à vérifier
- Cette cartographie est exploitable pour l'affinement de poids individuellement

## Objectif de l'expérimentation
Localiser la langue de spécialité dans le modèle de langue E5. Puis affiner le modèle poids par poids.

## Méthode
Soit un modèle de langue encodeur (ici E5) et un dataset 

### Localisation de la langue de spécialité du dataset dans E5
1. Identifier le lexique de spécialité $L_s$ du dataset
    a. Identifier les mots présents dans chaque texte
    b. Calculer la fréquence des mots
    c. Identifier le lexique de spécialité
2. Identifier les mots polysémiques (qui ont plusieurs sens) dans le lexique de spécialité $m \in L_s$ qui ont un sens différent dans le langage courant (grace à une ressource lexicale)
3. Identifier un synonyme pour le sens courant (Rq: On cherche un synonyme $s$ dont le sens est différent au sens du mot $m$.)
4. Construire les perturbations sous la forme `m -> s`
5. Sélectionner les perturbations auxquelles le modèle est sensible
    a. Avec les distances de représentation:
        - Comparer la répartition des distances (représentation de question, représentation de document) et (représentation de question, représentation de document perturbé)
        - Sélectionner les perturbations ayant des distributions différentes


### Affinement du modèle
3. Modifier les poids sensibles un à un 
4. Observer la variation de performance / Chercher à augmenter la performance

## Métriques
- Distance entre une paire (représentation de question, représentation de document)
- nDCG@k 


### Ouverture
Autres familles de perturbation:
- relations temporelles
- groupes de mots
- négation
- relations logiques
- suppression d'informations
- sous-groupes de langue de spécialité (cf ragright)

Autres exploitations de la cartographie:
- Entraînement approfondi d'un compétence linguistique
- Apprentissage par transfert (entraîner sur un autre dataset seulement pour la langue de spécialité)
- Prunning (en cas de spécialisation d'un modèle général)




