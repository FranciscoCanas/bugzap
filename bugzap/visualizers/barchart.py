import json
from pprint import pprint
import numpy as np
from bokeh.plotting import *
from bokeh.objects import ColumnDataSource, Range1d

__author__ = 'fcanas'

if __name__=="__main__":
    file="eap62.processed.json"
    bugs = json.load(open(file))
    keywords_tuples = [bug['keywords'] for bug in bugs]
    keywords_with_scores = [word for sublist in keywords_tuples for word in sublist]
    keywords_no_scores = [word[0] for sublist in keywords_tuples for word in sublist]
    keywords_sum_of_scores = {}
    for word in keywords_with_scores:
        if keywords_sum_of_scores.has_key(word[0]):
            keywords_sum_of_scores[word[0]] += word[1]
        else:
            keywords_sum_of_scores[word[0]] = word[1]

    array = np.array([])
    pprint(sorted(keywords_with_scores,key=lambda x: x[1]))


