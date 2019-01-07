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

D'après la lecture de (Kahane, Courtin et Gerdes, 2018) et des discussions sur le traitement des MWEs dans UD ([Working Group on Multiword Expressions](https://github.com/UniversalDependencies/docs/blob/pages-source/workgroups/mwe.md)), nous avons ciblé notre travail avec deux approches en parallèle :

A. Elaboration de lexique
1. Faire une liste de MWEs que nous souhaitons repérer dans les corpus
2. Faire un lexique qui indique comment ces MWEs doivent être annotées

B. Nettoyage de corpus
1. Rechercher tous les segments annotés avec des liens 'fixed' dans le corpus
2. Vérifier que les segments sont dans le lexiques des MWEs devant être annotées avec un 'fixed'
3. Ajouter le trait MWEPOS/INMWE s'il n'y est pas
4. Si le segment n'est dans aucun lexique, stocker la phrase qui le contient dans un fichier : l'utilisateur pourra consulter ce fichier pour ensuite procéder à une annotation manuelle/augmenter les lexiques

Nous travaillerons sur les lemmes pour éviter les problèmes liés à la flexion.

Exemple d'annotation :
```
1	ou	ou	CCONJ	_	_	5	cc	_	MWEPOS=CCONJ
2	bien	bien	ADV	_	_	1	fixed	_	INMWE=Yes
3	vous	vous	PRON	_	_	5	nsubj	_	_
4	le	le	PRON	_	_	5	obj	_	_
5	pensez	penser	VERB	_	_	0	root	_	_
6	vraiment	vraiment	ADV	_	_	5	advmod	_	_
```


```
1	euh	euh	INTJ	_	_	4	discourse	_	_
2	il	il	PRON	_	_	4	nsubj:expl	_	_
3	y	y	PRON	_	_	4	iobj	_	_
4	a	avoir	VERB	_	_	0	root	_	_
5	un	un	DET	_	_	6	det	_	_
6	stade	stade	NOUN	_	_	4	obj	_	_
7	aussi	aussi	ADV	_	_	4	advmod	_	_
8	à	à	ADP	_	_	9	case	_	INMWE=Yes
9	côté	côté	NOUN	_	_	4	obl:mod	_	MWEPOS=ADV
```
