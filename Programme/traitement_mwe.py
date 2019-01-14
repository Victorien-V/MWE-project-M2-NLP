#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Pour lancer le script :
python3 traitement_mwe.py corpus.conllu lexique_fixed.tsv lexique_synt.tsv

Par exemple :
python3 traitement_mwe.py ../Corpus/fr_spoken-ud-train.conllu  lexiqueFIXED_POS.tsv lexique_test.tsv
"""

import sys #pour accéder aux arguments fournis en ligne de commande
import traitement_conllu as tc #pour lire et stocker le conllu
from collections import defaultdict
import re
import nltk #pour les n-grammes de lemmes

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
	retourne un dico avec en clé la MWE et en valeur la POS (ou un tuple (POS,position tête))
	"""
	try : #cas des lexiques de la forme mwe\tPOS\tposition_de_la_tête
		dico_lexique={line.split("\t")[0]:(line.split("\t")[1],line.split("\t")[2]) for line in open(path).read().split("\n")}
	except IndexError : #cas des lexiques de la forme mwe\tPOS
		dico_lexique={line.split("\t")[0]:line.split("\t")[1] for line in open(path).read().split("\n")}
	
	return dico_lexique

def tri_lexique_relation(conllu,lexique,relation):
	"""
	utilise une relation de dépendance prédéfinie pour repérer des suites de mots dans un corpus
	trie ensuite ces suites de mots selon si elles sont dans un lexique ou pas
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

def lex2ngrams(path):
	"""
	prend le chemin d'un lexique au format .tsv
	retourne cinq listes : le lexique complet et la liste des mwe à 2, 3, 4 et 5 tokens
	"""
	
	lex_list = list()
	lex_2g = list()
	lex_3g = list()
	lex_4g = list()
	lex_5g = list()
	with open(path, encoding="utf-8") as f:
		for line in f:
			lex_list.append(line.split("\t")[0])	
	
	for mwe in lex_list:
		if len(mwe.split(" ")) == 2:
			lex_2g.append(mwe.split(" "))
		if len(mwe.split(" ")) == 3:
			lex_3g.append(mwe.split(" "))
		if len(mwe.split(" ")) == 4:
			lex_4g.append(mwe.split(" "))
		if len(mwe.split(" ")) == 5:
			lex_5g.append(mwe.split(" "))
	
	return lex_list, lex_2g, lex_3g, lex_4g, lex_5g
	
def tuple2list(lem_tuple):
	"""
	prend une liste de tuples de n-grams
	retourne une liste de listes de n-grams
	"""
	
	lem_list = list()
	for elem in lem_tuple:
		lem_list.append(list(elem))
	return lem_list
	
def pop_ngram(lem_list, lem_gram, lex_gram, mwe_list):
	"""
	vérifie les n-gram d'un lexique sont présents dans une liste
	de n-grams et les supprime le cas échéant
	
	lem_list = la liste à modifier
	lem_gram = cette même liste, contenant les n-gram à parcourir
	lex_gram = le lexique contenant les n-gram à trouver
	
	retourne la liste de lemmes sans les n-gram
	"""
	new_lem_gram = tuple2list(lem_gram)
	for elem in new_lem_gram:
			if elem in lex_gram:
				mwe_list.append(elem)
				try:
					for token in elem:
						lem_list.remove(token)
				except:
					pass
					
	return lem_list, mwe_list
	
def match_indices(mwe,lemmes):
	"""
	entrée : une mwe sous forme de liste, une liste de lemmes
	sortie : une liste de listes d'indices, si la mwe est dans la liste de lemmes
	"""
	i=0
	liste_indices=[]
	while i < len(lemmes): #on parcourt la liste de lemmes
		if lemmes[i] == mwe[0] : #si un élément correspond au 1er élément de la mwe
			indices=[] #on crée une liste qui va accueillir les indices correspondant aux mots de la mwe
			for j in range(len(mwe)):
				try:
					if lemmes[i+j] == mwe[j]:
						indices.append(i+j)
					else:
						indices.clear()
				except IndexError:
					indices.clear()
			if len(mwe) != len(indices):
				indices.clear()
			if indices :
				liste_indices.append(indices)
			i=i+j
		else:
			i+=1
		
	return liste_indices
		
def match_indices2(lex,lemmes):
	"""
	complète la fonction match_indices()
	entrée :
	- une liste correspondant à un lexique de mwe
	- une liste de lemmes
	"""
	liste_indicesMWE=[]
	for mwe in lex:
		indices=match_indices(mwe,lemmes)
		if indices:
			#print(indices)
			liste_indicesMWE.append((indices, " ".join(mwe)))
			
	return liste_indicesMWE
	
def tri_lexique_lemme(corpus,lex_5g,lex_4g,lex_3g,lex_2g,dict_lexique):
	"""
	dans un corpus, retrouve les mwes d'un lexique donné en passant par les lemmes
	entrée : 
	- corpus .conllu (lu par read_file())
	- lexiques de mwe ordonnées par tailles de mwe
	- dico {'mwe' : 'POS associée'}
	sortie :
	- dico {phrase : [liste de mots Word correspondant aux mwes de la phrase]}
	"""
	
	phrase_liste_mwe=defaultdict(lambda:list()) #dico des {phrase : [liste de Word qui constituent les mwe de la phrase]}
	
	for phrase in corpus:	
		lemmes=[lemme[0] for lemme in phrase.lem_list] #on stocke la liste de lemmes
		
		#pour chaque mwe, si elle est dans la phrase, 
		#on récupère les indices correspondants à la position des lemmes dans la liste de lemmes	
		
		indices_phrase=[
			match_indices2(lex_5g,lemmes),
			match_indices2(lex_4g,lemmes),
			match_indices2(lex_3g,lemmes),
			match_indices2(lex_2g,lemmes),
		]
		
		#on va remplacer chaque indice par le mot Word correspondant
		for mwe in indices_phrase :
			if mwe: #s'il y a au moins un tuple ([liste d'indices],'mwe')
				for couple in mwe:
					#on traite les indices d'abord
					for item in couple[0]: #au cas où une même mwe soit plusieurs fois dans une même phrase
						for i in item : #pour chaque indice
							mot=phrase.lem_list[i][1] #on récupère le Word associé au lemme grâce à l'indice
							#print(mot.form)
							if item.index(i) == int(dict_lexique[couple[1]][1])-1 : mot.misc = "MWEPOS="+dict_lexique[couple[1]][0] #pour la tête
							else : mot.misc = "INMWEPOS=Yes"
							
							phrase_liste_mwe[phrase].append(mot)
							
	return phrase_liste_mwe

#------Variables------
path_corpus=sys.argv[1] #chemin du corpus
path_lexique_fixed=sys.argv[2] #chemin du lexique MWE fixed
path_lexique_synt=sys.argv[3] #chemin du lexique MWE non-fixed
#print(path_corpus+'\n'+path_lexique_fixed+'\n'+path_lexique_synt)

#------Exécution------
if __name__ == '__main__':

	#on stocke le corpus dans la variable corpus en appelant la fonction 'read_file' de 'traitement_conllu'
	#on obtient une liste d'objets Sent(), contenant eux-mêmes des arbres (tree) qui sont des listes d'objets Word()
	corpus=tc.read_file(path_corpus)
	#print(corpus[0].text+'\n'+corpus[0].tree[0].lemma)

	#on récupère le lexique et on le stocke dans un dico
	lexique_fixed=dico_lexique(path_lexique_fixed)
	lexique_synt=dico_lexique(path_lexique_synt)
	
	#pour chaque mot, on regarde s'il gouverne d'autres mots par un lien 'fixed'
	dans_lexique_fixed,pas_dans_lexique_fixed=tri_lexique_relation(corpus,lexique_fixed,'fixed')
	
	#on récupère le lexique en entrée qu'on divise en sous-listes selon le nombre de tokens
	lexique, lex_2g, lex_3g, lex_4g, lex_5g = lex2ngrams(path_lexique_synt)
	#on parcourt le corpus par les lemmes, à la recherce de mwe
	dico_phrases_mwes=tri_lexique_lemme(corpus,lex_5g,lex_4g,lex_3g,lex_2g,lexique_synt)
	
	#---Nouveau fichier avec les MWE avec un trait MWEPOS/INMWE
	corpus2=corpus[:] #on copie notre corpus initial
	
	#pour chaque phrase, on va remplacer les mots des mwes par ceux modifiés (avec le trait MWEPOS/INMWE)
	for phrase in corpus2:
		if phrase in dans_lexique_fixed : #les phrases avec des MWEs annotées en 'fixed'
			mwes=defait_liste(dans_lexique_fixed[phrase]) #liste de tous les mots de toutes les mwes dans la phrase
			for mot in phrase.tree :
				for m in mwes :
					if mot.nid == m.nid : #comme on est dans la même phrase, deux mots ayant le même identifiant ne font qu'un
						mot=m #on remplace
	
		if phrase in dico_phrases_mwes: #les phrases avec des MWEs annotées autrement
			for mot in phrase.tree:
				for m in dico_phrases_mwes[phrase]:
					if mot.nid == m.nid :
						mot = m
			
	
	#écriture du nouveau conllu grâce à la fonction ecrit_nouveau() du module traitement_conllu
	tc.ecrit_nouveau(corpus2,"conllu_modifie.conllu")
	
	#---Sortie avec les cas à présenter à l'utilisateur
	
	with open("sortie_candidats.txt",'w',encoding="utf-8") as out :
		out.write("Les candidats MWEs sont entre '<>' dans le texte de la phrase qui les contient.\n\n\n")
		for phrase in pas_dans_lexique_fixed:
			out.write("# sent_id = "+phrase.id+"\n# text = ")
			id_debut_mwe=[mwe[0].nid for mwe in pas_dans_lexique_fixed[phrase]]
			id_fin_mwe=[mwe[-1].nid for mwe in pas_dans_lexique_fixed[phrase]]

			for mot in phrase.tree :
				if mot.nid in id_debut_mwe :
					out.write("< ")
				out.write(mot.form+' ')
				if mot.nid in id_fin_mwe :
					out.write("> ")
			out.write("\n")
			
			for w in phrase.tree :
				if w.nid in id_debut_mwe :
					out.write("#------Debut MWE------\n")
				out.write(
					w.nid+"\t"+w.form+"\t"+w.lemma+"\t"+w.upos+"\t"+w.xpos+"\t"+w.feats+"\t"+w.head+"\t"+w.deprel+"\t"+w.deps+"\t"+w.misc+"\n"
				)
				if w.nid in id_fin_mwe :
					out.write("#------Fin MWE------\n")
			out.write("\n")