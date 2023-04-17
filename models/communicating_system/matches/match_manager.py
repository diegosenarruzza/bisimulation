class MatchManager:

    def __init__(self, matches):
        self.matches = matches

    def match(self, matched, matching):
        self.matches.add(matched, matching)

    def unmatch(self, matched, matching):
        self.matches.remove(matched, matching)

    def has_matched(self, matched):
        return self.matches.includes(matched)

    def get_match(self, matched):
        return self.matches.get(matched)

    def serialize(self):
        return self.matches.collection

    def copy(self):
        return self.matches.copy()
