# Description

Ce dossier est le dossier de travail de Aline.

# Contenu

+ `brouillon.py` : première ébauche de script pour le projet. Ce script se concentre sur les éléments annotés `fixed` dans un corpus. Il repère ces éléments et vérifient s'ils font bien partie d'un lexique de MWEs à annoter en `fixed`. Si c'est le cas, le script ajoute un trait `MWEPOS/INMWE` ; si ce n'est pas le cas, la phrase contenant la ou les MWEs potentielles est écrité dans un fichier de sortie, où la ou les MWEs sont mises en évidence. Pour lancer le script `python3 brouillon.py chemin_du_corpus chemin_du_lexique` soit par exemple `python3 brouillon.py ../Corpus/fr_spoken-ud-train.conllu ./lexiqueFIXED_POS.tsv`
+ `traitement_conllu.py` : script qui sert de module dans le script `brouillon.py` et qui permet notamment de lire un fichier conllu.
+ `sortie_candidats.txt` : la sortie après l'exécution du script `brouillon.py` qui contient les phrases avec la ou les MWEs potentielles mises en évidence
+ `lexiqueFIXED_POS.tsv` : lexique de MWE à annoter en fixed. Première colonne --> les MWEs, deuxième colonne --> la POS du tout, à mettre derrière le trait 'MWEPOS='
+ `lexiqueNO.txt` : un lexique d'éléments annotés en `fixed` dans les treebanks UD du français qui ne devraient pas l'être
+ `lexiqueSYNT_POS.tsv` : lexique de MWEs à annoter en syntaxe (soit de manière régulière), avec dans la deuxième colonne la POS à mettre derrière le trait `MWEPOS=`

# Ce qui reste à faire, dans l'idéal

A. Elaborer d'autres lexiques

B. Faire un script qui permet de :

1. Repérer les MWEs par le texte (pas les relations de dépendance) ?
2. Proposer des schémas pour annoter en syntaxe des MWEs : ça pourrait prendre la forme d'un lexique avec des portions de conllu ; il faudrait bien sûr que ça permette de conserver une annotation correcte et cohérente des relations de syntaxe !
3. Pour le fichier de sortie qui présente les problèmes/candidats MWEs potentiels, on pourrait imaginer une sortie html un peu plus visuelle, avec des couleurs pour mettre les MWEs en évidence. Mais ce n'est pas vraiment la priorité...
4. Eventuellement, modifier le script pour qu'il devienne interactif : plutôt que de faire une sortie de MWEs potentielles, on peut imaginer que le script demande à l'utilisateur et que selon sa réponse, le comportement du logiciel change. Mais encore une fois, ce n'est pas vraiment une priorité je pense... 

# Origine des lexiques

Les lexiques sont disponibles [ici](https://github.com/bguil/UD-French-discussion).

Plus d'infos sur les lexiques :

"Voici deux fichiers .tsv de lexiques obtenus d'après le tableur [Framacalc](https://lite.framacalc.org/fixed_UD_French). 
Les POS ont été ajoutées en partie automatiquement à partir du lexique d'Orféo et en partie manuellement.
Ces fichiers doivent être corrigés sur deux points principaux : 1.les candidats MWE (ex. "à côté de") 2.les POS.

Le fichier "lexiqueNO.txt" contient une liste de termes qui ne sont (normalement) pas retenus comme MWE.
Le fichier "lexiqueDESACCORD.txt" contient une liste de termes pour lesquels il faut décider s'il s'agit de MWE ou pas, et si oui, s'ils sont fixed ou à analyser automatiquement."
