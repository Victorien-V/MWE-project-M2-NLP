#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys #pour accéder aux arguments fournis en ligne de commande
import traitement_conllu as tc

#------Fonctions------
def dico_lexique(path):
	"""
	prend le chemin d'un lexique au format .tsv
	retourne un dico avec en clé la MWE et en valeur la POS
	"""
	
	dico_lexique={line.split("\t")[0]:line.split("\t")[1] for line in open(path).read().split("\n")}
	
	return dico_lexique

#------Variables------
p_corpus=sys.argv[1] #chemin du corpus
p_lexique_fixed=sys.argv[2] #chemin du lexique MWE fixed
print(p_corpus+'\n'+p_lexique_fixed)

#------Exécution------
if __name__ == '__main__':

	#on stocke le corpus dans la variable corpus en appelant la fonction 'read_file' de 'traitement_conllu'
	#on obtient une liste d'objets Sent(), contenant eux-mêmes des arbres (tree) qui sont des listes d'objets Word()
	corpus=tc.read_file(p_corpus)
	print(corpus[0].text+'\n'+corpus[0].tree[0].lemma)

	#on récupère le lexique et on le stocke dans un dico
	lexique_fixed=dico_lexique(p_lexique_fixed)
	print(type(lexique_fixed),lexique_fixed)
	
	#on parcourt le corpus à la recherce d'éléments annotés en fixed
	#s'ils sont dans le lexique, on leur met le trait MWE approprié
	#s'ils ne sont pas dans le lexique, on met les phrases concernées dans un fichier de sortie à l'attention de l'utilisateur
	for phrase in corpus:
		mwes=[]
		mwe=[]
		for mot in phrase.tree:
			if mot.deprel == "fixed":
				
				mwes.extend([phrase.tree[int(mot.head)-1],mot])
					
		for m in mwes:
			print(m.form)