#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys #pour accéder aux arguments fournis en ligne de commande
import traitement_conllu as tc
from collections import defaultdict
import re

#------Fonctions------
def defait_liste(liste):
	"""
	entrée : une liste
	sortie : une autre liste
	permet de transformer une liste du type [[1,2],[3,4]] en [1,2,3,4]
	"""
	liste2=[]
	for e in liste :
		liste2.extend(e)
	return liste2
	
def dico_lexique(path):
	"""
	prend le chemin d'un lexique au format .tsv
	retourne un dico avec en clé la MWE et en valeur la POS
	"""
	
	dico_lexique={line.split("\t")[0]:line.split("\t")[1] for line in open(path).read().split("\n")}
	
	return dico_lexique

def tri_lexique_relation(conllu,lexique,relation):
	"""
	entrée : un conllu issu de read_file(), un lexique, une relation de dépendance
	sortie :
	- un dico {phrase du conllu : les suites de mots présentes dans le lexique, pour cette phrase}
	- un dico {phrase du conllu : les suites de mots absentes du lexique, pour cette phrase}
	"""
	
	#les deux dico à retourner
	dans_lexique=defaultdict(lambda:list())
	pas_dans_lexique=defaultdict(lambda:list())

	for phrase in conllu: #pour chaque phrase du conllu
		for mot in phrase.tree: #on regarde chaque mot
			id_mot=mot.nid #on stocke son identifiant
			#on reconstitue la MWE potentielle sous forme de liste d'objets Word
			#le filtrage se fait de la manière suivante : 
			#on parcourt à nouveau l'arbre à la recherche de mot2 gouvernés par le 1er mot et ce par la relation qui nous intéresse
			mwe=[mot2 for mot2 in phrase.tree if mot2.head == id_mot and mot2.deprel == relation]
			
			if mwe: #si la liste n'est pas vide (soit s'il y a une suite de mots correspondant à nos critères)
				mwe.append(mot) #on ajoute le mot censé être le gouverneur
				#print(' '.join([m.form for m in sorted(mwe, key=lambda x:x.nid)]))
				#on reconstitue le candidat en triant sur l'identifiant pour retrouver la linéarité
				#on prend les lemmes puisque notre lexique est en lemmes
				mwe=sorted(mwe, key=lambda x:x.nid)
				candidat=' '.join([m.lemma for m in mwe])
				candidat=re.sub("\+le",'',candidat)
				if candidat in lexique: #si le candidat est dans le lexique
					#ajout du trait MWEPOS/INMWE pour les 'fixed'
					if relation == "fixed":
						mwe[0].misc='MWEPOS='+lexique[candidat] #pour le 1er élément de la MWE
						for m in mwe[1:]:
							m.misc='INMWE=Yes'
					dans_lexique[phrase].append(mwe)
				else:
					pas_dans_lexique[phrase].append(mwe)
		mwe.clear() #ne pas oublier de vider la liste qui sert à reconstituer les mwes potentielles !
		
	return dans_lexique,pas_dans_lexique


#------Variables------
p_corpus=sys.argv[1] #chemin du corpus
p_lexique_fixed=sys.argv[2] #chemin du lexique MWE fixed
#print(p_corpus+'\n'+p_lexique_fixed)

#------Exécution------
if __name__ == '__main__':

	#on stocke le corpus dans la variable corpus en appelant la fonction 'read_file' de 'traitement_conllu'
	#on obtient une liste d'objets Sent(), contenant eux-mêmes des arbres (tree) qui sont des listes d'objets Word()
	corpus=tc.read_file(p_corpus)
	#print(corpus[0].text+'\n'+corpus[0].tree[0].lemma)

	#on récupère le lexique et on le stocke dans un dico
	lexique_fixed=dico_lexique(p_lexique_fixed)
	#print(type(lexique_fixed),lexique_fixed)
	
	#pour chaque mot, on regarde s'il gouverne d'autres mots par un lien 'fixed'
	dans_lexique_fixed,pas_dans_lexique_fixed=tri_lexique_relation(corpus,lexique_fixed,'fixed')
	
	#---Nouveau fichier avec les MWE avec un trait MWEPOS/INMWE
	corpus2=corpus[:] #on copie notre corpus initial
	
	#pour chaque phrase, on va remplacer les mots des mwes par ceux modifiés (avec le trait MWEPOS/INMWE)
	for phrase in corpus2:
		if phrase in dans_lexique_fixed :
			mwes=defait_liste(dans_lexique_fixed[phrase]) #liste de tous les mots de toutes les mwes dans la phrase
			for mot in phrase.tree :
				for m in mwes :
					if mot.nid == m.nid : #comme on est dans la même phrase, deux mots ayant le même identifiant ne font qu'un
						mot=m #on remplace
	
	#écriture du nouveau conllu grâce à la fonction ecrit_nouveau() du module traitement_conllu
	tc.ecrit_nouveau(corpus2,"conllu_modifie.conllu")
	
	#---Sortie avec les cas à présenter à l'utilisateur
	
	with open("sortie_candidats.html",'w', encoding="utf-8") as out :
		out.write("<html><head></head><body style=background-color:#FFFFF0><h3><p>Résultat:</p><p>Les candidats MWEs sont entre '[]' dans le texte de la phrase qui les contient.</p></h3>")
		for phrase in pas_dans_lexique_fixed:
			out.write("<p style=color:#ff0000># sent_id = "+phrase.id+"</p>\n<p style=color:#0000ff><b><i><big> # text = ")
			id_debut_mwe=[mwe[0].nid for mwe in pas_dans_lexique_fixed[phrase]]
			id_fin_mwe=[mwe[-1].nid for mwe in pas_dans_lexique_fixed[phrase]]

			for mot in phrase.tree :
				if mot.nid in id_debut_mwe :
					out.write("[ ")
				out.write(mot.form+' ')
				if mot.nid in id_fin_mwe :
					out.write("] ")
			out.write("\n</big></i></b></p>")
			
			for w in phrase.tree :
				if w.nid in id_debut_mwe :
					out.write("<p><big><b>------Debut MWE------</b></big></p>")
				out.write(
					"<table border=1 cellspacing=0 cellpadding=10 width=450><tr><td align=center>"+w.nid+"</td><td align=center>"+w.form+"</td><td align=center>"+w.lemma+"</td><td align=center>"+w.upos+"</td><td align=center>"+w.xpos+"</td><td align=center>"+w.feats+"</td><td align=center>"+w.head+"</td><td align=center>"+w.deprel+"</td><td align=center>"+w.deps+"</td><td align=center>"+w.misc+"</td></tr></table>\n"
				)
				if w.nid in id_fin_mwe :
					out.write("<p><big><b>------Fin MWE------</b></big></p>\n\n\n")
			out.write("</body></html>\n")
	
	