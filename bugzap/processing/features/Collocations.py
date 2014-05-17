import nltk
from nltk.collocations import *

__author__ = 'fcanas'

class Collocations():

    def __init__(self):
        pass

    def find_ngrams(self, n=2, body=None, top=10):
        """
        Input
        n:  n-grams!
        body: A list containing a sequence of words from a text.
        top: How many n-grams to return.

        Output:
        A list of the top 'top' n-grams in body.
        """
        measures = {
            2: nltk.collocations.BigramAssocMeasures,
            3: nltk.collocations.TrigramAssocMeasures
        }

        finder = {
            2: BigramCollocationFinder,
            3: TrigramCollocationFinder
        }


        if not body:
            return []

        m = measures[n]()
        result = finder[n].from_words(body)
        return result.nbest(m.pmi, top)
