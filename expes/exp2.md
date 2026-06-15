
# Elephant sur un dataset défense à une question 

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

Construction des perturbations

Choix des mots à remplacer:
- fréquence et TF-IDF des documents
- contenu de la question

Choix des mots éléphants utilisés:
- aléas de nos pensées avec jugement qualitatif de la proximité entre le mot et le contexte du dataset
- utilisation de mot improbable dans ce contexte, de même classe grammaticale
/!\ pas de groupe de mot improbable dans la langue en général

Perturbations replace:
``` 
article -> table
aérien -> épicurien
drone -> gazon
défense -> fromage
limitation -> animation
matériel -> post-it
système -> panneau
technique -> magique
```

Perturbations append et prépend
```
+post-it
post-it+
+panneau
panneau+
+animation
animation+
+gazon
gazon+
+fromage
fromage+
+table
table+
+magique
magique+
+épicurien
épicurien+
```
## Résultats et analyse
### replace
Pas de matrice calculée : présence de NaN
Des scores de perturbations peut intéressants (sauf drone -> gazon même si pas de matrice)