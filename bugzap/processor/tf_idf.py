__author__ = 'fran'


def compute_tf_idf(tag, document, documents):
    """
    Compute the final tf-idf score: The product of tf * idf.
    """
    return compute_tf(tag, document) * compute_idf(tag, documents)

def compute_tf(tag, document):
    """
    Compute the term frequency: How many times this word appears
    in this document.
    """
    pass

def compute_idf(tag, documents):
    """
    Compute the inverse document frequency: A score of how uncommon a word
    is among all the documents.
    log(docs_with_word/total_number_of_docs)
    """
    pass

