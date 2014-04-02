from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import re
import nltk

__author__ = 'fcanas'

def pre_process_pipeline(text, black_list):
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
    tokens = pos_tag(tokens)
    for token in tokens:
        if not filter_by_pos(token) or not filter_by_pattern(token, black_list):
            continue
        token = pre_process_text(token)
        token = stem_token(token)
        token = lemmatize_token(token)
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

def pos_tag(tokens):
    """

    """
    return nltk.pos_tag(tokens)


def filter_by_pos(token):
    """
    Input: (word, pos)
    Output: True if pos is noun, proper noun, or adj. False otherwise.
    """
    return token[1] in ['NN', 'JJ', 'NNP']


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



def filter_by_pattern(token, black_list):
    """
    Input: (word, pos), [blacklist_word, ...]
    Filters by removing tokens with words that are numbers, or in the black list or in the stop words list.
    Output: False if word is any of the above. True otherwise.
    """
    nums = re.compile("^[0-9]*$")
    return token[0].lower() not in map(unicode, black_list) and \
           token[0].lower() not in stopwords.words('english') and \
           not nums.match(token[0])


def extract_keywords(candidates, maximal=0.00):
    """
    Input: [(candidate, tf-idf score), ...], maximal value
    1) Compute tf-idf for each of the candidates.
    2) Remove candidates with score less than 1/5 of maximal value.
    Output [(candidate, tf-idf score), ...]
    """
    keywords = []
    for candidate in candidates:
        if candidate[1] > (maximal / 5):
            keywords.append((candidate[0], candidate[1]))
    return keywords