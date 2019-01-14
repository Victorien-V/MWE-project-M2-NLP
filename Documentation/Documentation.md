# Projet universitaire dans le cadre du master 2 TAL Plurital (Inalco-Nanterre-Paris III)
#### Matière
Langage de script (programmation Python pour le TAL)

##### Auteurs
Aline Etienne, Elena Edelman, Victorien Villiers

##### Sujet du projet
Gestion de MWEs dans un fichier conllu

#### Lien vers le git : https://github.com/Victorien-V/MWE-project-M2-NLP

# Corpus
Corpus universel du français parlé au format conllu convertie automatiquement depuis le treebank Rhapsodie (http://www.projet-rhapsodie.fr/).

Divisé en 3 sous-corpus (train, dev, test) :
+ fr_spoken-ud-train.conllu 1153 sentences  14952 tokens
+ fr_spoken-ud-dev.conllu 907 sentences 10010 tokens
+ fr_spoken-ud-test.conllu  726 sentences 10010 tokens
+ total 2786 sentences 34972 tokens

Résumé :
+ Échantillonnage et genre : corpus de français parlé annoté pour la prosodie et la syntaxe, intégrant des informations sur les rections, dépendances (arbres syntaxiques ou treebank) et catégories grammaticales au format tabulaire
+ Modalité : oral, échantillon de 30 heures de parole, regroupant des transcriptions d'interview, de parole libre, de commentaires sportifs, etc. issus d'une compilation de corpus externes et internes au projet
+ Taille : retranscription de 30h de parole
+ Documentation : corpus annoté issus des travaux réalisés par les équipes de MODYCO, de l'IRCAM, du LATTICE, de l'ERSS et du LPL. Lien vers les publications : https://www.projet-rhapsodie.fr/bibliographie/
+ Licence et droit d'utilisation : Licence Creative Commons Attribution, citation des sources des corpus dans le respect des propriétés intellectuelles selon qu'il s'agisse de corpus externe ou interne 

# Travail définitoire
voir le fichier "resume_KahaneCourtinGerdes.txt"

# Liens utiles
voir le fichier "liens_utiles.txt"

# Résumé du projet et étapes

Pour ce projet, notre objectif est de pouvoir gérer les Multi-Word Expressions (MWE) présentes dans un fichier `.conllu`.

Dans l'idéal, nous souhaiterions :
+ rechercher dans un fichier `.conllu` tous les segments (continus ou discontinus) correspondant à des MWE et les annoter
+ rechercher dans un fichier `.conllu` tous les segments (continus ou discontinus) annotés comme des MWE et vérifier qu'il s'agit bien de MWE
+ pour ce dernier objectif, peut-être une dimension interactive où on demande à l'utilisateur s'il s'agit d'une MWE et on avise selon la réponse (effacement de l'annotation, conservation de l'annotation, modification de l'annotation)

Pour effectuer ces tâches, nous aurons (probablement) besoin :
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
+ **du 14 nov. 2018 au 24 déc. 2018** : recherche de documentation sur les MWE

# Plan d'attaque (éléments réalisés)

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

# Exemple d'annotation en sortie :
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

# Pour la suite... (ce que nous pourrions encore faire, dans l'idéal)

A. Elaborer d'autres lexiques

B. Faire un script qui permet de :

1. Repérer les MWEs par le texte (pas les relations de dépendance) ?
2. Proposer des schémas pour annoter en syntaxe des MWEs : ça pourrait prendre la forme d'un lexique avec des portions de conllu ; il faudrait bien sûr que ça permette de conserver une annotation correcte et cohérente des relations de syntaxe !
3. Pour le fichier de sortie qui présente les problèmes/candidats MWEs potentiels, on pourrait imaginer une sortie html un peu plus visuelle, avec des couleurs pour mettre les MWEs en évidence. Mais ce n'est pas vraiment la priorité...
4. Eventuellement, modifier le script pour qu'il devienne interactif : plutôt que de faire une sortie de MWEs potentielles, on peut imaginer que le script demande à l'utilisateur et que selon sa réponse, le comportement du logiciel change. Mais encore une fois, ce n'est pas vraiment une priorité je pense... 

