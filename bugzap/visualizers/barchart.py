import json
from pprint import pprint
import numpy as np
from matplotlib.axes import Subplot
from bokeh.plotting import *
from bokeh.objects import ColumnDataSource, Range1d

__author__ = 'fcanas'

if __name__ == "__main__":
    file = "eap62.processed.json"
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

    sorted_keywords_sum_of_scores = sorted(keywords_sum_of_scores.items(), key=lambda x: x[1], reverse=True)
    words = np.array([word_score[0] for word_score in sorted_keywords_sum_of_scores])
    score = np.array([word_score[1] for word_score in sorted_keywords_sum_of_scores], dtype=np.float)
    #pprint(sorted_keywords_sum_of_scores)
    output_file('keywords.html')
    hold()
    rect(x=words, y=score, width=0.8, height=score, x_range=words, color="#CD7F32", alpha=0.6,
         background_fill='#59636C', title="Olympic Medals by Country (stacked)", tools="",
         y_range=Range1d(start=0, end=max(score)), plot_width=800)

    show()



