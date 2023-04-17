from .match_manager import MatchManager


class MatchWithCandidatesManager(MatchManager):

    def __init__(self, matches, candidates):
        self.candidates = candidates
        super().__init__(matches)

    def match(self, matched, matching):
        self.candidates.remove(matching, matched)
        super().match(matched, matching)

    def unmatch(self, matched, matching):
        self.candidates.add(matching, matched)
        super().unmatch(matched, matching)

    def has_candidates(self):
        return self.candidates.is_empty()

    def candidates_copy(self):
        return self.candidates.copy()
