# Spécifications de description d'une liste de perturbations

## Perturbations

On distingue quatre types de perturbations:

- `replace` : remplace **un** mot par un autre (peut être utilisé pour supprimer un mot) dans un document
- `append`: ajoute un mot à la fin du document
- `prepend`: ajoute un mot au début du document
- `full_replace` : remplace une liste de mots par une autres (correspond au cumul de plusieurs perturbations de type `replace`)

## Au format texte

Trois types de perturbations peuvent être décrits au format texte :

- `replace` : représenté par `mot_remplacé -> mot replaçant`
- `prepend` : représenté par `mot_ajouté+`
- `append` : représenté par `+mot_ajouté`

Chaque perturbation de la liste est séparé par (au moins) un retour à la ligne. Les types de perturbations peuvent être mélangés.

## Au format json

Quatre types de perturbations peuvent être décrits au format json. Elles sont regroupés dans une liste où chaque perturbation est décrite comme suit.

Les perturbations de type `replace` sont représentés par des objets de la forme 

```{json}
{
    "type" : "replace",
    "from" : "mot_remplacé",
    "to" : "mot_remplaçant",
    "name" : "mot_remplacé -> mot remplaçant",
}
```

Les perturbations de type `append` sont représentés par des objets de la forme 

```{json}
{
    "type" : "append",
    "word" : "mot_ajouté",
    "name" : "+mot_ajouté",
}
```

Les perturbations de type `prepend` sont représentés par des objets de la forme 

```{json}
{
    "type" : "prepend",
    "word" : "mot_ajouté",
    "name" : "mot_ajouté+",
}
```

Les perturbations de type `full_replace` sont représentées par des objets de la forme

```{json}
{
    "type" : "full_replace",
    "name" : "<description succincte>",
    "compo": [
        {
            "type" : "replace",
            "from" : "mot_remplacé",
            "to" : "mot_remplaçant",
            "name" : "mot_remplacé -> mot_remplaçant",
        },
        {
            "type" : "replace",
            "from" : "mot_remplacé",
            "to" : "mot_remplaçant",
            "name" : "mot_remplacé -> mot_remplaçant",
        },
        ...
    ]
}
```

`compo` correspond à une liste de perturbations de type `replace`. Si un même mot est remplacé plusieurs fois ou qu'un mot remplaçant est lui même remplacé, le comportement n'est pas garanti.