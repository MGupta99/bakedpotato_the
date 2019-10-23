import random
import sys
import json
from .musicInfo import *

class NGramModel(object):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.
                  This function is done for you.
        """
        printed_string = self.__class__.__name__ + ':\n'

        try:
            printed_string = printed_string + json.dumps(
                self.nGramCounts,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        except:
            printed_string = printed_string + json.dumps(
                repr(self.nGramCounts),
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )


        return printed_string

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """
        pass

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this n-gram model
                  can be used to choose the next token for the current
                  sentence. This function does not need to be modified because
                  you will override it in NGramModel child classes according
                  to the spec.
        """
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. This function does not need to be
                  modified because you will override it in the NGramModel child
                  classes according to the spec.
        """
        pass

    def weightedChoice(self, candidates):
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


    def getNextToken(self, sentence):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.
        """

        return self.weightedChoice(self.getCandidateDictionary(sentence))

    def getNextNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from getNextToken, see the spec.
        """

        # Get candidates from sentence
        allCandidates = self.getCandidateDictionary(musicalSentence)
        constrainedCandidates = {}

        key = ''

        # Find constrained candidates
        for note in allCandidates:
            if note[0][0:-1] in possiblePitches or note == '$:::$':
                constrainedCandidates[note] = allCandidates[note]

        if len(constrainedCandidates) > 0:
            return self.weightedChoice(constrainedCandidates)
        else:
            return (random.choice(possiblePitches) + '4', random.choice(NOTE_DURATIONS))


###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # testing weightedChoice
    test = NGramModel()

    candidates1 = {'north': 4, 'east': 3, 'south': 2, 'west': 1}

    north = 0
    east = 0
    south = 0
    west = 0

    for trial in range(10000):
        choice = test.weightedChoice(candidates1)
        if choice == 'north':
            north += 1
        elif choice == 'east':
            east += 1
        elif choice == 'south':
            south += 1
        elif choice == 'west':
            west += 1
        else:
            print("ERROR")

    print("North: ", north)
    print("East: ", east)
    print("South: ", south)
    print("West: ", west)
    print("\n")

    candidates2 = {'north': 2, 'east': 2, 'south': 2, 'west': 2}

    north = 0
    east = 0
    south = 0
    west = 0

    for trial in range(8000):
        choice = test.weightedChoice(candidates2)
        if choice == 'north':
            north += 1
        elif choice == 'east':
            east += 1
        elif choice == 'south':
            south += 1
        elif choice == 'west':
            west += 1
        else:
            print("ERROR")

    print ("North: ", north)
    print ("East: ", east)
    print ("South: ", south)
    print ("West: ", west)
    print ("\n")

    candidates3 = {'north': 3, 'east': 3, 'south': 2, 'west': 0}

    north = 0
    east = 0
    south = 0
    west = 0

    for trial in range(8000):
        choice = test.weightedChoice(candidates3)
        if choice == 'north':
            north += 1
        elif choice == 'east':
            east += 1
        elif choice == 'south':
            south += 1
        elif choice == 'west':
            west += 1
        else:
            print("ERROR")

    print ("North: ", north)
    print ("East: ", east)
    print ("South: ", south)
    print ("West: ", west)
    print ("\n")

    candidates4 = {'north': 10, 'east': 0, 'south': 0, 'west': 0}

    north = 0
    east = 0
    south = 0
    west = 0

    for trial in range(10000):
        choice = test.weightedChoice(candidates4)
        if choice == 'north':
            north += 1
        elif choice == 'east':
            east += 1
        elif choice == 'south':
            south += 1
        elif choice == 'west':
            west += 1
        else:
            print("ERROR")

    print ("North: ", north)
    print ("East: ", east)
    print ("South: ", south)
    print ("West: ", west)
    print ("\n")


    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    nGramModel = NGramModel()
    print(nGramModel)
