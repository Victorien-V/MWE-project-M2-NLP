#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys #pour accéder aux arguments fournis en ligne de commande
import traitement_conllu as tc
import nltk

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
	
#------Variables------
p_corpus="fr_spoken-ud-train.conllu" #chemin du corpus
p_lexique_fixed="lexiqueFIXED_POS.tsv" #chemin du lexique MWE fixed
#print(p_corpus+'\n'+p_lexique_fixed)

#------Exécution------
if __name__ == '__main__':

	#on stocke le corpus dans la variable corpus en appelant la fonction 'read_file' de 'traitement_conllu'
	#on obtient une liste d'objets Sent(), contenant eux-mêmes des arbres (tree) qui sont des listes d'objets Word()
	corpus=tc.read_file(p_corpus)
	
	#on récupère le lexique en entrée qu'on divise en sous-listes selon le nombre de tokens
	lexique, lex_2g, lex_3g, lex_4g, lex_5g = lex2ngrams(p_lexique_fixed)
	
	#on parse le corpus à la recherche des mwe du lexique
	#on commencera par les mwe les plus longues, qu'on supprimera au fur et à mesure
	#afin d'éviter les doublons tels que "dès lors que" / "dès lors"
	for phrase in corpus:
		mwe_list = list()
		# on imprime l'id de l'arbre et les mwe trouvées grâce à la fonction pop_ngrams
		new_list, mwe_list = pop_ngram(phrase.lem_list, phrase.lem_5g, lex_5g, mwe_list)
		lem_4g = nltk.ngrams(new_list, 4)
		new_list, mwe_list = pop_ngram(new_list, phrase.lem_4g, lex_4g, mwe_list)
		lem_3g = nltk.trigrams(new_list)
		new_list, mwe_list = pop_ngram(new_list, phrase.lem_3g, lex_3g, mwe_list)
		lem_2g = nltk.bigrams(new_list)
		new_list, mwe_list = pop_ngram(new_list, phrase.lem_2g, lex_2g, mwe_list)
		if len(mwe_list) > 0:
			line = ""
			line += phrase.id
			line += "\t"
			for elem in mwe_list:
				for token in elem:
					line += token
					line += " "
				line += "\t"
			print(line)

	# print(*map(' '.join, corpus[8].lem_2g), sep=', ')