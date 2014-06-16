import os
import json
import nltk
from keyextractor.src.features.Collocations import Collocations
from keyextractor.src.features.Positioning import Positioning
from keyextractor.src.features.tf_idf import tf_idf
from keyextractor.src.preprocessors.preprocessing import pre_process_pipeline


class BugProcessor():
    """
    """
    bugs = []
    documents = []
    pos_list = ['NN','NNP']
    words_black_list = ['installer', 'installation', 'jboss', 'eap', 'install', 'problem', 'description', 'reproduce',
                        'user','number', 'new', 'bz', 'ER', 'actual', 'results', 'expected', 'reproducible' 'target', 'release',
                        'milestone', 'run', 'default', 'er','er1', 'er2','er3', 'er4', 'er5', 'er6', 'see', 'severity',
                        'priority', 'error', 'fix', 'actual']

    def __init__(self, data_file):
        """
        """
        with open(data_file) as j:
            self.jdata = json.load(j)
            self.construct_bugs()

    def construct_bugs(self):
        """
        """
        print "Constructing from data..."
        for bug in self.jdata:
            pbug = {'id': str(bug['id']), 'description': bug['description'], 'url': bug['url'], 'candidates': []}
            print str(bug['id']),
            self.process_comments(pbug, bug['comments'])
            print '.',
            self.process_description(pbug, bug['description'])
            print '.',
            self.bugs.append(pbug)
            print '.'
        self.documents = self.construct_documents_list()


    def process_description(self, pbug, desc):
        """
        """
        tags = pre_process_pipeline(desc, black_list=self.words_black_list, pos_list=self.pos_list, lemmatize=False)
        candidates = set(pbug['candidates'])
        if tags:
             candidates |= set(zip(*tags)[0])
        pbug['candidates'] = list(candidates)

    def process_comments(self, pbug, comments):
        """
        """
        pcomments = []
        candidates = set(pbug['candidates'])
        for comment in comments:
            pcomment = {}
            try:
                comment_tags = pre_process_pipeline(comment['body'],
                                                           black_list=self.words_black_list,
                                                           pos_list=self.pos_list,
                                                           lemmatize=False)
                pcomment['comment'] = comment['body']
                pcomment['tokenized_comment'] = comment_tags
                if comment_tags:
                    candidates |= set(zip(*comment_tags)[0])
            except KeyError:
                pcomment['comment'] = ""
                pcomment['tokenized_comment'] = ""
            pcomments.append(pcomment)
        pbug['comments'] = pcomments
        pbug['candidates'] = list(candidates)

    def construct_documents_list(self):
        """
        Generates a list of all the 'documents': that is, a list of bodies of text created by
        putting together every comment for each bug.
        Returns a list of lists of tokens.
        """
        documents = []
        print "Constructing documents",
        for bug in self.bugs:
            print ".",
            bug['document'], bug['processed_document'] = self.construct_document_from_bug(bug)
            bug['freq_distribution'] = nltk.FreqDist(bug['document'])
            documents.append(bug['document'])
        print "."
        return documents

    def construct_document_from_bug(self, bug):
        """
        Generates a single document from the description and all of the comments in a bug.
        Returns this doc as a list of tokens.
        """
        document = map(unicode.lower, nltk.word_tokenize(bug['description']))
        processed_document = pre_process_pipeline(bug['description'])
        for comment in bug['comments']:
            if comment.has_key('comment'):
                document += map(unicode.lower, nltk.word_tokenize(comment['comment']))
                processed_document += pre_process_pipeline(comment['comment'], lemmatize=False,
                                                           black_list=self.words_black_list)
        return document, processed_document

def process(bug_file, path):
    """

    """
    processor = BugProcessor(bug_file)
    documents = processor.documents
    tfidf = tf_idf()
    collocations = Collocations()
    positioning = Positioning()

    make_path(path)
    extract_statistics(path, processor, tfidf, collocations, positioning, documents)
    store_statistic(path, processor.bugs, 'keywords', lambda x: x[0], nltk.FreqDist)
    store_statistic(path, processor.bugs, 'bigrams', lambda x: ' '.join(map(lambda y: y[0], x)), nltk.FreqDist)
    store_statistic(path, processor.bugs, 'trigrams', lambda x: ' '.join(map(lambda y: y[0], x)), nltk.FreqDist)
    store_collections(path, processor.bugs)

def make_path(path):
    """
    Ensures the target path for stat reports is created.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

def extract_statistics(path, processor, tfidf, collocator, positioning, documents):
    """
    Gather the statistics from a given set of processed bugs and documents.
    """
    print "Extracting statistics",
    for bug in processor.bugs:
        process_bug(bug, tfidf, collocator, positioning, documents)


def process_bug(bug, tfidf, collocator, positioning, documents):
    """
    Computes statistics for a given bug based on the documents set.
    """
    print str(bug['id']),
    bug['tfidf'] = tfidf.compute_tf_idf(bug['candidates'], bug['document'], documents)
    print ".",
    bug['positioning'] = positioning.compute_position_score(bug['candidates'], bug['document'])
    print ".",
    bug['keywords'] = extract_keywords(bug['tfidf'], bug['positioning'], lower_cutoff=0.001)
    print ".",
    bug['bigrams'] = collocator.find_ngrams(2, bug['processed_document'], 10)
    print ".",
    bug['trigrams'] = collocator.find_ngrams(3, bug['processed_document'], 10)
    print "."

def extract_keywords(tf_idf_scores, positioning_scores, lower_cutoff=0.0001):
    """
    Input: sorted list of tf-idf candidate scores
           hash of position scores.

    output: list of (candidate, score=tf-idf * positioning)
    """
    keywords = []
    for candidate in tf_idf_scores:
        if candidate[1] > lower_cutoff:
            score = candidate[1] * 2 * positioning_scores[candidate[0]]
            keywords.append((candidate[0], score))
    return keywords

def store_statistic(path, bugs, stat, transformer=lambda x: x, compiler=lambda x: x):
    """
    Creates a json output file for the given stat and set of bugs.
    """
    stats = []
    for bug in bugs:
        for item in bug[stat]:
            stats.append(transformer(item))
    processed_statistic = compiler(stats)
    with open(path + stat + '.json', 'w') as outfile:
        json.dump(processed_statistic, outfile)
    outfile.close()


def store_collections(path, bugs):
    """
    Stores the collections:
    (keyword => [BZ id, ...])
    (BZ id => Bug)
    """
    keymap = {}
    bugmap = {}

    for bug in bugs:
        bugmap[bug['id']] = bug
        for word in bug['keywords']:
            if not keymap.has_key(word[0]):
                keymap[word[0]] = []
            keymap[word[0]].append(str(bug['id']))

    with open(path + 'keymap.json', 'w') as outfile:
        json.dump(keymap, outfile)
    outfile.close()

    with open(path + 'bugmap.json', 'w') as outfile:
        json.dump(bugmap, outfile)
    outfile.close()




