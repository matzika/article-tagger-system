"""
Created on Sat Jan  9 09:52:05 2016

@author: Katerina Iliakopoulou
@email: ai2315@columbia.edu
"""

import sys
import os
import json
import time
import nltk
import operator
import re

from time import time
from parser import Parser


"""
The Comparator processes the input text 
and tries to find article's subject and
infer relevant concepts and entities through
the similar words dictionary that is derived 
from the word2vec model.
"""
class Comparator(object):
	def __init__(self,simdir):
		self.parser = Parser(None)
		#read similar words dictionary
		self.similar_words = json.load(open(simdir))

	def find_similarities(self):
		self.detect_tags()
		i_words = self.input.split(" ")
		similarities = {}

		for iw in i_words:
			if iw in self.similar_words:
				for s in self.similar_words[iw]:
					if not s[0] in similarities:
						similarities[s[0]] = s[1]
					else:
						similarities[s[0]] += s[1]


		sorted_similarities = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)

		return sorted_similarities

	def detect_tags(self, input_text):
		tags = {}

		people = {}
		locations = {}
		organizations = {}
		concepts = {}

		print("Parse Article")
		self.input = self.parser.parse_plain_text(input_text)
		print("Find Entities in the Article")
		self.entities = self.parser.extract_entities(input_text)
		print "Entities: \n" + str(self.entities)
		for ent in self.entities:
			if self.entities[ent] == 'PERSON':
				entity = ent
				people[entity] = 10
			elif self.entities[ent] == 'GPE' or self.entities[ent] == 'GSP':
				entity = ent
				locations[entity] = 10
			elif self.entities[ent] == 'FACILITY' or self.entities[ent] == 'ORGANIZATION':
				entity = ent
				organizations[entity] = 10

		print("Find Frequent Words")
		words = self.calc_freq_words(self.input)
		print("Find Important Words")
		important_words = self.find_important_words(input_text)
		for word in words:
			if word[1] == 1:
				break #too infrequent to care

			score = word[1]; #count frequency
			if word[0] in important_words:
				score *= 2 #double if in the nutgraph of the article
			if word[0] in self.similar_words:
				
				for s in self.similar_words[word[0]]:
					
					if 'P' in s[0]:
						if 'O' in s[0]:
							s[0] = re.sub("/O","",s[0])
						if 'L' in s[0]:
							s[0] = re.sub("/L","",s[0])
						stripped = re.sub("/P","",s[0])
						
						if stripped in people:
							people[stripped] += s[1] + score
							
						else:
							people[stripped] = score
					elif 'L' in s[0]:
						if 'O' in s[0]:
							s[0] = re.sub("/O","",s[0])
						stripped = re.sub("/L","",s[0])
						
						if stripped in locations:
							locations[stripped] += s[1] + score
							
						else:
							locations[stripped] = score
					elif 'O' in s[0]:
						stripped = re.sub("/O","",s[0])
						
						if stripped in organizations:
							organizations[stripped] += s[1] + score
							
						else:
							organizations[stripped] = score
					else:
						if s[0] in concepts:
							concepts[s[0]] += s[1] + score
						else:
							concepts[s[0]] = score

		print("Sort Entities and Concepts")
		sorted_people = sorted(people.items(), key=operator.itemgetter(1), reverse=True)
		sorted_orgs = sorted(organizations.items(), key=operator.itemgetter(1), reverse=True)
		sorted_locations = sorted(locations.items(), key=operator.itemgetter(1), reverse=True)
		sorted_concepts = sorted(concepts.items(), key=operator.itemgetter(1), reverse=True)

		tags['people'] = []
		for sp in sorted_people:
			tags['people'].append(sp[0])

		tags['locations'] = []
		for sp in sorted_locations:
			tags['locations'].append(sp[0])

		tags['organizations'] = []
		for sp in sorted_orgs:
			tags['organizations'].append(sp[0])

		tags['concepts'] = []
		for sp in sorted_concepts:
			tags['concepts'].append(sp[0])
			if len(tags['concepts']) > 500:
				break
		
		return tags

	def calc_freq_words(self, input_text):
		vocab = {}
		for word in input_text.split(" "):
			if word in vocab:
				vocab[word] += 1
			else:
				vocab[word] = 1

		sorted_freq_words = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)

		return sorted_freq_words

	def find_important_words(self,input_text):
		"""Detect entities that appear in the article's nutgraph"""
		words = input_text.split()
		limit = int(len(words)/4)
		
		nutgraph = self.parser.parse_plain_text(' '.join(words[0:limit]))
		nutgraph_entities = self.parser.extract_entities(' '.join(words[0:limit]))

		important = []

		for w in nutgraph.split(" "):
			if w in nutgraph_entities:
				if nutgraph_entities[w] == 'PERSON':
					w = w + "P";
				elif nutgraph_entities[w] == 'GPE' or nutgraph_entities[w] == 'GSP':
					w = w + "L";
				elif nutgraph_entities[w] == 'FACILITY' or nutgraph_entities[w] == 'ORGANIZATION':
					w = w + "O";
			
			important.append(w)
			
		return important


if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.exit('Please provide [input data file dir] [similar words dir]: [--s --s ]')

	indir = sys.argv[1]
	simdir = sys.argv[2]
	f = open(indir, 'r')
	input_text = f.read()
	starttime = time()
	comparator = Comparator(simdir)
	tags = comparator.detect_tags(input_text)
	print tags
	endtime = time()
	print("Processing input lasted : " + str(endtime - starttime) + " seconds")
