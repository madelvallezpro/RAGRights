
# Replace, Append et Prepend sur un dataset défense à une question 

## Contexte
Semaine du 8 juin
mirev42
Effectué avec GenericAutomatedPertubation.py
interruption du K de la matrice de sensibilité des noeuds si présence d'un NaN


## Dataset défense fait main V2 

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


## Perturbations

Construction des perturbations:
- fréquence et TF-IDF des documents
- contenu de la question


```
matériel -> concret
matériel -> outil
+matériel
matériel+

système -> doctrine
système -> équation
système -> problème
système -> institution
système -> instance
+système
système+

drone+
+drone

défense -> lutte
défense -> protection
défense -> sport de combat
défense -> contre-attaque
défense -> interdiction
défense -> prohibition
défense -> corne
défense+
+défense

article -> publication
article -> journal
article -> produit
article -> revue
article -> achat
article -> sujet
article -> déterminant
article -> nom
+article
article+

technique -> difficile
technique -> fin
technique -> procédé
+technique 
technique+

aérien -> léger
aérien -> souple
+aérien
aérien+

limitation -> bornage
limitation -> démarcation
limitation -> restriction
limitation -> interdiction
+limitation
limitation+

```
## Résultats et analyse
### prepend `matériel` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_matériel+.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_matériel+.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_matériel+.png)

2e version du graphique

![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_matériel+V2.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_matériel+V2.png)


Graphiques
- concentre les extraits dans l'espace de représentation
- Quelques noeuds ressortent mais avec des variances assez élevés
- Des écarts-types globalement très élevés pour une bonne partie des noeuds


Vis-a-vis des données:
- _matériel_ est très présent dans les documents (6 extraits issu du chapitre MATERIEL du Code de la défense)
- _matériel_ n'est pas présent dans la question et n'est pas lié


### append `matériel` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_+matériel.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_+matériel.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_+matériel.png)


2e version du graphique

![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_+matérielV2.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_+matérielV2.png)

Graphiques
- Perturbation modérée d'après le graphique
- Réaction chaotique des noeuds  + grand écart-type

Vis-a-vis des données:
- _matériel_ est très présent dans les documents (6 extraits issu du chapitre MATERIEL du Code de la défense)
- _matériel_ n'est pas présent dans la question et n'est pas lié


### prepend `drone` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_drone+.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_drone+.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_drone+.png)

Vis-à-vis des données:
- Apparent dans la question
- Apparent dans 50% des extraits (100% extraits positifs)

Graphiques
- ajouter _drone_ regroupe tous les documents
- ajouter _drone_ éloigne les documents de la question
- On identifie un noeud plus sensible


### append `drone` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_+drone.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_+drone.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_+drone.png)

Vis-à-vis des données:
- Apparent dans la question
- Apparent dans 50% des extraits (extraits positifs)

Graphiques:
- distribution des distances similaires
- on retrouve le même noeud
- écart-type assez faible ~> résultats exploitables

### prepend `limitation` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_limitation+.png)

![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_limitation+.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_limitation+.png)

Vis-a-vis des données:
- Présent dans la question
- Présent dans les extraits (~50%)
- 2<sup>e</sup> plus grand TF-IDF sur les extraits

Graphique:
- 1 noeud intéressant à interpréter
- des écart-types parfois élevés 

### append `limitation` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_+limitation.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_+limitation.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_+limitation.png)

Vis-a-vis des données:
- Présent dans la question
- Présent dans les extraits (~50%)
- 2<sup>e</sup> plus grand TF-IDF sur les extraits

Graphique:
- plus de noeuds réactifs
- un noeud se dégage (même que pour prepend)
- MAIS des écarts-types plus importants !! ~> exploitable?

$\Rightarrow$ Même noeud que pour _drone_ (sont ts les deux dans la question... mais ce ne sont pas les seuls.)

### append `système` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_+système.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_+système.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_+système.png)

Vis-à-vis des données:
- Présent dans la question
- TF-IDF élevé

Graphique:
- perturbation qui concentre les extraits
- grand nombre de noeuds modérément sensibles
- mais grands écrats-types pour une majorité de noeuds (souvent plus grand que la moyenne) ~> Est-ce vraiment exploitable?


### prepend `technique` - Perturbation Score

![](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/PerturbationScore_technique+.png)


![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-mean_technique+.png) ![height:325px](../Travaux/stagexairag/challenge/rag4def_model/perturbation/res/mE5-MainV2/ComponentPatching-std_technique+.png)


- présent dans la question
- TF-IDF très faible (127<sup>e</sup>, 1 occ, TF-IDF = 0.0074)
- plusieurs noeuds modérément sensibles (concentrés en fin de modèle)
- MAIS écarts-types assez importants ~> peut-être pas exploitable

### Analyse générale
- Pas de perturbation `replace` suffisamment importante 
- Certaines perturbations semblent chaotiques
- Noeuds sensibles concentrés à une extrémité du modèle
- Cartographie des noeuds parfois similaire pour _append_ et _prepend_(cas avec écarts-types faibles)

$\Rightarrow$ Le choix du dataset doit-il est un levier pour la cartographie?
$\Rightarrow$ Les ordres de grandeur sont-ils importants pour l'interprétation?
$\Rightarrow$ Remplacer les NaN par des 0 ?

