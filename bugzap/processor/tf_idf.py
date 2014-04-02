import math
import nltk

__author__ = 'mailfrancisco@gmail.com'

def compute_tf_idf(candidates, document, documents):
    """
    For each token used in this bug:
    Compute the final tf-idf score. The product of tf * idf.
    Returns a list of tuples: (word, tf-idf score)
    Sorted by tf-idf score.
    """
    tfs = compute_tf(candidates, document)
    idfs = compute_idf(candidates, documents)
    return sorted(map(lambda x,y: (x[0], x[1] * y[1]), tfs, idfs),key=lambda item:item[1],reverse=True)

def compute_tf(candidates, document):
    """
    Compute the term frequency: How many times this word appears
    in this document.
    Returns a list of tuples: (word, tf score)
    """
    dist = nltk.FreqDist(document)
    return [(word, dist[word.lower()]/float(len(document))) for word in sorted(candidates)]

def compute_idf(candidates, documents):
    """
    Compute the inverse document frequency: A score of how uncommon a word
    is among all the documents.
    log(total_number_of_docs/number_of_docs_tag_appears_in)
    Returns a list of tuples: (word, idf score)
    """
    idfs = []
    for word in set(sorted(candidates)):
        idf = math.log(len(documents) / 1.0 + sum([1 for d in documents if word.lower() in d]))
        idfs.append((word, idf))
    return idfs


