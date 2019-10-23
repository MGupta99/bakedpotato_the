#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import urllib.request
import random
import codecs
import unicodedata
import tinify

import tweepy

from tweet import *

import csv

from pysynth import pysynth
from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import *

# FIXME Add your team name

con_key = 'D3B8vkfi2H3Wrqd2CXdZ7C3bE'
con_sec = 'UPOdLz2fzfPpkGQHxD3LqoQmXeuuJVjCCMeWSVQoYFLtiypeaB'
acc_tok = '983521193797013507-kNcs4WhO3ZyIZHBl9uii18iTpdmrvZn'
acc_sec = 'a55tXEHYc1hzSXPgE2kDzeQskDX4IkXL5IqyeImPsBUhg'

authorization = tweepy.OAuthHandler(con_key, con_sec)
authorization.set_access_token(acc_tok, acc_sec)

api = tweepy.API(authorization)

tinify.key = "g7T0cBv3gxGLjvfWrBGYpx8TJFW4cTxC"

TEAM = 'Baked Potato'
LYRICSDIRS = ['headlines']
TESTLYRICSDIRS = ['the_beatles_test']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

import spacy
nlp = spacy.load("en_core_web_sm")

###############################################################################
# Helper Functions
###############################################################################

def output_models(val, output_fn = None):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  outputs the dictionary val to the given filename. Used
              in Test mode. This function has been done for you.
    """
    from pprint import pprint
    if output_fn == None:
        print("No Filename Given")
        return
    with open('TEST_OUTPUT/' + output_fn, 'wt') as out:
        pprint(val, stream=out)

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]
    print("RANDOMLY GENERATED SONG by " + TEAM)
    print("*" * 40)
    print
    for verse in verses:
        for line in verse:
            print (' '.join(line)).capitalize()
        print

def trainLyricModels(lyricDirs, test=False):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        for model in models:
            model.trainModel(lyrics)
    return models

###############################################################################
# Core
###############################################################################

def trainMusicModels(musicDirs):
    """
    Requires: lyricDirs is a list of directories in data/midi/
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]

    # call dataLoader.loadMusic for each directory in musicDirs
    for mdir in musicDirs:
        music = loadMusic(mdir)

        # Train each model
        for model in models:
            model.trainModel(music)

    return models


