import random
from .nGramModel import *

class UnigramModel(NGramModel):

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.
        """
        default_text = []

        i = 0

        # Iterate through lines in text
        for L1 in text:
            default_text.append(L1)

            # Iterate through words in lines
            for unigram in range(len(L1)):
                word1 = default_text[i][unigram]

                # Update and populate nGramCounts
                if word1 in self.nGramCounts:
                    self.nGramCounts[word1] += 1
                elif word1 != '^::^' and word1 != '^:::^':
                    self.nGramCounts[word1] = 1
            i = i + 1

        return self.nGramCounts


    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        # Check if nGramCounts is empty
        if self.nGramCounts != {}:
            return True
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts

###############################################################################
# Main
###############################################################################

# This is the code python runs when unigramModel.py is run as main
if __name__ == '__main__':

    # An example trainModel test case
    uni = UnigramModel()
    text = [ [ 'brown' ] ]
    uni.trainModel(text)
    # Should print: { 'brown' : 1 }
    print(uni)

    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    uni.trainModel(text)
    # Should print: { 'brown': 2, 'dog': 1, 'fox': 1, 'lazy': 1, 'the': 2 }
    print(uni)

    text = [ ['^::^', '^:::^', 'the', 'white', 'fox', 'jumped', '^$$^'], ['^::^', 'hi', '^$$^'] ]
    uni.trainModel(text)
    # Should print: { 'the', 'white', 'fox', 'jumped', 'hi': 1, '^$$^: 2}
    print(uni)

    # An example trainingDataHasNGram test case
    uni = UnigramModel()
    sentence = "Eagles fly in the sky"
    print(uni.trainingDataHasNGram(sentence)) # should be False
    uni.trainModel(text)
    print(uni.trainingDataHasNGram(sentence)) # should be True
