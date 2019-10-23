import random
from .nGramModel import *

class TrigramModel(NGramModel):

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.
        """

        # Iterate through lines in text
        for L in text:

            # Iterate through words in lines
            for count2 in range((len(L) - 2)):
                word1 = L[count2]
                word2 = L[count2 + 1]
                word3 = L[count2 + 2]

                # Update and populate nGramCounts
                if ((word1 in self.nGramCounts) and (word2 in self.nGramCounts[word1]) and (word3 in self.nGramCounts[word1][word2])):
                    self.nGramCounts[word1][word2][word3] += 1
                elif ((word1 in self.nGramCounts) and (word2 in self.nGramCounts[word1])):
                    newWord = 1
                    self.nGramCounts[word1][word2][word3] = newWord
                elif word1 in self.nGramCounts:
                    newWord = {word3: 1}
                    self.nGramCounts[word1][word2] = newWord
                else:
                    newWord = {word2: {word3: 1}}
                    self.nGramCounts[word1] = newWord

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        last_word = sentence[len(sentence) - 1]
        second_last_word = sentence[len(sentence) - 2]

        # Check if last/second to last word are part of three-word sequence
        if second_last_word in self.nGramCounts:
            if last_word in self.nGramCounts[second_last_word]:
                return True

        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """

        last_word = sentence[-1]
        second_last_word = sentence[-2]

        return self.nGramCounts[second_last_word][last_word]

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    text = [['if', 'we', 'i', 'go', 'you', 'dead'], ['if', 'i','go', 'now']]
    tri = TrigramModel()
    tri.trainModel(text)
    print(tri)

    sentence = ['if' , 'i', 'go', 'i', 'go']
    print(tri.trainingDataHasNGram(sentence))
    sentence = ['this', 'should', 'be', 'false']
    print(tri.trainingDataHasNGram(sentence))

    sentence = ['if', 'you', 'live', 'i', 'go']
    print(tri.getCandidateDictionary(sentence))
