import sys

import spacy
nlp = spacy.load("en_core_web_sm")

from generate import *

import random

import csv

from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import *

class Tweet:

    def __init__(self):
        self.text = []
        self.image = ''

    def checkTweetEnd(self):
        tweet = " ".join(self.text)

        doc = nlp(tweet)

        POS = []
        for token in doc:
            POS.append((token.text, token.pos_.encode))

        i = -1
        while POS[i][1] in ['CCONJ', 'SCONJ', 'DET']:
            self.text.pop()
            print(i)
            i -= 1
