from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import re
import nltk

__author__ = 'fcanas'


def pre_process_pipeline(text, pos_tag=True, black_list=None, pos_list=['NN', 'JJ', 'NNP'], pre_process=True, stem=True, lemmatize=True):
    """
    Input: "Big blob of text..."

    1) Divide content into tokens.
    2) POS tag tokens.
    3) Filter out only potential candidates.
    3) Normalize
    4) Filter out useless tokens.
    5) Stem.
    6) Lemmatize

    Output: [(word, pos), ...]
    """
    processed = []
    tokens = tokenize(text)
    if pos_tag: tokens = pos_tag_tokens(tokens)

    for token in tokens:
        if not filter_by_pos(token, pos_list) or not filter_by_pattern(token, black_list):
            continue
        if pre_process: token = pre_process_text(token)
        if stem: token = stem_token(token)
        if lemmatize: token = lemmatize_token(token)
        processed.append(token)
    return processed


def tokenize(text):
    """
    Input: "Body of text...:
    Output: [word, ...] list of tokenized words matching regex '\w+'
    """
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens


def pos_tag_tokens(tokens):
    """

    """
    return nltk.pos_tag(tokens)


def filter_by_pos(token, pos_list=['NN', 'JJ', 'NNP']):
    """
    Input: (word, pos)
    Output: True if pos is noun, proper noun, or adj. False otherwise.
    """
    return token[1] in pos_list


def pre_process_text(token):
    """
    Input: (word, pos)
    Output: (word, pos) with lower case word.
    """
    return token[0].lower(), token[1]


def stem_token(token):
    """
    Input: (word, pos)
    Output: (stem of word, pos)
    """
    porter = nltk.PorterStemmer()
    return porter.stem(token[0]), token[1]


def lemmatize_token(token):
    """
    Input: (word, pos)
    Output: (Lemmatized word, pos)
    """
    wnl = nltk.WordNetLemmatizer()
    return wnl.lemmatize(token[0]), token[1]


def filter_by_pattern(token, black_list=None):
    """
    Input: (word, pos), [blacklist_word, ...]
    Filters by removing tokens with words that are numbers, or in the black list or in the stop words list.
    Output: False if word is any of the above. True otherwise.
    """
    if not black_list: black_list = []
    nums = re.compile("^[0-9]*$")
    return token[0].lower() not in map(unicode, black_list) and \
           token[0].lower() not in stopwords.words('english') and \
           not nums.match(token[0])
