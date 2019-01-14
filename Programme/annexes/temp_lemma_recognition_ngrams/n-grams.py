#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys #pour accéder aux arguments fournis en ligne de commande
import traitement_conllu as tc
import nltk
import re
from collections import defaultdict

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

def output2dict(output):
	"""
	prend en entrée un corpus tabulaire comprenant l'id de l'arbre et ses mwe
	retourne un dictionnaire avec comme clé l'id de l'arbre et comme valeurs ses mwe
	"""
	id_dict = defaultdict(list)
	with open(output, encoding="utf-8") as f:
		for line in f:
			tab = line.strip().split("\t")
			key = tab.pop(0)
			for elem in tab:
				id_dict[key].append(elem)
	return id_dict

def print_mot(mot):
	"""
	prend un mot en entrée et imprime les valeurs correspondantes en sortie
	"""
	out.write(mot.nid+"\t"+mot.form+"\t"+mot.lemma+"\t"+mot.upos+"\t"+mot.xpos+"\t"+mot.feats+"\t"+mot.head+"\t"+mot.deprel+"\t"+mot.deps+"\t"+mot.misc+"\n")
	
#------Variables------
p_corpus="fr_spoken-ud-train.conllu" #chemin du corpus
p_lexique_fixed="lexiqueFIXED_POS.tsv" #chemin du lexique MWE fixed
data_out = open("output.txt","w")
# data_out_2 = open("corpus_modifie.txt","w")

#------Exécution------
if __name__ == '__main__':

	#on stocke le corpus dans la variable corpus en appelant la fonction 'read_file' de 'traitement_conllu'
	# on obtient une liste d'objets Sent(), contenant eux-mêmes des arbres (tree) qui sont des listes d'objets Word()
	corpus=tc.read_file(p_corpus)
	
	# on récupère le lexique en entrée qu'on divise en sous-listes selon le nombre de tokens
	lexique, lex_2g, lex_3g, lex_4g, lex_5g = lex2ngrams(p_lexique_fixed)
	
	# on parse le corpus à la recherche des mwe du lexique
	# on ajoute les mwe à la ligne de sortie en partant de n-grams les plus longs (5-gram)
	# on supprime chaque nouvelle mwe afin d'éviter les doublons tels que "dès lors que" / "dès lors"
	# on crée en sortie un fichier tabulaire output.txt
	
	for phrase in corpus:
	
		mwe_list = list()
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
			line += "\n"
			line = re.sub(" \t\n", "\n", line)
			line = re.sub(" \t", "\t", line)
			
			data_out.write(line)
	
	data_out.close()
	
	# on crée un dictionnaire à partir du fichier tabulaire output.txt précédemment créé
	id_dict = output2dict("output.txt")
	
	# on copie le corpus d'origine afin de le modifier
	corpus_modifie=tc.read_file(p_corpus)
	
	# on parcoure le nouveau corpus afin de le modifier en regardant dans le dictionnaire des mwe
	with open("sortie_candidats.txt",'w',encoding="utf-8") as out :
		for phrase in corpus_modifie:
		
			out.write("# sent_id = "+phrase.id+"\n# text = "+phrase.text+"\n")
			
			if phrase.id in id_dict:
				# for mwe in id_dict[phrase.id]:
				tokens = (id_dict[phrase.id])[0].strip().split()
				print((id_dict[phrase.id])[0])
				print(tokens)
				for mot in phrase.tree:
					if mot.lemma == "à+le":
						mot.lemma = re.sub("\+le", '', mot.lemma)
					if tokens[0] == mot.lemma:
						mot.misc = "MWE"
						print_mot(mot)
					elif mot.lemma in tokens:
						i=0
						for token in tokens:
							if token == mot.lemma:
								mot.misc = "INMWE"
								print_mot(mot)
								i = i+1
							else:
								continue
					else:
						print_mot(mot)
			else:
				for mot in phrase.tree:
					print_mot(mot)
					
			out.write("\n")
	
	# print(corpus_modifie)

	# print(*map(' '.join, corpus[8].lem_2g), sep=', ')