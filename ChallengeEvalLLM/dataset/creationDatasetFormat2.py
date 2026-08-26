#!/usr/bin/env python
# coding: utf-8

# # Construction à la main d'un petit dataset maitrisé issu de challenge

import pandas as pd

docsV2 = pd.read_csv("../docsV2.csv")

# ## Creation DB

db = pd.DataFrame(columns=["q_id", "question", "doc_id", "doc_name", "page_number", "chunk_id", "text", "pertinent"])

db = pd.concat([db,
           pd.DataFrame({
               "q_id" : [0],
               "question" : ["Quelles sont les trois catégories principales d’espaces couverts par la notion d'« installations militaires » selon le cadre juridique en vigueur?"],
               "doc_id" : [docsV2.iloc[49181].doc_id],
               "doc_name" : [docsV2.iloc[49181].doc_name],
               "page_number" :[docsV2.iloc[49181].page_number],
               "chunk_id" : [docsV2.iloc[49181].chunk_number],
               "text" : [docsV2.iloc[49181].text],
               "pertinent" : [True]
           })
           ], axis=0)



db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [0],
               "question" : ["Quelles sont les trois catégories principales d’espaces couverts par la notion d'« installations militaires » selon le cadre juridique en vigueur?"],
               "doc_id" : [docsV2.iloc[28106].doc_id],
               "doc_name" : [docsV2.iloc[28106].doc_name],
               "page_number" :[docsV2.iloc[28106].page_number],
               "chunk_id" : [docsV2.iloc[28106].chunk_number],
               "text" : [docsV2.iloc[28106].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [1],
               "question" : ["Qu'encourt une personne qui exporte des explosifs sans autorisation?"],
               "doc_id" : [docsV2.iloc[34421].doc_id],
               "doc_name" : [docsV2.iloc[34421].doc_name],
               "page_number" :[docsV2.iloc[34421].page_number],
               "chunk_id" : [docsV2.iloc[34421].chunk_number],
               "text" : [docsV2.iloc[34421].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [1],
               "question" : ["Qu'encourt une personne qui exporte des explosifs sans autorisation?"],
               "doc_id" : [docsV2.iloc[70843].doc_id],
               "doc_name" : [docsV2.iloc[70843].doc_name],
               "page_number" :[docsV2.iloc[70843].page_number],
               "chunk_id" : [docsV2.iloc[70843].chunk_number],
               "text" : [docsV2.iloc[70843].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [2],
               "question" : ["Quelles sont les caractéristiques de l'UAV SAENA?"],
               "doc_id" : [docsV2.iloc[76254].doc_id],
               "doc_name" : [docsV2.iloc[76254].doc_name],
               "page_number" :[docsV2.iloc[76254].page_number],
               "chunk_id" : [docsV2.iloc[76254].chunk_number],
               "text" : [docsV2.iloc[76254].text],
               "pertinent" : [True]
           })
                ], axis=0)

db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [2],
               "question" : ["Quelles sont les caractéristiques de l'UAV SAENA?"],
               "doc_id" : [docsV2.iloc[76549].doc_id],
               "doc_name" : [docsV2.iloc[76549].doc_name],
               "page_number" :[docsV2.iloc[76549].page_number],
               "chunk_id" : [docsV2.iloc[76549].chunk_number],
               "text" : [docsV2.iloc[76549].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [3],
               "question" : ["Quels publics est-il important de former à l'IA et pourquoi?"],
               "doc_id" : [docsV2.iloc[44635].doc_id],
               "doc_name" : [docsV2.iloc[44635].doc_name],
               "page_number" :[docsV2.iloc[44635].page_number],
               "chunk_id" : [docsV2.iloc[44635].chunk_number],
               "text" : [docsV2.iloc[44635].text],
               "pertinent" : [True]
           })
                ], axis=0)

