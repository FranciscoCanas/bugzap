__author__ = 'fcanas'
from BugProcessors.bugprocessor import BugProcessor

__author__ = 'fcanas'

ID = 'id'
BODY = 'body'
COMMENTS = 'comments'
DESCRIPTION = 'description'
URL = 'base_url'

class JiraProcessor(BugProcessor):
    """
    Jira bug report processor.
    """
    nlp_args = {
        'black_list': ['installer', 'installation', 'jboss', 'eap', 'install', 'problem', 'description', 'reproduce',
                    'user','number', 'new', 'bz', 'ER', 'actual', 'results', 'expected', 'reproducible' 'target', 'release',
                    'milestone', 'run', 'default', 'er','er1', 'er2','er3', 'er4', 'er5', 'er6', 'see', 'severity',
                    'priority', 'error', 'fix', 'actual', 'verified', 'bug', 'steps', 'additional'],
        'normalize': True,
        'stem': False,
        'lemmatize': False,
        'pos_list': ['NN','NNP'],
        'tfidf_cutoff': 0.002
    }

    def __init__(self):
        """
        Initialize.
        """
        print "Not supported yet."
        pass


    def construct_documents(self):
        """
        Fill the list of documents by gathering all text body from description and comments of each
        bugzilla report.
        """
        pass
