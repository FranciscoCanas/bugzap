import os
import json
from Distiller.distiller import Distiller


class BugProcessor():
    default_black_list_path = ''
    """
    Base class responsible for processing bug reports generated by scraper and producing
    document collections in JSON format that are compatible with Distiller lib.
    """
    nlp_args = {
            'black_list': [],
            'normalize': True,
            'stem': False,
            'lemmatize': False,
            'pos_list': ['NN','NNP'],
            'tfidf_cutoff': 0.0001
        }
    bugs = []
    documents = []

    def __init__(self, data_file, data_set_name, black_list_file=None):
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

        self.nlp_args['black_list'] = generate_black_list(black_list_file) + \
                                      generate_black_list(self.default_black_list_path)
        self.construct_documents()
        self.construct_metadata()
        self.export()
        self.runDistiller(data_set_name)

    def construct_documents(self):
        """
        Fill the list of documents by gathering all text body from description and comments of each
        bugzilla report.

        Implemented by child class.
        """
        pass

    def construct_metadata(self):
        """
        Creates the metadata dict for this set of bug reports.
        """
        self.metadata['base_url'] = self.generate_base_url()

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

    def runDistiller(self, data_set_name):
        """
        """
        Distiller(self.target_file, 'bugzap/visualization/data/' + data_set_name, self.nlp_args)


def generate_black_list(path):
    """
    Given the path to a txt file containing space separated tokens,
    it returns a list of said tokens.
    """
    black_list = []
    if path:
        with open(path, 'r') as infile:
            for line in infile.readlines():
                black_list.append(line.strip())
        infile.close()
    return black_list


def make_path(path):
    """
    Ensures the target path for stat reports is created.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