db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [3],
               "question" : ["Quels publics est-il important de former à l'IA et pourquoi?"],
               "doc_id" : [docsV2.iloc[44649].doc_id],
               "doc_name" : [docsV2.iloc[44649].doc_name],
               "page_number" :[docsV2.iloc[44649].page_number],
               "chunk_id" : [docsV2.iloc[44649].chunk_number],
               "text" : [docsV2.iloc[44649].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [4],
               "question" : ["Quels sont les deux type de drones MALE et HALE actuellement exploité par l'USAF, et quelles différences majeures (envergure, masse, propulsion, durée de mission et armement) permettent de distinguer le MQ-9 Reaper du RQ-4 Global Hawk ?"],
               "doc_id" : [docsV2.iloc[45377].doc_id],
               "doc_name" : [docsV2.iloc[45377].doc_name],
               "page_number" :[docsV2.iloc[45377].page_number],
               "chunk_id" : [docsV2.iloc[45377].chunk_number],
               "text" : [docsV2.iloc[45377].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
            pd.DataFrame({
               "q_id" : [4],
               "question" : ["Quels sont les deux type de drones MALE et HALE actuellement exploité par l'USAF, et quelles différences majeures (envergure, masse, propulsion, durée de mission et armement) permettent de distinguer le MQ-9 Reaper du RQ-4 Global Hawk ?"],
               "doc_id" : [docsV2.iloc[20274].doc_id],
               "doc_name" : [docsV2.iloc[20274].doc_name],
               "page_number" :[docsV2.iloc[20274].page_number],
               "chunk_id" : [docsV2.iloc[20274].chunk_number],
               "text" : [docsV2.iloc[20274].text],
               "pertinent" : [False]
           })
], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [5],
               "question" : ["Quelles sont les deux prérogatives spécifiques que possède la Commission nationale consultative des droits de l'homme dans ses relations avec les organisations internationales, et en quoi ces prérogatives diffèrent-elles de celles des États ou des ONG ?"],
               "doc_id" : [docsV2.iloc[52757].doc_id],
               "doc_name" : [docsV2.iloc[52757].doc_name],
               "page_number" :[docsV2.iloc[52757].page_number],
               "chunk_id" : [docsV2.iloc[52757].chunk_number],
               "text" : [docsV2.iloc[52757].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [5],
               "question" : ["Quelles sont les deux prérogatives spécifiques que possède la Commission nationale consultative des droits de l'homme dans ses relations avec les organisations internationales, et en quoi ces prérogatives diffèrent-elles de celles des États ou des ONG ?"],
               "doc_id" : [docsV2.iloc[58398].doc_id],
               "doc_name" : [docsV2.iloc[58398].doc_name],
               "page_number" :[docsV2.iloc[58398].page_number],
               "chunk_id" : [docsV2.iloc[58398].chunk_number],
               "text" : [docsV2.iloc[58398].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [6],
               "question" : ["Quelles sont les deux conditions cumulatif qu’un ordre donné à un militaire français doit respecter pour être considéré comme légal selon le code de la défense, et quelles en sont les conséquences pour le subordonné et pour le supérior en cas de non-respect de ces conditions ?"],
               "doc_id" : [docsV2.iloc[39809].doc_id],
               "doc_name" : [docsV2.iloc[39809].doc_name],
               "page_number" :[docsV2.iloc[39809].page_number],
               "chunk_id" : [docsV2.iloc[39809].chunk_number],
               "text" : [docsV2.iloc[39809].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [6],
               "question" : ["Quelles sont les deux conditions cumulatif qu’un ordre donné à un militaire français doit respecter pour être considéré comme légal selon le code de la défense, et quelles en sont les conséquences pour le subordonné et pour le supérior en cas de non-respect de ces conditions ?"],
               "doc_id" : [docsV2.iloc[40252].doc_id],
               "doc_name" : [docsV2.iloc[40252].doc_name],
               "page_number" :[docsV2.iloc[40252].page_number],
               "chunk_id" : [docsV2.iloc[40252].chunk_number],
               "text" : [docsV2.iloc[40252].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [7],
               "question" : ["Quelles sont les deux missions principales du musée national de la Marine en lien avec ses collections, et quel type d’établissement public représente-t-il sur le plan juridique et administratif ?"],
               "doc_id" : [docsV2.iloc[39223].doc_id],
               "doc_name" : [docsV2.iloc[39223].doc_name],
               "page_number" :[docsV2.iloc[39223].page_number],
               "chunk_id" : [docsV2.iloc[39223].chunk_number],
               "text" : [docsV2.iloc[39223].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [7],
               "question" : ["Quelles sont les deux missions principales du musée national de la Marine en lien avec ses collections, et quel type d’établissement public représente-t-il sur le plan juridique et administratif ?"],
               "doc_id" : [docsV2.iloc[76691].doc_id],
               "doc_name" : [docsV2.iloc[76691].doc_name],
               "page_number" :[docsV2.iloc[76691].page_number],
               "chunk_id" : [docsV2.iloc[76691].chunk_number],
               "text" : [docsV2.iloc[76691].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [8],
               "question" : ["Quelles sont les deux fonctions principales remplies par les drones dans le domaine du *support au combat*?"],
               "doc_id" : [docsV2.iloc[45272].doc_id],
               "doc_name" : [docsV2.iloc[45272].doc_name],
               "page_number" :[docsV2.iloc[45272].page_number],
               "chunk_id" : [docsV2.iloc[45272].chunk_number],
               "text" : [docsV2.iloc[45272].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [8],
               "question" : ["Quelles sont les deux fonctions principales remplies par les drones dans le domaine du *support au combat*?"],
               "doc_id" : [docsV2.iloc[45548].doc_id],
               "doc_name" : [docsV2.iloc[45548].doc_name],
               "page_number" :[docsV2.iloc[45548].page_number],
               "chunk_id" : [docsV2.iloc[45548].chunk_number],
               "text" : [docsV2.iloc[45548].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [9],
               "question" : ["Quelles sont les deux conditions précises qui permettent à un militaire de bénéficier *de droit* d’une prorogation de son congé pour création ou reprise d’entreprise, sans que l’avis de la commission compétente ne soit requis ?"],
               "doc_id" : [docsV2.iloc[40854].doc_id],
               "doc_name" : [docsV2.iloc[40854].doc_name],
               "page_number" :[docsV2.iloc[40854].page_number],
               "chunk_id" : [docsV2.iloc[40854].chunk_number],
               "text" : [docsV2.iloc[40854].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [9],
               "question" : ["Quelles sont les deux conditions précises qui permettent à un militaire de bénéficier *de droit* d’une prorogation de son congé pour création ou reprise d’entreprise, sans que l’avis de la commission compétente ne soit requis ?"],
               "doc_id" : [docsV2.iloc[1183].doc_id],
               "doc_name" : [docsV2.iloc[1183].doc_name],
               "page_number" :[docsV2.iloc[1183].page_number],
               "chunk_id" : [docsV2.iloc[1183].chunk_number],
               "text" : [docsV2.iloc[1183].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [10],
               "question" : ["Quelles sont les conditions pour obtenir un congé pour convenances personelles en tant que militaire?"],
               "doc_id" : [docsV2.iloc[40993].doc_id],
               "doc_name" : [docsV2.iloc[40993].doc_name],
               "page_number" :[docsV2.iloc[40993].page_number],
               "chunk_id" : [docsV2.iloc[40993].chunk_number],
               "text" : [docsV2.iloc[40993].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [10],
               "question" : ["Quelles sont les conditions pour obtenir un congé pour convenances personelles en tant que militaire?"],
               "doc_id" : [docsV2.iloc[34792].doc_id],
               "doc_name" : [docsV2.iloc[34792].doc_name],
               "page_number" :[docsV2.iloc[34792].page_number],
               "chunk_id" : [docsV2.iloc[34792].chunk_number],
               "text" : [docsV2.iloc[34792].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [11],
               "question" : ["Quelles sont les trois types de charges utiles que peuvent employer les essaims de vecteurs compacts pour neutraliser des cibles navales ou aéronavales, et en quoi l’une d’entre elles présente-t-elle un risque particulier dans un contexte portuaire ou de base militaire ?"],
               "doc_id" : [docsV2.iloc[55603].doc_id],
               "doc_name" : [docsV2.iloc[55603].doc_name],
               "page_number" :[docsV2.iloc[55603].page_number],
               "chunk_id" : [docsV2.iloc[55603].chunk_number],
               "text" : [docsV2.iloc[55603].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [11],
               "question" : ["Quelles sont les trois types de charges utiles que peuvent employer les essaims de vecteurs compacts pour neutraliser des cibles navales ou aéronavales, et en quoi l’une d’entre elles présente-t-elle un risque particulier dans un contexte portuaire ou de base militaire ?"],
               "doc_id" : [docsV2.iloc[43524].doc_id],
               "doc_name" : [docsV2.iloc[43524].doc_name],
               "page_number" :[docsV2.iloc[43524].page_number],
               "chunk_id" : [docsV2.iloc[43524].chunk_number],
               "text" : [docsV2.iloc[43524].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [12],
               "question" : ["Comment le drone tactique SDTI, conçu pour les opérations militaires conventionnelles (type Afghanistan), se compare-t-il aux mini-drones utilisés dans les guerres asymétriques (type Mossoul) en termes de contraintes logistiques et de souplesse d'emploi ?"],
               "doc_id" : [docsV2.iloc[45297].doc_id],
               "doc_name" : [docsV2.iloc[45297].doc_name],
               "page_number" :[docsV2.iloc[45297].page_number],
               "chunk_id" : [docsV2.iloc[45297].chunk_number],
               "text" : [docsV2.iloc[45297].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [12],
               "question" : ["Comment le drone tactique SDTI, conçu pour les opérations militaires conventionnelles (type Afghanistan), se compare-t-il aux mini-drones utilisés dans les guerres asymétriques (type Mossoul) en termes de contraintes logistiques et de souplesse d'emploi ?"],
               "doc_id" : [docsV2.iloc[70689].doc_id],
               "doc_name" : [docsV2.iloc[70689].doc_name],
               "page_number" :[docsV2.iloc[70689].page_number],
               "chunk_id" : [docsV2.iloc[70689].chunk_number],
               "text" : [docsV2.iloc[70689].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [13],
               "question" : ["Quels sont les deux objectifs principaux de l’exercice REPMUS 2024 au Portugal, et en quoi cet événement représente-t-il également une opportunité stratégique pour les industriels participants ?"],
               "doc_id" : [docsV2.iloc[71317].doc_id],
               "doc_name" : [docsV2.iloc[71317].doc_name],
               "page_number" :[docsV2.iloc[71317].page_number],
               "chunk_id" : [docsV2.iloc[71317].chunk_number],
               "text" : [docsV2.iloc[71317].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [13],
               "question" : ["Quels sont les deux objectifs principaux de l’exercice REPMUS 2024 au Portugal, et en quoi cet événement représente-t-il également une opportunité stratégique pour les industriels participants ?"],
               "doc_id" : [docsV2.iloc[64891].doc_id],
               "doc_name" : [docsV2.iloc[64891].doc_name],
               "page_number" :[docsV2.iloc[64891].page_number],
               "chunk_id" : [docsV2.iloc[64891].chunk_number],
               "text" : [docsV2.iloc[64891].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [14],
               "question" : ["Quelles sont les deux couleurs utilisées dans le tableau des amendements pour distinguer respectivement ceux qui ont été validés par le CICDE et ceux qui ont été intégrés dans la nouvelle version du document, et que symbolisent chacune de ces couleurs ?"],
               "doc_id" : [docsV2.iloc[1642].doc_id],
               "doc_name" : [docsV2.iloc[1642].doc_name],
               "page_number" :[docsV2.iloc[1642].page_number],
               "chunk_id" : [docsV2.iloc[1642].chunk_number],
               "text" : [docsV2.iloc[1642].text],
               "pertinent" : [True]
           })
                ], axis=0)

db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [14],
               "question" : ["Quelles sont les deux couleurs utilisées dans le tableau des amendements pour distinguer respectivement ceux qui ont été validés par le CICDE et ceux qui ont été intégrés dans la nouvelle version du document, et que symbolisent chacune de ces couleurs ?"],
               "doc_id" : [docsV2.iloc[1645].doc_id],
               "doc_name" : [docsV2.iloc[1645].doc_name],
               "page_number" :[docsV2.iloc[1645].page_number],
               "chunk_id" : [docsV2.iloc[1645].chunk_number],
               "text" : [docsV2.iloc[1645].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [15],
               "question" : ["Quelles sont les deux obligations financières distinctes qu’un assujetti doit remplir s’il ne restitue pas suffisamment de quotas d’émission pour couvrir ses émissions annuelles de CO₂, et en quoi ces obligations diffèrent-elles en termes de finalité et de persistance ?"],
               "doc_id" : [docsV2.iloc[70527].doc_id],
               "doc_name" : [docsV2.iloc[70527].doc_name],
               "page_number" :[docsV2.iloc[70527].page_number],
               "chunk_id" : [docsV2.iloc[70527].chunk_number],
               "text" : [docsV2.iloc[70527].text],
               "pertinent" : [True]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [15],
               "question" : ["Quelles sont les deux obligations financières distinctes qu’un assujetti doit remplir s’il ne restitue pas suffisamment de quotas d’émission pour couvrir ses émissions annuelles de CO₂, et en quoi ces obligations diffèrent-elles en termes de finalité et de persistance ?"],
               "doc_id" : [docsV2.iloc[68751].doc_id],
               "doc_name" : [docsV2.iloc[68751].doc_name],
               "page_number" :[docsV2.iloc[68751].page_number],
               "chunk_id" : [docsV2.iloc[68751].chunk_number],
               "text" : [docsV2.iloc[68751].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [16],
               "question" : ["cyberattaque agression armée droit international critères seuil gravité attribution effets comparables attaque conventionnelle coordination opérations physiques accumulation effets article 2(4) Charte ONU doctrine Tallin"],
               "doc_id" : [docsV2.iloc[52517].doc_id],
               "doc_name" : [docsV2.iloc[52517].doc_name],
               "page_number" :[docsV2.iloc[52517].page_number],
               "chunk_id" : [docsV2.iloc[52517].chunk_number],
               "text" : [docsV2.iloc[52517].text],
               "pertinent" : [True]
           })
                ], axis=0)



db = pd.concat([db,
                pd.DataFrame({
               "q_id" : [16],
               "question" : ["cyberattaque agression armée droit international critères seuil gravité attribution effets comparables attaque conventionnelle coordination opérations physiques accumulation effets article 2(4) Charte ONU doctrine Tallin"],
               "doc_id" : [docsV2.iloc[10274].doc_id],
               "doc_name" : [docsV2.iloc[10274].doc_name],
               "page_number" :[docsV2.iloc[10274].page_number],
               "chunk_id" : [docsV2.iloc[10274].chunk_number],
               "text" : [docsV2.iloc[10274].text],
               "pertinent" : [False]
           })
                ], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [17],
               "question" : ["Quels sont les deux moteurs d’avions de combat pour lesquels Safran, MTU Aero Engines et Rolls-Royce collaborent ensemble, et quel programme européen futur est associé à ces mêmes partenaires ?"],
               "doc_id" : [docsV2.iloc[72375].doc_id],
               "doc_name" : [docsV2.iloc[72375].doc_name],
               "page_number" :[docsV2.iloc[72375].page_number],
               "chunk_id" : [docsV2.iloc[72375].chunk_number],
               "text" : [docsV2.iloc[72375].text],
               "pertinent" : [True]
           })], axis=0)

db = pd.concat([db,pd.DataFrame({
               "q_id" : [17],
               "question" : ["Quels sont les deux moteurs d’avions de combat pour lesquels Safran, MTU Aero Engines et Rolls-Royce collaborent ensemble, et quel programme européen futur est associé à ces mêmes partenaires ?"],
               "doc_id" : [docsV2.iloc[44459].doc_id],
               "doc_name" : [docsV2.iloc[44459].doc_name],
               "page_number" :[docsV2.iloc[44459].page_number],
               "chunk_id" : [docsV2.iloc[44459].chunk_number],
               "text" : [docsV2.iloc[44459].text],
               "pertinent" : [False]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [18],
               "question" : ["Quels sont les deux défis contradictoires auxquels les États-Unis sont confrontés dans la mise en œuvre de leur architecture C4ISR face à la stratégie anti-A2/AD de l’Armée de libération populaire chinoise, et en quoi ces défis remettent-ils en cause les principes mêmes de l’intégration multidomaine (JADC2) ?"],
               "doc_id" : [docsV2.iloc[30048].doc_id],
               "doc_name" : [docsV2.iloc[30048].doc_name],
               "page_number" :[docsV2.iloc[30048].page_number],
               "chunk_id" : [docsV2.iloc[30048].chunk_number],
               "text" : [docsV2.iloc[30048].text],
               "pertinent" : [True]
           })], axis=0)

db = pd.concat([db,pd.DataFrame({
               "q_id" : [18],
               "question" : ["Quels sont les deux défis contradictoires auxquels les États-Unis sont confrontés dans la mise en œuvre de leur architecture C4ISR face à la stratégie anti-A2/AD de l’Armée de libération populaire chinoise, et en quoi ces défis remettent-ils en cause les principes mêmes de l’intégration multidomaine (JADC2) ?"],
               "doc_id" : [docsV2.iloc[71580].doc_id],
               "doc_name" : [docsV2.iloc[71580].doc_name],
               "page_number" :[docsV2.iloc[71580].page_number],
               "chunk_id" : [docsV2.iloc[71580].chunk_number],
               "text" : [docsV2.iloc[71580].text],
               "pertinent" : [False]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [19],
               "question" : ["Quels sont les deux effets concrets de l’article D4154-1 du code du travail sur la production industrielle des drones, en particulier dans le domaine de la soudure, et comment ces effets menacent-ils la stabilité des PME du secteur ?"],
               "doc_id" : [docsV2.iloc[20494].doc_id],
               "doc_name" : [docsV2.iloc[20494].doc_name],
               "page_number" :[docsV2.iloc[20494].page_number],
               "chunk_id" : [docsV2.iloc[20494].chunk_number],
               "text" : [docsV2.iloc[20494].text],
               "pertinent" : [True]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [19],
               "question" : ["Quels sont les deux effets concrets de l’article D4154-1 du code du travail sur la production industrielle des drones, en particulier dans le domaine de la soudure, et comment ces effets menacent-ils la stabilité des PME du secteur ?"],
               "doc_id" : [docsV2.iloc[17469].doc_id],
               "doc_name" : [docsV2.iloc[17469].doc_name],
               "page_number" :[docsV2.iloc[17469].page_number],
               "chunk_id" : [docsV2.iloc[17469].chunk_number],
               "text" : [docsV2.iloc[17469].text],
               "pertinent" : [False]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [20],
               "question" : ["Quelles sont les deux conditions précises dans lesquelles un militaire peut engager une médiation, malgré l’existence d’un recours administratif préalable déjà formé devant la commission des recours des militaires ?"],
               "doc_id" : [docsV2.iloc[40258].doc_id],
               "doc_name" : [docsV2.iloc[40258].doc_name],
               "page_number" :[docsV2.iloc[40258].page_number],
               "chunk_id" : [docsV2.iloc[40258].chunk_number],
               "text" : [docsV2.iloc[40258].text],
               "pertinent" : [True]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [20],
               "question" : ["Quelles sont les deux conditions précises dans lesquelles un militaire peut engager une médiation, malgré l’existence d’un recours administratif préalable déjà formé devant la commission des recours des militaires ?"],
               "doc_id" : [docsV2.iloc[75135].doc_id],
               "doc_name" : [docsV2.iloc[75135].doc_name],
               "page_number" :[docsV2.iloc[75135].page_number],
               "chunk_id" : [docsV2.iloc[75135].chunk_number],
               "text" : [docsV2.iloc[75135].text],
               "pertinent" : [False]
           })], axis=0)



db = pd.concat([db,pd.DataFrame({
               "q_id" : [21],
               "question" : ["Quels étaient les quatre rôles concrets remplis par le ballon captif déployé lors de l'opération Barkhane à Kidal en 2018, et comment son efficacité se manifestait-elle aussi bien de jour que de nuit ?"],
               "doc_id" : [docsV2.iloc[1668].doc_id],
               "doc_name" : [docsV2.iloc[1668].doc_name],
               "page_number" :[docsV2.iloc[1668].page_number],
               "chunk_id" : [docsV2.iloc[1668].chunk_number],
               "text" : [docsV2.iloc[1668].text],
               "pertinent" : [True]
           })], axis=0)


db = pd.concat([db, pd.DataFrame({
               "q_id" : [21],
               "question" : ["Quels étaient les quatre rôles concrets remplis par le ballon captif déployé lors de l'opération Barkhane à Kidal en 2018, et comment son efficacité se manifestait-elle aussi bien de jour que de nuit ?"],
               "doc_id" : [docsV2.iloc[2].doc_id],
               "doc_name" : [docsV2.iloc[2].doc_name],
               "page_number" :[docsV2.iloc[2].page_number],
               "chunk_id" : [docsV2.iloc[2].chunk_number],
               "text" : [docsV2.iloc[2].text],
               "pertinent" : [False]
           })], axis=0)

db = pd.concat([db,pd.DataFrame({
               "q_id" : [22],
               "question" : ["What are the two concrete types of ties linking the BIG to the Azerbaijani state, and how does each manifest verifiably in administrative practices or public statements?"],
               "doc_id" : [docsV2.iloc[63552].doc_id],
               "doc_name" : [docsV2.iloc[63552].doc_name],
               "page_number" :[docsV2.iloc[63552].page_number],
               "chunk_id" : [docsV2.iloc[63552].chunk_number],
               "text" : [docsV2.iloc[63552].text],
               "pertinent" : [True]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [22],
               "question" : ["What are the two concrete types of ties linking the BIG to the Azerbaijani state, and how does each manifest verifiably in administrative practices or public statements?"],
               "doc_id" : [docsV2.iloc[59584].doc_id],
               "doc_name" : [docsV2.iloc[59584].doc_name],
               "page_number" :[docsV2.iloc[59584].page_number],
               "chunk_id" : [docsV2.iloc[59584].chunk_number],
               "text" : [docsV2.iloc[59584].text],
               "pertinent" : [False]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [23],
               "question" : ["Quelles sont les trois principales catégories de limitations techniques affectant les systèmes de drones, et comment chacune influence-t-elle l'efficacité opérationnelle de ces vecteurs ?"],
               "doc_id" : [docsV2.iloc[27666].doc_id],
               "doc_name" : [docsV2.iloc[27666].doc_name],
               "page_number" :[docsV2.iloc[27666].page_number],
               "chunk_id" : [docsV2.iloc[27666].chunk_number],
               "text" : [docsV2.iloc[27666].text],
               "pertinent" : [True]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [23],
               "question" : ["Quelles sont les trois principales catégories de limitations techniques affectant les systèmes de drones, et comment chacune influence-t-elle l'efficacité opérationnelle de ces vecteurs ?"],
               "doc_id" : [docsV2.iloc[43549].doc_id],
               "doc_name" : [docsV2.iloc[43549].doc_name],
               "page_number" :[docsV2.iloc[43549].page_number],
               "chunk_id" : [docsV2.iloc[43549].chunk_number],
               "text" : [docsV2.iloc[43549].text],
               "pertinent" : [False]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [24],
               "question" : ["Quelles sont les deux méthodes alternatives utilisées pour évaluer les actifs de l'État dont le coût historique est indéterminable, et dans quel cas chacune d’elles est-elle appliquée ?"],
               "doc_id" : [docsV2.iloc[69420].doc_id],
               "doc_name" : [docsV2.iloc[69420].doc_name],
               "page_number" :[docsV2.iloc[69420].page_number],
               "chunk_id" : [docsV2.iloc[69420].chunk_number],
               "text" : [docsV2.iloc[69420].text],
               "pertinent" : [True]
           })], axis=0)



db = pd.concat([db,pd.DataFrame({
               "q_id" : [24],
               "question" : ["Quelles sont les deux méthodes alternatives utilisées pour évaluer les actifs de l'État dont le coût historique est indéterminable, et dans quel cas chacune d’elles est-elle appliquée ?"],
               "doc_id" : [docsV2.iloc[9200].doc_id],
               "doc_name" : [docsV2.iloc[9200].doc_name],
               "page_number" :[docsV2.iloc[9200].page_number],
               "chunk_id" : [docsV2.iloc[9200].chunk_number],
               "text" : [docsV2.iloc[9200].text],
               "pertinent" : [False]
           })], axis=0)


db = pd.concat([db,pd.DataFrame({
               "q_id" : [25],
               "question" : ["Quelles sont les trois règles fondamentales qu’un drone ou un agent au sein d’un essaim autonome doit appliquer pour reproduire un comportement collectif coordonné, et en quoi chacune de ces règles contribue-t-elle à la fluidité et à la résilience du déplacement du groupe ?"],
               "doc_id" : [docsV2.iloc[55999].doc_id],
               "doc_name" : [docsV2.iloc[55999].doc_name],
               "page_number" :[docsV2.iloc[55999].page_number],
               "chunk_id" : [docsV2.iloc[55999].chunk_number],
               "text" : [docsV2.iloc[55999].text],
               "pertinent" : [True]
           })], axis=0)

db = pd.concat([db,pd.DataFrame({
               "q_id" : [25],
               "question" : ["Quelles sont les trois règles fondamentales qu’un drone ou un agent au sein d’un essaim autonome doit appliquer pour reproduire un comportement collectif coordonné, et en quoi chacune de ces règles contribue-t-elle à la fluidité et à la résilience du déplacement du groupe ?"],
               "doc_id" : [docsV2.iloc[14321].doc_id],
               "doc_name" : [docsV2.iloc[14321].doc_name],
               "page_number" :[docsV2.iloc[14321].page_number],
               "chunk_id" : [docsV2.iloc[14321].chunk_number],
               "text" : [docsV2.iloc[14321].text],
               "pertinent" : [False]
           })], axis=0)

db.reset_index(drop=True, inplace=True)


db.to_csv("paires_mainV1.csv", index=True)


docs = db[["doc_id", "doc_name", "page_number", "chunk_id", "text"]]
docs.to_csv("docs_mainV1.csv", index=True)

queries = db[["q_id", "question"]]
queries.drop_duplicates(inplace=True, ignore_index=True)
queries.to_csv("queries_mainV1.csv", index=False)