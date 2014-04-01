from operator import mul
import math

__author__ = 'fran'


def compute_tf_idf(bug, documents):
    """
    For each token used in this bug:
    Compute the final tf-idf score. The product of tf * idf.
    Returns a list of tuples: (word, tf-idf score)
    Sorted by tf-idf score.
    """
    tfs = compute_tf(bug, bug['document'])
    idfs = compute_idf(bug, documents)
    return sorted(map(lambda x,y: (x[0], x[1] * y[1]), tfs, idfs),key=lambda item:item[1],reverse=True)

def compute_tf(bug, document):
    """
    Compute the term frequency: How many times this word appears
    in this document.
    Returns a list of tuples: (word, tf score)
    """
    words, pos = zip(*bug['candidates'])
    return [(word, bug['freq_distribution'][word]/float(len(words))) for word in set(sorted(words))]

def compute_idf(bug, documents):
    """
    Compute the inverse document frequency: A score of how uncommon a word
    is among all the documents.
    log(total_number_of_docs/number_of_docs_tag_appears_in)
    Returns a list of tuples: (word, idf score)
    """
    idfs = []
    words, pos = zip(*bug['candidates'])
    for word in set(sorted(words)):
        idf = math.log(len(documents) / 1.0 + sum([1 for d in documents if word in d]))
        idfs.append((word, idf))
    return idfs


