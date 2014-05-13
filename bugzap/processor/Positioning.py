
class Positioning():

    def __init__(self):
        pass

    def compute_position_score(self, tokens, document):
        """
        Compute the positioning score for each of the tokens in this
        document and return a map of token => score.
        """
        self.scores = {}
        for token in tokens:
            if not token in self.scores.keys():
                self.scores[token] = self.positioning_score(token, document)
        return self.scores

    def first_occurrence(self, token, body):
        """
        Return the index of the first occurrence of token in
        the body of tokens.
        """
        try:
            index = body.index(token)
        except ValueError:
            index = len(body)
        return index

    def positioning_score(self, token, body):
        """
        Return a score based on the position of token in a
        body of tokens, normalized by length.
        """
        return 1.0 - float(self.first_occurrence(token, body)) / float(len(body))