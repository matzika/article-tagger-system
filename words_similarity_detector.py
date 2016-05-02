# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:57:45 2016

@author: katerinailiakopoulou
"""

import gensim
import logging
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

"""
The Finder finds which words are similar to the one given
based on the word2vec word vectors. It also prints how similar two
words are depending on their word vectors comparison.
"""

class Finder(object):
    
    def __init__(self,model,output,topn):
        self.output_file = open(output,'w')
        self.m = gensim.models.Word2Vec.load(model)
        print(len(self.m.index2word))
        self.n = topn

    def get_most_similar(self,input):
        self.output_file.write('---Similar words to:' + input + '---\n')
        try:
            self.output_file.write(str(self.m.most_similar([input], topn=self.n)))
        except KeyError as e:
            self.output_file.write(str(e))  
        self.output_file.write('\n')
    
    def get_pos_negs_similar(self,input):
        self.output_file.write('--- Similar words to: ' + input + '---\n')
        pos_negs = input.split('NOT')
        pos = pos_negs[0]
        neg = pos_negs[1]
        poss = pos.split('AND')
        negs = neg.split(',')
        positives = []
        for p in poss:
            positives.append(p.strip())
        negatives = []
        for n in negs:
            negatives.append(n.strip())
        try:
            self.output_file.write(str(self.m.most_similar(positive=positives, negative=negatives, topn=self.n)))
        except KeyError as e:
            self.output_file.write(str(e))
        self.output_file.write('\n')
        
    def get_pos_similar(self,input):
        self.output_file.write('--- Similar words to: ' + input + '---\n')
        poss = input.split('AND')
        positives = []
        for p in poss:
            positives.append(p.strip())
        try:
            self.output_file.write(str(self.m.most_similar(positive=positives, topn=self.n)))
        except KeyError as e:
            self.output_file.write(str(e))
        self.output_file.write('\n')
        
    def get_similarity(self,input):
        self.output_file.write('--- Similarity between: ' + input + '---\n')
        parts = input.split('-')
        try:
            self.output_file.write(str(self.m.similarity(parts[0], parts[1])))
        except KeyError as e:
            self.output_file.write(str(e))
        self.output_file.write('\n')
        
    def process_input(self,input):
        f = open(input, 'r+')
        for line in f:
            word = line.replace("\n", "")
            if 'AND' and 'NOT' in line:
                self.get_pos_negs_similar(word)
            elif 'AND' in line:
                self.get_pos_similar(word)
            elif '-' in line:
                self.get_similarity(word)
            else:
                self.get_most_similar(word)
                

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit('Please provide [word2vec model] [input directory], [output directory] [similar word count]: [--s --s --s --int]')
    
    Finder(sys.argv[1],sys.argv[3],int(sys.argv[4])).process_input(sys.argv[2])
