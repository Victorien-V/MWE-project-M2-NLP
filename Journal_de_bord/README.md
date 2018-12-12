# Consignes

Les consignes pour le projet sont disponibles [ici](https://loicgrobol.github.io/python-im/m2-2018/projets.html).

# Sujet du projet : gestion de MWEs dans un fichier conllu

Pour ce projet, notre objectif est de pouvoir gérer les Multi-Word Expressions (MWE) présentes dans un fichier `.conllu`.

Dans l'idéal, nous souhaiterions :
+ rechercher dans un fichier `.conllu` tous les segments (continus ou discontinus) correspondant à des MWE et les annoter
+ rechercher dans un fichier `.conllu` tous les segments (continus ou discontinus) annotés comme des MWE et vérifier qu'il s'agit bien de MWE
+ pour ce dernier objectif, peut-être une dimension interactive où on demande à l'utilisateur s'il s'agit d'une MWE et on avise selon la réponse (effacement de l'annotation, conservation de l'annotation, modification de l'annotation)

Pour effectuer ces tâches, nous auront (probablement) besoin :
+ d'un moyen efficace de parcourir les `.conllu`
+ d'un lexique de MWE à repérer
+ d'un ou plusieurs lexiques contenant les annotations correctes à faire pour les MWE
+ et donc d'un typage des MWE (1 type = 1 schéma d'annotation)

Les difficultés sont les suivantes :
+ qu'est-ce qu'une MWE ?
+ comment repérer les MWE qui sont discontinues ?
+ comment repérer uniquement les MWE (éviter le bruit) ?
+ comment s'assurer que l'annotation en dépendance reste correcte, malgré les modifications engendrées par l'annotation d'une MWE (changement de tête) ?

# D'où vient l'idée ?

Cette idée de sujet a plusieurs origines. 
Tout d'abord, nous avons pu nous rendre compte dans plusieurs cours que les MWE posent (ou peuvent poser) un problème conséquent. C'est notamment le cas pour l'analyse syntaxique : dans une MWE, qui est la tête ? Y-a-t il une catégorie globale pour le tout ? Cela influence l'analyse obtenue (lien gouverneur-tête voire nom de la relation de dépendance).
Ensuite, Aline a eu l'occasion de travailler sur l'annotation du corpus [French Spoken](https://github.com/UniversalDependencies/UD_French-Spoken). Dans le cadre de ce travail, la question de la gestion des MWEs s'est posée.

# Chronologie

+ **11 nov. 2018** : début de réflexion sur le sujet du projet
+ **14 nov. 2018** : sujet global fixé, approuvé par les enseignants
+ **du 14 nov. 2018 au ?? déc. 2018** : recherche de documentation sur les MWE

# Plan d'attaque

D'abord, nous avons pensé qu'il était important de rechercher de la documentation sur les MWEs. Cette catégorie est en effet très vaste et assez hétéroclite, pour notre projet nous avons donc décidé de nous concentrer seulement sur quelques types de MWE.
