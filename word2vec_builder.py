# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 09:52:05 2016

@author: katerinailiakopoulou
"""


import logging
import string
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases
import sys
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


"""
The builder trains the word2vec model
"""
class Builder(object):

    def __init__(self,corpus_dir,models_dir,modelname):
        self.corpus = corpus_dir 
        self.models = models_dir
        self.word2vec = modelname

        print self.corpus, self.models, self.word2vec

    def build(self,count,wrkers,sze,wndow):
        """Trains the bigram and trigram models with the sentences extracted from the given corpus"""
        sentences = Corpus_Sentence_Extractor(self.corpus)
        bigram = self.build_bigram_model(sentences,count)
        trigram = self.build_trigram_model(sentences,bigram)

        self.train(sentences,trigram,self.word2vec,count,wrkers,sze,wndow)

    def build_bigram_model(self,sentences,count):
        print "In Bigram Model"
        bigram = Phrases(sentences,min_count=count)
        dest = self.models + 'bigram_model'
        bigram.save(dest)
        return bigram
    
    def build_trigram_model(self,sentences,bigram):
        print "In Trigram Model"
        trigram = Phrases(bigram[sentences])
        dest = self.models + 'trigram_model'
        trigram.save(dest)
        
        return trigram

    def update(self,new_corpus,count,wrkers,sze,wndow):
        sentences = Corpus_Sentence_Extractor(new_corpus)

        bigram = Phrases().load(self.models + 'bigram_model')
        trigram = Phrases().load(self.models + 'trigram_model')

        bigram.add_vocab(sentences)
        trigram.add_vocab(bigram[sentences])

        self.train(sentences,trigram,self.word2vec,count,wrkers,sze,wndow)

    def train(self,sentence_stream,model,modelname,c,w,s,wd):
        print "Training..."
        try:
            mdl = Word2Vec(model[sentence_stream],min_count=c, workers=w, size=s, window=wd)
            #model.build_vocab(sentences)
            #mdl.train()
            print "Save model " + modelname
            mdl.save(modelname)
        except Exception as e:
            print e
            pass

 
class Corpus_Sentence_Extractor(object):
    def __init__(self, dirname):
        self.dirname = dirname 
    def __iter__(self):
            for line in open(self.dirname):
                text = re.sub("^\\_[^a-zA-Z]"," ",line)
                #text = line.translate(string.maketrans("",""), string.punctuation)
                yield text.split()
    


if __name__ == "__main__":
    #example values for [min_count] [workers] [size] [window]: 100 4 200 20 
    if len(sys.argv) < 8:
        sys.exit('Please provide [corpus directory] [models directory] [word2vec model name] [min_count] [workers] [size] [window]: [--s --s --int --int --int --int]')
    
    builder = Builder(sys.argv[1],sys.argv[2],sys.argv[3])
    builder.build(int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]))