def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  returns the best possible model that can be used for the
              current sentence based on the n-grams that the models know.
              (Remember that you wrote a function that checks if a model can
              be used to pick a word for a sentence!)
    """
    # Return first model that works
    for model in models:
        if model.trainingDataHasNGram(sentence):
            return model

def generateLyricalSentence(models, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']

    # Add words to sentence until too long or ending character
    while not sentenceTooLong(desiredLength, len(sentence) - 2):
        model = selectNGramModel(models, sentence)
        sentence.append(model.getNextToken(sentence))
        if sentence[-1] == '$:::$':
            sentence.remove('$:::$')
            sentence.remove('^::^')
            sentence.remove('^:::^')
            break

    else:
        if '$:::$' in sentence:
            sentence.remove('$:::$')
            sentence.remove('^::^')
            sentence.remove('^:::^')

    return sentence

def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateLyricalSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """
    sentence = ['^::^', '^:::^']

    # Add notes to line until too long or ending character
    while not sentenceTooLong(desiredLength, len(sentence) - 2):
        model = selectNGramModel(models, sentence)
        sentence.append(model.getNextNote(sentence, possiblePitches))
        if sentence[-1] == '$:::$':
            sentence.remove('$:::$')
            sentence.remove('^::^')
            sentence.remove('^:::^')
            break
    else:
        if '$:::$' in sentence:
            sentence.remove('$:::$')
        sentence.remove('^::^')
        sentence.remove('^:::^')

    return sentence

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []

    song = [verseOne, verseTwo, chorus]

    desiredLength = 7

    # Generate lyrics for each section
    for section in song:
        for line in range(4):
            section.append(generateLyricalSentence(models, desiredLength))

    printSongLyrics(song[0], song[1], song[2])
    return

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """
    possiblePitches = KEY_SIGNATURES[random.choice(KEY_SIGNATURES.keys())]

    desiredLength = 96
    song = generateMusicalSentence(models, desiredLength, possiblePitches)

    pysynth.make_wav(song, fn=songName)

    return

###############################################################################
# Reach
###############################################################################

# Runs through array of tweets and removes URLs from them
def removeURL(tweet):
    for pos, word in enumerate(tweet.split()):
        if '.' in word and '/' in word:
            tweet = tweet.split()[:pos]
            break

    new_tweet = ''
    for word in tweet:
        new_tweet += word + ' '

    return new_tweet

'''The following five functions use a database of pictures with object
annotations to select an appropriate image for each Baked Potato tweet.
They check which images have annotations that contain words from the tweet,
and then pick the image with the most number of instances'''

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

# Checks to make sure tweet is <= 280 characters
def tweetTooLong(tweet_text):

    max_length = 280 + len('^::^') + len('^:::^')
    tweet_length = 0

    for word in tweet_text:
        tweet_length += len(word) + 1

    if tweet_length > 280:
        return True
    else:
        return False

# Checks to make sure tweet is not already an existing tweet from The Onion
def tweetExists(tweet):
    with open('data/lyrics/headlines/tweets.txt') as Onion_tweets:
        existing_tweets = Onion_tweets.readlines()

        for line in existing_tweets:

            word_list = line.strip().split()
            tweet_list = tweet[:]

            for i in range(len(word_list)):
                word_list[i] = word_list[i].lower()
            for j in range(len(tweet_list)):
                tweet_list[j].lower()

            if word_list == tweet_list:
                return True

        return False


def generateTweet(tweet_models):

    while True:
        try:
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

            for pos, word in enumerate(tweet.text):
                tweet.text[pos] = word.encode('ascii', 'ignore')

            return tweet

        except UnicodeDecodeError:
            pass

def tweet(tweet_models):
    new_tweet = generateTweet(tweet_models)

    while tweetExists(new_tweet.text):
        new_tweet = generateTweet(tweet_models)

    new_status = ' '.join([str(word, 'utf-8').capitalize() for word in new_tweet.text])
    new_status += ' '

    if new_tweet.image != None:
        try:
            image = urllib.request.urlretrieve(new_tweet.image, 'image.jpg')
            tinify.from_file('image.jpg').to_file('image_opt.jpg')
            upload = api.media_upload(filename='image_opt.jpg')
            media_ids = [upload.media_id_string]
            api.update_status(media_ids=media_ids, status=new_status)
        except:
            new_status += new_tweet.image
            api.update_status(status=new_status)
    else:
        api.update_status(status = new_status)

    return new_status

###############################################################################
# Main
###############################################################################

PROMPT = """
(1) Tweet Using The Baked Potato
(2) Quit the Twitterbot
> """

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """

    lyricsTrained = False
    musicTrained = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "--test":
            print("TEST MODE")
            testLyricsModels = trainLyricModels(TESTLYRICSDIRS)
            trigram = testLyricsModels[0].nGramCounts
            bigram = testLyricsModels[1].nGramCounts
            unigram = testLyricsModels[2].nGramCounts
            output_models(unigram, output_fn = "unigram_student.txt")
            output_models(bigram, output_fn = "bigram_student.txt")
            output_models(trigram, output_fn = "trigram_student.txt")
            print('Student models have been written to the TEST_OUTPUT folder')
            sys.exit()


    print('Welcome to the ' + TEAM + ' Twitterbot!')
    while True:
        try:
            userInput = int(input(PROMPT))
            if userInput == 1:
                if not lyricsTrained:
                    print('Starting Twitterbot and loading data...')
                    tweet_models = trainLyricModels(LYRICSDIRS)
                    print('Data successfully loaded')
                    lyricsTrained = True

                print('Tweeted', tweet(tweet_models))
                #print("Under construction")
            elif userInput == 2:
                print('Thank you for using the ' + TEAM + ' Twitterbot!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")

# This is how python tells if the file is being run as main
if __name__ == '__main__':
    main()

    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
