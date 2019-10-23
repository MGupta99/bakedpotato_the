import sys
sys.dont_write_bytecode = True # Suppress .pyc files

from .generate import *
from .tweet import *

import random

import csv

from .data.dataLoader import *
from .models.musicInfo import *
from .models.unigramModel import *
from .models.bigramModel import *
from .models.trigramModel import *

lyricDirs = ['headlines']

import spacy
nlp = spacy.load("en_core_web_sm")

def removeURL(tweet):
    for pos, word in enumerate(tweet.split()):
        if '.' in word and '/' in word:
            tweet = tweet.split()[:pos]
            break

    new_tweet = ''
    for word in tweet:
        new_tweet += word + ' '

    return new_tweet

def createImageDictionary(classes, annotations):

    image_dictionary = {}

    with open(classes, 'r') as class_descriptions:
        class_reader = csv.reader(class_descriptions, delimiter=',')

        for row in class_reader:
            image_dictionary[row[0]] = []

        with open(annotations, 'r') as image_annotations:
            annotation_reader = csv.reader(image_annotations, delimiter=',')

            for row in annotation_reader:
                image_dictionary[row[2]].append(row[0])

    return image_dictionary

def createClassDictionary(classes):

    class_dictionary = {}

    with open(classes, 'r') as class_descriptions:
        class_reader = csv.reader(class_descriptions, delimiter=',')

        for row in class_reader:
            class_dictionary[row[1].lower()] = row[0]

    return class_dictionary

def weightedChoice(candidates):
    """
    Requires: candidates is a dictionary; the keys of candidates are items
              you want to choose from and the values are integers
    Modifies: nothing
    Effects:  returns a candidate item (a key in the candidates dictionary)
              based on the algorithm described in the spec.
    """
    cumulative = []
    total = 0
    tokens = []

    # Creates list of tokens and list of cumulative totals
    for item in candidates:
        tokens.append(item)
        total += candidates[item]
        cumulative.append(total)

    num = random.randrange(0, total)


    # Randomly select token based on weights

    for i in range(len(cumulative)):
        if num < cumulative[i]:
            return tokens[i]

def createCandidateDictionary(tweet_text, classes, annotations):

    image_dictionary = createImageDictionary(classes, annotations)
    class_dictionary = createClassDictionary(classes)

    candidate_dictionary = {}

    for word in tweet_text:
        if word.lower() in class_dictionary:
            candidate_list = image_dictionary[class_dictionary[word.lower()]]

            for image in candidate_list:
                if image in candidate_dictionary:
                    candidate_dictionary[image] += 1
                else:
                    candidate_dictionary[image] = 1

    return candidate_dictionary

def pickImage(tweet_text, classes, annotations, images):

    candidate_dictionary = createCandidateDictionary(tweet_text, classes, annotations)
    if len(candidate_dictionary) > 0:
        image = weightedChoice(candidate_dictionary)
        with open(images, 'r') as image_URLs:
            image_reader = csv.reader(image_URLs, delimiter=',')

            for row in image_reader:
                if image == row[0]:
                    return row[2]
    else:
        return

def tweetTooLong(tweet_text):

    max_length = 280 + len('^::^') + len('^:::^')
    tweet_length = 0

    for word in tweet_text:
        tweet_length += len(word) + 1

    if tweet_length > 280:
        return True
    else:
        return False


def generateTweet():

    tweet_models = trainLyricModels(lyricDirs)

    tweet = Tweet()
    tweet.text = ['^::^', '^:::^']

    desiredLength = 12

    while not tweetTooLong(tweet.text):
        model = selectNGramModel(tweet_models, tweet.text)
        tweet.text.append(model.getNextToken(tweet.text))
        if tweet.text[-1] == '$:::$':
            tweet.text.remove('$:::$')
            tweet.text.remove('^::^')
            tweet.text.remove('^:::^')
            break

    else:
        if '$:::$' in tweet.text:
            tweet.text.remove('$:::$')
        tweet.text.remove('^::^')
        tweet.text.remove('^:::^')

    if tweetTooLong(tweet.text):
        tweet.text.pop()

    tweet.checkTweetEnd()
    tweet.image = pickImage(tweet.text, 'images/class-descriptions.csv', 'images/confident-annotations.csv', 'images/images.csv')

    print tweet.text
    for pos, word in enumerate(tweet.text):
        tweet.text[pos] = word.encode('ascii', 'ignore')

    return tweet

tweet = generateTweet()
print tweet.text, tweet.image
