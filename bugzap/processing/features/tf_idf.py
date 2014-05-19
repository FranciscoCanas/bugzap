import math
import nltk

__author__ = 'mailfrancisco@gmail.com'

class tf_idf():
    def __init__(self):
        self.idf_cache = {}

    def compute_tf_idf(self, candidates, document, documents):
        """
        For each token used in candidates list:
        Compute the final tf-idf score. The product of tf * idf.
        Returns a list of tuples: (word, tf-idf score)
        Sorted by tf-idf score.
        """
        tfs = self.compute_tf(candidates, document)
        idfs = self.compute_idf(candidates, documents)
        return sorted(map(lambda x,y: (x[0], x[1] * y[1]), tfs, idfs),key=lambda item:item[1],reverse=True)

    def compute_tf(self, candidates, document):
        """
        Compute the term frequency: How many times this word appears
        in this document.
        Returns a list of tuples: (word, tf score)
        """
        dist = nltk.FreqDist(document)
        score_tf = lambda w, doc: dist[w.lower()]/float(len(doc))
        return [(word, score_tf(word, document)) for word in sorted(candidates)]

    def compute_idf(self, candidates, documents):
        """
        Compute the inverse document frequency: A score of how uncommon a word
        is among all the documents.
        log(total_number_of_docs/1 + number_of_docs_tag_appears_in)
        Returns a list of tuples: (word, idf score)
        """
        idfs = []
        score_idf = lambda w, docs: sum([1 for d in docs if w.lower() in d])

        for word in set(sorted(candidates)):
            if not self.idf_cache.has_key(word):
                idf = math.log(len(documents) / 1.0 + score_idf(word, documents))
                self.idf_cache[word]=idf
            else:
                idf = self.idf_cache[word]
            idfs.append((word, idf))
        return idfs


