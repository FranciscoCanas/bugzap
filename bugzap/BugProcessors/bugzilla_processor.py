from BugProcessors.bugprocessor import BugProcessor

__author__ = 'fcanas'

ID = 'id'
BODY = 'body'
COMMENTS = 'comments'
DESCRIPTION = 'description'
URL = 'base_url'

class BugzillaProcessor(BugProcessor):
    """
    Bugzilla bug report processor.
    """
    nlp_args = {
        'black_list': [],
        'normalize': True,
        'stem': False,
        'lemmatize': False,
        'pos_list': ['NN','NNP'],
        'tfidf_cutoff': 0.002
    }

    def construct_documents(self):
        """
        Fill the list of documents by gathering all text body from description and comments of each
        bugzilla report.
        """
        for doc in self.jdata:
            document = {}
            document[ID] = doc[ID]
            document[BODY] = doc[DESCRIPTION] + " " + self.join_comments(doc[COMMENTS])
            self.documents.append(document)

    @staticmethod
    def join_comments(comments):
        """
        Pieces all bugzilla comment bodies together into a single blob.
        """
        return " ".join([comment['body'] for comment in comments if comment.has_key('body')])