# Projet universitaire dans le cadre du master 2 TAL Plurital (Inalco-Nanterre-Paris III)
#### Mati�re
Langage de script (programmation Python pour le TAL)

##### Auteurs
Aline Etienne, Elena Edelman, Victorien Villiers

##### Sujet du projet
Gestion de MWEs dans un fichier conllu

#### Lien vers le git : https://github.com/Victorien-V/MWE-project-M2-NLP

# Corpus
Corpus universel du fran�ais parl� au format conllu convertie automatiquement depuis le treebank Rhapsodie (http://www.projet-rhapsodie.fr/).

Divis� en 3 sous-corpus (train, dev, test) :
+ fr_spoken-ud-train.conllu 1153 sentences  14952 tokens
+ fr_spoken-ud-dev.conllu 907 sentences 10010 tokens
+ fr_spoken-ud-test.conllu  726 sentences 10010 tokens
+ total 2786 sentences 34972 tokens

R�sum� :
+ �chantillonnage et genre : corpus de fran�ais parl� annot� pour la prosodie et la syntaxe, int�grant des informations sur les rections, d�pendances (arbres syntaxiques ou treebank) et cat�gories grammaticales au format tabulaire
+ Modalit� : oral, �chantillon de 30 heures de parole, regroupant des transcriptions d'interview, de parole libre, de commentaires sportifs, etc. issus d'une compilation de corpus externes et internes au projet
+ Taille : retranscription de 30h de parole
+ Documentation : corpus annot� issus des travaux r�alis�s par les �quipes de MODYCO, de l'IRCAM, du LATTICE, de l'ERSS et du LPL. Lien vers les publications : https://www.projet-rhapsodie.fr/bibliographie/
+ Licence et droit d'utilisation : Licence Creative Commons Attribution, citation des sources des corpus dans le respect des propri�t�s intellectuelles selon qu'il s'agisse de corpus externe ou interne 

# Travail d�finitoire
voir le fichier "resume_KahaneCourtinGerdes.txt"

# Liens utiles
voir le fichier "liens_utiles.txt"

# R�sum� du projet et �tapes

Pour ce projet, notre objectif est de pouvoir g�rer les Multi-Word Expressions (MWE) pr�sentes dans un fichier `.conllu`.

Dans l'id�al, nous souhaiterions :
+ rechercher dans un fichier `.conllu` tous les segments (continus ou discontinus) correspondant � des MWE et les annoter
+ rechercher dans un fichier `.conllu` tous les segments (continus ou discontinus) annot�s comme des MWE et v�rifier qu'il s'agit bien de MWE
+ pour ce dernier objectif, peut-�tre une dimension interactive o� on demande � l'utilisateur s'il s'agit d'une MWE et on avise selon la r�ponse (effacement de l'annotation, conservation de l'annotation, modification de l'annotation)

Pour effectuer ces t�ches, nous aurons (probablement) besoin :
+ d'un moyen efficace de parcourir les `.conllu`
+ d'un lexique de MWE � rep�rer
+ d'un ou plusieurs lexiques contenant les annotations correctes � faire pour les MWE
+ et donc d'un typage des MWE (1 type = 1 sch�ma d'annotation)

Les difficult�s sont les suivantes :
+ qu'est-ce qu'une MWE ?
+ comment rep�rer les MWE qui sont discontinues ?
+ comment rep�rer uniquement les MWE (�viter le bruit) ?
+ comment s'assurer que l'annotation en d�pendance reste correcte, malgr� les modifications engendr�es par l'annotation d'une MWE (changement de t�te) ?

# D'o� vient l'id�e ?

Cette id�e de sujet a plusieurs origines. 
Tout d'abord, nous avons pu nous rendre compte dans plusieurs cours que les MWE posent (ou peuvent poser) un probl�me cons�quent. C'est notamment le cas pour l'analyse syntaxique : dans une MWE, qui est la t�te ? Y-a-t il une cat�gorie globale pour le tout ? Cela influence l'analyse obtenue (lien gouverneur-t�te voire nom de la relation de d�pendance).
Ensuite, Aline a eu l'occasion de travailler sur l'annotation du corpus [French Spoken](https://github.com/UniversalDependencies/UD_French-Spoken). Dans le cadre de ce travail, la question de la gestion des MWEs s'est pos�e.

# Chronologie

+ **11 nov. 2018** : d�but de r�flexion sur le sujet du projet
+ **14 nov. 2018** : sujet global fix�, approuv� par les enseignants
+ **du 14 nov. 2018 au 24 d�c. 2018** : recherche de documentation sur les MWE

# Plan d'attaque (�l�ments r�alis�s)

D'abord, nous avons pens� qu'il �tait important de rechercher de la documentation sur les MWEs. Cette cat�gorie est en effet tr�s vaste et assez h�t�roclite, pour notre projet nous avons donc d�cid� de nous concentrer seulement sur quelques types de MWE.

D'apr�s la lecture de (Kahane, Courtin et Gerdes, 2018) et des discussions sur le traitement des MWEs dans UD ([Working Group on Multiword Expressions](https://github.com/UniversalDependencies/docs/blob/pages-source/workgroups/mwe.md)), nous avons cibl� notre travail avec deux approches en parall�le :

A. Elaboration de lexique
1. Faire une liste de MWEs que nous souhaitons rep�rer dans les corpus
2. Faire un lexique qui indique comment ces MWEs doivent �tre annot�es

B. Nettoyage de corpus
1. Rechercher tous les segments annot�s avec des liens 'fixed' dans le corpus
2. V�rifier que les segments sont dans le lexiques des MWEs devant �tre annot�es avec un 'fixed'
3. Ajouter le trait MWEPOS/INMWE s'il n'y est pas
4. Si le segment n'est dans aucun lexique, stocker la phrase qui le contient dans un fichier : l'utilisateur pourra consulter ce fichier pour ensuite proc�der � une annotation manuelle/augmenter les lexiques

Nous travaillerons sur les lemmes pour �viter les probl�mes li�s � la flexion.

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
8	�	�	ADP	_	_	9	case	_	INMWE=Yes
9	c�t�	c�t�	NOUN	_	_	4	obl:mod	_	MWEPOS=ADV
```

# Pour la suite... (ce que nous pourrions encore faire, dans l'id�al)

A. Elaborer d'autres lexiques

B. Faire un script qui permet de :

1. Rep�rer les MWEs par le texte (pas les relations de d�pendance) ?
2. Proposer des sch�mas pour annoter en syntaxe des MWEs : �a pourrait prendre la forme d'un lexique avec des portions de conllu ; il faudrait bien s�r que �a permette de conserver une annotation correcte et coh�rente des relations de syntaxe !
3. Pour le fichier de sortie qui pr�sente les probl�mes/candidats MWEs potentiels, on pourrait imaginer une sortie html un peu plus visuelle, avec des couleurs pour mettre les MWEs en �vidence. Mais ce n'est pas vraiment la priorit�...
4. Eventuellement, modifier le script pour qu'il devienne interactif : plut�t que de faire une sortie de MWEs potentielles, on peut imaginer que le script demande � l'utilisateur et que selon sa r�ponse, le comportement du logiciel change. Mais encore une fois, ce n'est pas vraiment une priorit� je pense... 

