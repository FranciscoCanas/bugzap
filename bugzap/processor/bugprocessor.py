import json
from pprint import pprint
import nltk
import tf_idf
from preprocessing import pre_process_pipeline, extract_keywords

__author__ = 'mailfrancisco@gmail.com'


class BugProcessor():
    """
    """
    bugs = []
    documents = []
    words_black_list = ['installer', 'installation', 'jboss', 'eap', 'install', 'problem', 'description', 'reproduce',
                        'user','']

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
            pbug = {'id': str(bug['id']), 'description': bug['description'], 'url': bug['url'], 'candidates': []}
            self.process_comments(pbug, bug['comments'])
            self.process_description(pbug, bug['description'])
            self.bugs.append(pbug)
        self.documents = self.construct_documents_list()


    def process_description(self, pbug, desc):
        """
        """
        tags = pre_process_pipeline(desc, self.words_black_list)
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
                comment_tags = pre_process_pipeline(comment['body'], self.words_black_list)
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
        for bug in self.bugs:
            bug['document'] = self.construct_document_from_bug(bug)
            bug['freq_distribution'] = nltk.FreqDist(bug['document'])
            documents.append(bug['document'])
        return documents

    def construct_document_from_bug(self, bug):
        """
        Generates a single document from the description and all of the comments in a bug.
        Returns this doc as a list of tokens.
        """
        document = map(unicode.lower, nltk.word_tokenize(bug['description']))
        for comment in bug['comments']:
            if comment.has_key('comment'):
                document += map(unicode.lower, nltk.word_tokenize(comment['comment']))
        return document


def stats(bugs):
    all_keywords = []
    for bug in bugs:
        for word in bug['keywords'][0:5]:
            all_keywords.append(word[0])
    keyword_freq = nltk.FreqDist(all_keywords)
    keyword_freq.plot(25,title="Installer Bugs for EAP 6.2")


if __name__ == "__main__":
    p = BugProcessor('installer.bugs.json')
    documents = p.construct_documents_list()
    print str.format("{0} bugs found and analysed.", str(len(p.bugs)))
    print
    with open('processed.json', 'w') as outfile:
        for bug in p.bugs:
            bug['tfidf'] = tf_idf.compute_tf_idf(bug['candidates'], bug['document'], documents)
            bug['keywords'] = extract_keywords(bug['tfidf'], maximal=0.1)
            print "url: " + bug['url']
            print "Description: " + bug['description']
            print "Top 5 Keywords:"
            pprint(bug['keywords'][0:5])
            print
            json.dump(bug, outfile)
    stats(p.bugs)








