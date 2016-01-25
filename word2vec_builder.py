# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 09:52:05 2016

@author: katerinailiakopoulou
"""


import logging
import string
import gensim
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
class Corpus_Sentence_Extractor(object):
    def __init__(self, dirname):
        self.dirname = dirname 
    def __iter__(self):
            for line in open(self.dirname):
                text = line.translate(string.maketrans("",""), string.punctuation)
                yield text.split()
    
def train(sents,model_name,c,w,s,wd):
    bigram_model = gensim.models.phrases.Phrases(sents)
    #trigram_model = gensim.models.phrases.Phrases(bigram_model[sents])

    try:
        model = gensim.models.Word2Vec(bigram_model[sents],min_count=c, workers=w, size=s, window=wd)
        model.save(model_name)
    except(TypeError):
        pass

if __name__ == "__main__":
    if len(sys.argv) < 7:
        sys.exit('Please provide [corpus directory] [word2vec model name] [min_count] [workers] [size] [window]: [--s --s --int --int --int --int]')
    
    sentences = Corpus_Sentence_Extractor(sys.argv[1])
    train(sentences,sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))



