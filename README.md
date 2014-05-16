bugzap
======


Bugzilla Analysis Program is an analysis tool that uses some basic Natural Language Processing to extract descriptive information from bug reports.


Scraping
---------------
Bugzap scrapes a given Bugzilla query url and saves all of the resulting bug
reports locally.


Preprocessing
---------------
Each of the reports is pre-processed to construct a body of documents composed
from the bugs' respective descriptions and comments.


Feature Extraction
------------
These documents are then passed through a series processing pipeline to extract
useful features: Currently using term Frequency, document Frequency, position in document body.


Statistics
------------------
Once each bug report has had its set of features extracted, we can compile and
gather statistics: top unigrams, bigrams, trigrams.


Visualization
-------------
Datasets can be visualized as histograms: Most frequently appearing n-grams.


