class MatchManager:

    def __init__(self, matches):
        self.matches = matches

    def match(self, matched, candidate):
        self.matches.add(matched, candidate)

    def unmatch(self, matched, candidate):
        self.matches.remove(matched, candidate)

    def has_matched(self, matched):
        return self.matches.includes(matched)

    def get_match(self, matched):
        return self.matches.get(matched)

    def serialize(self):
        return self.matches.collection

    def copy(self):
        return self.matches.copy()
