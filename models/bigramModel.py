import random
from .nGramModel import *


class BigramModel(NGramModel):

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.
        """
        temp_list = []

        i = 0

        # Iterate through lines in text
        for L in text:
            temp_list.append(L)

            # Iterate through words in lines
            for count in range((len(L) - 1)):
                word1 = temp_list[i][count]
                word2 = temp_list[i][count + 1]

                # Update and Populate nGramCounts
                if ((word1 in self.nGramCounts) and (word2 in self.nGramCounts[word1])):
                    self.nGramCounts[word1][word2] += 1
                elif word1 in self.nGramCounts:
                    inner = 1
                    self.nGramCounts[word1][word2] = inner
                else:
                    newWord = {word2 : 1}
                    self.nGramCounts[word1] = newWord
            i = i + 1

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 1
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        last_word = sentence[len(sentence) - 1]

        # Check if last word begins a two-word sequence in nGramCounts
        for word in self.nGramCounts:
            if word == last_word:
                return True
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  BigramModel sees as candidates, see the spec.
        """

        lastWord = sentence[-1]
        return self.nGramCounts[lastWord]

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    bi = BigramModel()
    text = [ ['the', 'brown', 'fox'], ['the', 'brown', 'cat', 'brown', 'fox'] ]
    bi.trainModel(text)
    print(bi)
    text2 = [['the', 'brown', 'bear'], ['the', 'bear']]
    bi.trainModel(text2)
    print(bi)
    #dictionary = {'black': {'dog': '1', 'cat': '2'}, 'car':{ 'dog': {1}, deer: {2}}}
    #print dictionary[0]
    #should print {the: brown: 2}, {brown: fox: 2}, everything else :1

    sentence = ['if', 'i', 'go', 'you', 'dead']
    print(bi.trainingDataHasNGram(sentence))
    sentence = ['if', 'he', 'goes', 'into', 'the']
    print(bi.trainingDataHasNGram(sentence))

    print(bi.getCandidateDictionary(sentence))
