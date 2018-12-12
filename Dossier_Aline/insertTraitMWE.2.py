# coding: utf-8

import re

def constitutionDicoMWE(dictionnaire):
    """
    argument : un fichier au format .tsv, encodé en utf-8 (et unix)
    retour : le dico mwe/POS
    """
    dicoMWE={}
    with open(dictionnaire,encoding="utf-8") as dico:
        for ligne in dico:
            ligne = ligne.rstrip()
            mwe, POS, tete = ligne.split('\t')
            dicoMWE[mwe]=(POS,tete)
    return dicoMWE

def traitementConll(fichierEntree,dicoMWE,fichierSortie="resultatTraitement.2.conllu"):
    """
    arguments : un fichier conll (en utf-8), un dico mwe/POS, un fichier de sortie (par exemple en conll)
    retour : une liste contenant le fichier conll modifié
    +écrit ce nouveau fichier dans le fichier de sortie spécifié en argument
    """
    nouveau=[] #liste qui va accueillir le fichier modifié
    n=re.compile("\n\n")
    #(n°)\t(token)\t(lemme)\t(POS)\t(_)\t(_)\t(n°gouv)\t(relation)\t(_)\t(_)
    motif=re.compile("(\d+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t])+\t([^\t])+\t(\d+)\t([^\t])+\t([^\t])+\t([^\t]+)")
    doc=n.split(open(fichierEntree,encoding="utf-8").read())
    
    for item in doc:
    #---------DECOUPAGE DU CONLL ET RECUPERATION DES DONNEES UTILES---------------
        phrase,dicoLignes=[],{} #doivent être réinitialisées pour chaque énoncé du conll
        lignes=item.split("\n") #récupération de chaque ligne
        for ligne in lignes:
            match=re.match(motif,ligne)
            if not(match):
                if "sent_id" in ligne: #pour réintroduire une ligne vide avant chaque énoncé
                    nouveau.append("\n"+ligne)
                else:
                    nouveau.append(ligne)
            elif match:
                num,token,lemme,pos,a,b,numGouv,c,d,dernier=match.group(1),match.group(2),match.group(3),match.group(4),match.group(5),match.group(6),match.group(7),match.group(8),match.group(9),match.group(10)
                #phrase.append(token) #on reconstitue la phrase dans une liste pour pouvoir ensuite chercher la mwe
                phrase.append(lemme)
                dicoLignes[num]=(ligne,dernier,numGouv) 
                nouveau.append(ligne)           
    #---------REPERAGE ET TRAITEMENT DES MWEs---------------
        for mwe in dicoMWE: #pour chaque clé mwe
            mwe2=mwe.split(' ') #on récupère les éléments de la mwe
            l=len(mwe2) #et la longueur de la mwe
            for x in range(0,len(phrase)):
                if phrase[x:x+l]==mwe2[0:l]: #on cherche la mwe dans la liste de lemme (ou de tokens)
                    for y in range(x+1,x+l+1): #NB: les indices de token ont +1 par rapport à ceux de la liste
                    #on va remplacer la 10e colonne, mais deux cas : tête ou dépendant
                        if phrase[y-1]==dicoMWE[mwe][1]: #est la tête
                            modif=re.sub(dicoLignes[str(y)][1]+'$','MWEPOS='+dicoMWE[mwe][0],dicoLignes[str(y)][0])
                        else:
                            modif=re.sub(dicoLignes[str(y)][1]+'$','INMWE=yes',dicoLignes[str(y)][0])                                                                     
                        for z in range(0,len(nouveau)): #on remplace les lignes avec mwe par la modification
                            if nouveau[z]==dicoLignes[str(y)][0]:
                                nouveau[z]=modif
    #---------ECRITURE DU FICHIER CONLL MODIFIE---------------
    nouveau[0]=re.sub('^\n','',nouveau[0]) #on supprime le retour à la ligne en tête de la 1ère ligne du conll
    with open(fichierSortie,'w',encoding="utf-8") as sortie:
        for i in range(0,len(nouveau)):
            #print(nouveau[i])
            sortie.write(nouveau[i]+'\n')
    return nouveau

#------------EXECUTION----------------------------------------
dico=input("Quel est le fichier .tsv contenant les MWE ? ")
conll=input("Quel est le fichier conll à modifier ? ")
sortie=input("Quel est le fichier de sortie ? Appuyer sur entrée pour conserver la valeur par défaut ('resultatTraitement.conllu'). ")
dicoMWE=constitutionDicoMWE(dico.rstrip())
#dicoMWE=constitutionDicoMWE("dico2.tsv")
#print(dicoMWE)
if sortie != '':
    resultat=traitementConll(conll.rstrip(),dicoMWE,sortie)
else:
    resultat=traitementConll(conll.rstrip(),dicoMWE)
#resultat=traitementConll("fr_spoken-ud-dev.conllu",dicoMWE)
#print(resultat)