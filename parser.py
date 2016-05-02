
####### Documents Parser #######
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

from bs4 import BeautifulSoup  
from time import time as tm
from processor import Processor


# The Parser parses html documents 
# and extracts the article's body. 
class Parser(object):
	def __init__(self,output):
		self.p = Processor()
		if output != None:
			self.outfile = open(output,'w')
	   
	def parse_HTML(self,indir):
		"""Parses the HTML code of a document and writes the body in a txt file."""
		self.input = indir
		
		for fname in os.listdir(self.input):
			if fname == '.DS_Store':
				continue
			with open((self.input + fname), 'r') as inputfile:
				print("Parsing: " + (self.input + fname))
				content = inputfile.read()
				soup = BeautifulSoup(content,"html.parser")
				#class name is defined by the location of the html data 
				story_body_parts = soup.findAll("p", { "class" : "story-body-text" })
				for b in story_body_parts:
					text = b.get_text().encode('utf8')
					entities = self.extract_entities(text)
					text = self.p.process(text)
					text = self.p.annotate_entities(entities,text)
					self.outfile.write(text.rstrip() + "\n")

	def parse_HTML_fix(self,indir,parsed_file):
		self.input = indir
		f = open(parsed_file, 'r')
		input_text = f.read()
		total_entities = {}
		for fname in os.listdir(self.input):
			if fname == '.DS_Store':
				continue
			with open((self.input + fname), 'r') as inputfile:
				print("Parsing: " + (self.input + fname))
				content = inputfile.read()
				soup = BeautifulSoup(content,"html.parser")
				#class name is determined by where the content data to retrieve exist in the html doc
				story_body_parts = soup.findAll("p", { "class" : "story-body-text" })
				for b in story_body_parts:
					text = b.get_text().encode('utf8')
					entities = self.extract_entities(text)
					for ent in entities:
						if not ent in total_entities:
							total_entities[ent] = entities[ent]
		
		input_text = self.p.annotate_entities(total_entities,input_text)
		self.outfile.write(input_text)

	def parse_recursive(self,indir,it):
		"""Parses HTML documents in different directories in a recursive manner."""
		if it == 1:
			self.parse_HTML(indir + "/")
		else:
			for fname in os.listdir(indir):
				if fname == '.DS_Store':
					continue

				self.parse_recursive((indir + fname),(it-1))

	def extract_entities(self,text):
		"""Detects name entities (Person, Location, Organization) in text using the nltk library"""
		#text = text.decode("utf8")

		#remove honorifics in case they exist in the text
		text = re.sub("Mr.","",text)
		text = re.sub("Mrs.","",text)
		text = re.sub("Dr.","",text)

		entities = {}
		for sent in nltk.sent_tokenize(text):
			for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
				if chunk.__class__.__name__ == "Tree":
					ent = ""
					for child in chunk.leaves():
						ent += child[0] + "_"
					ent = ent[:-1].lower()
					if not ent in entities:
						entities[ent] = chunk.label()

		return entities


if __name__ == "__main__":
	if len(sys.argv) < 4:
		sys.exit('Please provide [input data file dir] [parsed data file dir and name] [dir levels (default = 1)]: [--s --s --i]')

	indir = sys.argv[1]
	outdir = sys.argv[2]
	n = int(sys.argv[3])

	starttime = tm()
	Parser(outdir).parse_recursive(indir,n)
	endtime = tm()
	timestamp = datetime.datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S')

	print("[" + str(timestamp) + "]Parsed articles in " + str(endtime - starttime) + " seconds")
	

