#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
module pour lire du conllu
read_file(path) permettra de lire un fichier conllu
	retour : une liste de Sent() ayant des attributs .tree
	ces derniers sont des listes de Word()
"""

import sys

class Word:
	"""
	définit un 'mot' dans un conllu
	les attributs sont ceux définis dans la doc UD (http://universaldependencies.org/format.html)
	"""
	def __init__(self, line):
		line=line.strip().split('\t') #découpage de la ligne (10 éléments au total)
		self.nid = line[0]
		self.form = line[1]
		self.lemma = line[2]
		self.upos = line[3]
		self.xpos = line[4]
		self.feats = line[5]
		self.head = line[6]
		self.deprel = line[7]
		self.deps = line[8]
		self.misc = line[9]
		
class Sent:
	"""
	définit une phrase dans un conllu
	id = n° id de la phrase
	text = texte de la phrase
	sentlen = longueur de la phrase (en nb de mots, d'après la taille de l'arbre)
	tree = arbre de la phrase
	N.B.: Cet arbre est une liste de mots de la classe Word
	"""
	def __init__(self, element):
		#element --> l'arbre d'une phrase+les métadonnées
		tree=[]
		lines=element.split('\n') #liste de lignes
		for line in lines:
			if line.startswith('#'):
				if 'sent_id' in line: #n°id de la phrase
					self.id=line.strip().split('= ')[1]
				else: #texte de la phrase
					self.text=line.strip().split('= ')[1]
					continue
			elif line: #pour éviter la ligne vide
				mot=Word(line)
				#if not mot.nid.isdigit():
					#continue
				tree.append(mot)
				
			self.tree=tree #arbre de la phrase
			self.sentlen=len(tree)

def read_file(path):
	"""
	lit le conllu et donne en sortie une liste d'objets Sent
	chaque objet Sent a : .id, .text, .tree
	les éléments de l'arbre d'un Sent sont des Word
	un Word : .nid, .form, .lemma, .upos, .xpos, .feats, .head, .deprel, .deps, .misc
	si le résultat est stocké dans une variable corpus on aura :
	texte de la 1ère phrase du corpus --> corpus[0].text
	lemme du 1er token de la 1ère phrase --> corpus[0].tree[0].lemma
	"""
	
	res=[]
	conllu=open(path).read().split("\n\n") #on récupère tout le fichier, découpé en arbres
	for element in conllu:
		if element : 
			phrase=Sent(element.rstrip())
			res.append(phrase)
	
	return res

def ecrit_nouveau(conllu,path):
	"""écrit le nouveau fichier .conll avec un '_' dans la colonne xpos """

	with open(path,'w',encoding="utf-8") as out:
		for s in conllu:
			out.write("# sent_id = "+s.id+"\n"+"# text = "+s.text+"\n")
			for w in s.tree:
				out.write(
					w.nid+"\t"+w.form+"\t"+w.lemma+"\t"+w.upos+"\t"+w.xpos+"\t"+w.feats+"\t"+w.head+"\t"+w.deprel+"\t"+w.deps+"\t"+w.misc+"\n"
				)
			out.write("\n")