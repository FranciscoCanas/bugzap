__author__ = 'fcanas'
import json
from pprint import pprint
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
import tf_idf


class Preprocessor():
    """
    """
    bugs = []
    documents = []
    words_black_list = stopwords.words('english')

    def __init__(self, data_file):
        """
        """
        with open(data_file) as j:
            self.jdata = json.load(j)
            self.construct_bugs()

    def construct_bugs(self):
        """
        """
        for bug in self.jdata:
            pbug = {'id': str(bug['id']), 'description': bug['description']}
            self.process_comments(pbug, bug['comments'])
            self.bugs.append(pbug)
        self.documents = self.construct_documents_list()


    def process_description(self, pbug, desc):
        """
        """
        vocab = self.vocab_pipeline(desc)
        pbug['tokenized_desc'] = vocab


    def process_comments(self, pbug, comments):
        """
        """
        tags = []
        pcomments = []
        for comment in comments:
            pcomment = {}
            comment_tags = self.pre_process_pipeline(comment['body'])
            pcomment['comment'] = comment['body']
            pcomment['tokenized_comment'] = comment_tags
            candidates = self.find_keyword_candidates(comment_tags)
            tags += candidates
            pcomments.append(pcomment)
        pbug['comments'] = pcomments
        pbug['candidates'] = tags

    def construct_documents_list(self):
        """
        Generates a list of all the 'documents': that is, a list of bodies of text created by
        putting together every comment for each bug.
        Returns a list of lists of tokens.
        """
        documents = []
        for bug in self.bugs:
            bug['document'] = self.construct_document_from_bug(bug)
            documents.append(bug['document'])
        return documents

    def construct_document_from_bug(self, bug):
        """
        Generates a single document from the description and all of the comments in a bug.
        Returns this doc as a list of tokens.
        """
        document = nltk.word_tokenize(bug['id'])
        for comment in bug['comments']:
            document += (nltk.word_tokenize(comment['comment']))
        return document

    def pre_process_pipeline(self, text):
        """
        1) Divide content into tokens.
        2) Filter out useless tokens.
        3) stem? perhaps.
        4) POS tag tokens.
        """
        tokens = self.tokenize(text)
        tokens = self.filter_tokens(tokens)
        #tokens = self.stem_tokens(tokens)
        tokens = nltk.pos_tag(tokens)
        return tokens

    def find_keyword_candidates(self, tags):
        """
        1) Extract nouns, proper nouns, and adjectives from tags.
        2) Choose only commonly occuring words, instead of uniquely occuring ones.
        """
        candidates = [tag for tag in tags if tag[1] in ['NN', 'JJ', 'NNP']]
        return candidates

    def extract_keywords(self, candidates, document, documents):
        """
        1) Compute tf-idf for each of the candidates.
        2) Remove candidates with score less than 1/5 of maximal value.
        """
        scores = []
        for candidate in candidates:
            score = self.compute_tf_idf(candidate[0], document, documents)
            if score > (self.maximal / 5):
                scores.append((candidate[0], score))
        return candidates

    def tokenize(self, text):
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        return tokens

    def stem_tokens(self, words):
        porter = nltk.PorterStemmer()
        return [porter.stem(word) for word in words]

    def pre_process_text(self, text):
        """
        1) Lower case
        """
        return map(unicode.lower,text)


    def filter_tokens(self, tokens):
        """
        Remove numerics, punctuation, and stop words.
        """
        nums = re.compile("^[0-9]*$")
        tokens = [token for token in tokens
                  if token not in self.words_black_list
            and not nums.match(token)]
        return tokens


if __name__ == "__main__":
    p = Preprocessor('my.bugs.json')
    pprint(p.bugs[0]['comments'])
    d = p.construct_documents_list()
    pprint(d[0])





