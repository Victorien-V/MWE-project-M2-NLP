#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Word:
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
	sent_id = n° id de la phrase
	sent_text = texte de la phrase
	sent_tree = arbre de la phrase
	sent_len = longueur de la phrase (en nb de mots, d'après la taille de l'arbre)
	Cet arbre est composé de mots de la classe Word
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
				w.xpos="_"
				out.write(
					w.nid+"\t"+w.form+"\t"+w.lemma+"\t"+w.upos+"\t_\t"+w.feats+"\t"+w.head+"\t"+w.deprel+"\t"+w.deps+"\t"+w.misc+"\n"
				)
			out.write("\n")
			