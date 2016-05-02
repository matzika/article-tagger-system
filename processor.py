
####### Documents Processor #######
#Author: Katerina Iliakopoulou
#email: ai2315@columbia.edu


import sys
import os
import json
import re
import time
import datetime
import nltk
import inspect
  
from nltk.corpus import stopwords

#The Processor processes text by removing
#words that carry no or little contextual 
#information and keeping only those that can
#contribute to NLP. 
class Processor(object):

	def process(self,content):
		"""Process plain text and remove words that carry little or no information"""
		self.text = content
		self.words = []
		self.remove_what_is_not_a_word()
		self.keep_only_nouns()
		self.remove_stopwords()
		self.text = ' '.join(self.words)
		return self.text.strip()

	def annotate_entities(self,entities,text):
		"""Annotate name entities based on whether they represent a Person, a Location or an Organization."""
		for ent in entities:
			if len(ent) == 1:
				continue
			ent_pr = re.sub("_"," ",ent)
			if entities[ent] == 'PERSON':
				text = re.sub(ent_pr+" ",(ent+"/P "),text)
			elif entities[ent] == 'GPE' or entities[ent] == 'GSP':
				text = re.sub(ent_pr+" ",(ent+"/L "),text)
			elif entities[ent] == 'ORGANIZATION' or entities[ent] == 'FACILITY':
				text = re.sub(ent_pr+" ",(ent+"/O "),text)

		return text

	def remove_stopwords(self):
		#remove stopwords, honorifics and words that consist of only one letter
		self.words = [w for w in self.words if (not w in stopwords.words("english")) and (len(w) > 1) and w!="mr" and w!="mrs" and w!="prof" and w!="dr" and w!="ms"]

	def remove_what_is_not_a_word(self):
		"""Remove punctuation and numerical symbols"""
		self.text = re.sub("[^a-zA-Z]"," ",self.text).lower()

	def keep_only_nouns(self):
		"""Filter out every word that is not a noun or an adjective"""
		tagged = nltk.pos_tag(self.text.split())
		for t in tagged:
			if t[1] == 'NN' or t[1] == 'NNS' or t[1] == 'NNP' or t[1] == 'NNPS' or t[1] == 'JJ':
				self.words.append(t[0])

