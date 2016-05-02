"""
Created on Sat Jan  9 09:52:05 2016

@author: Katerina Iliakopoulou
@email: ai2315@columbia.edu
"""


import sys
import os
import json
import re
import nltk
import gensim
import en

from bs4 import BeautifulSoup  
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from time import time


"""
The Processor processes word2vec word vectors and 
builds a dictionary of similar words 
"""

class Processor(object):
    def __init__(self,model,outdir):
        self.model = gensim.models.Word2Vec.load(model)
        self.output = outdir

    def refine(self,t):
        threshold = float(t)
        corpus = self.model.index2word

        originals = detect_overlaps(corpus)
        similar_words = {}
        for word in corpus:
            syns = wn.synsets(word)
            if is_a_verb_or_adverb(syns):
                continue
            
            most_similar = self.model.most_similar([word], topn=300)
            similar_words[word] = []
            u_most_similar = remove_overlaps(most_similar,originals)
            for m in u_most_similar:
                try:
                    if u_most_similar[m] < threshold:
                        continue
                    t = (m,u_most_similar[m])
                    similar_words[word].append(t)
                except KeyError:
                    pass
        json.dump(similar_words, open(self.output,'w'))

def detect_overlaps(corpus):
    assignments = {}
    for w1 in corpus:
        if "_" in w1:
            parts = w1.split("_")
            for w2 in corpus:
                if (w1 != w2) and (w2 in parts):
                    if w2 in assignments:
                        words = assignments[w2]
                        words.add(w1)
                        assignments[w2] = words
                    else:
                        words = set()
                        words.add(w1)
                        assignments[w2] = words

    #remove duplicates with the same meaning (e.g.: north korea - north korean)
    clear_assignments = {}
    for a in assignments:
        duplicates = set()
        for w1 in assignments[a]:
            for w2 in assignments[a]:
                if w1 != w2:
                    if (w2 in w1) and len(w1) - len(w2) == 1:
                        #print(w1 + " is a duplicate to " + w2)
                        duplicates.add(w2)
        clear_assignments[a] = set()
        for w1 in assignments[a]:
            if not w1 in duplicates:
                clear_assignments[a].add(w1)
                        
    return clear_assignments

def remove_overlaps(similar,assignments):
    words = {}
    
    for sw in similar:
        if sw[0] in assignments:
            for a in assignments[sw[0]]:
                if a in words:
                    words[a] += sw[1]
                else:
                    words[a] = sw[1]
        else:
            words[sw[0]] = sw[1]

    return words



if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit('Please provide [word2vec model] [output file dir] [similarity threshold]: [--s --s --f]')
    starttime = time()
    model = sys.argv[1]
    outfile = sys.argv[2]
    threshold = sys.argv[3]
    Processor(model,outfile).refine(threshold)
    endtime = time()
    print("Processing similar words set lasted : " + str(endtime - starttime) + " seconds")
	

