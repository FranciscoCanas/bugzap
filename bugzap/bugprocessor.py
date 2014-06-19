import os
import json
from keyextractor.src.extractor import Extractor


class BugProcessor():
    """
    """
    nlp_args = {
            'black_list': ['installer', 'installation', 'jboss', 'eap', 'install', 'problem', 'description', 'reproduce',
                        'user','number', 'new', 'bz', 'ER', 'actual', 'results', 'expected', 'reproducible' 'target', 'release',
                        'milestone', 'run', 'default', 'er','er1', 'er2','er3', 'er4', 'er5', 'er6', 'see', 'severity',
                        'priority', 'error', 'fix', 'actual', 'verified', 'bug', 'steps'],
            'pre_process': True,
            'stem': False,
            'lemmatize': False,
            'pos_list': ['NN','NNP'],
            'tfidf_cutoff': 0.002
        }
    bugs = []
    documents = []
    base_url = 'http://'

    def __init__(self, data_file, data_set_name):
        """
        Load a JSON containing BUGZILLA bug reports and process them into a format useable by the
        keyextractor.
        """

        self.documents = []
        self.metadata = {}
        self.data_set = data_set_name
        self.path = 'documents/' + data_set_name + '/'
        self.target_file = self.path + 'documents.json'

        with open(data_file) as j:
            self.jdata = json.load(j)
        j.close()

        self.construct_documents()
        self.construct_metadata()
        self.export()


        Extractor(self.target_file, 'bugzap/visualization/data/' + data_set_name, self.nlp_args)

    def construct_documents(self):
        """
        Fill the list of documents by gathering all text body from description and comments of each
        bugzilla report.
        """
        for doc in self.jdata:
            document = {}
            document['id'] = doc['id']
            document['body'] = doc['description'] + " " + self.join_comments(doc['comments'])
            self.documents.append(document)

    def construct_metadata(self):
        """
        Creates the metadata dict for this set of bug reports.
        """
        self.metadata['base_url'] = self.generate_base_url()


    def join_comments(self, comments):
        """
        Pieces all bugzilla comment bodies together into a single blob.
        """
        return " ".join([comment['body'] for comment in comments if comment.has_key('body')])

    def generate_base_url(self):
        """
        Makes the base url for this set of bug reports. Uses the first bug report as a
        template.
        """
        bug = self.jdata[0]
        return bug['url'].replace(bug['id'], '{0}')

    def export(self):
        """
        Export the data to the target path.
        """
        data = {'metadata': self.metadata,
                'documents': self.documents}
        make_path(self.path)
        with open(self.target_file, 'w') as outfile:
            json.dump(data, outfile)
        outfile.close()


def make_path(path):
    """
    Ensures the target path for stat reports is created.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
