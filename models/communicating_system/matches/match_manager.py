from libs.symmetrical_collections.dict import SymmetricalDict


class MatchManager:

    def __init__(self):
        self.matches = SymmetricalDict({}, {})

    def match(self, matched, matching):
        self.matches.add(matched, matching)

    def unmatch(self, matched, matching, symmetric_mode_when_match):
        if symmetric_mode_when_match == self.matches.symmetric_mode:
            self.matches.remove(matched, matching)
        else:
            self.matches.remove(matching, matched)

    def has_matched(self, matched):
        return self.matches.includes(matched)

    def get_match(self, matched):
        return self.matches.get(matched)

    def enable_symmetric_mode(self):
        self.matches.enable_symmetric_mode()

    def disable_symmetric_mode(self):
        self.matches.disable_symmetric_mode()

    def serialize(self):
        return self.matches.collection

    def copy(self):
        return self.matches.copy()
