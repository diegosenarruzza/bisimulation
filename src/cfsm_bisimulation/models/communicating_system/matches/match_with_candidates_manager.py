from .match_manager import MatchManager


class MatchWithCandidatesManager(MatchManager):

    def __init__(self, matches, candidates):
        self.candidates = candidates
        super().__init__(matches)

    def match(self, matched, candidate):
        self.candidates.remove(candidate, matched)
        super().match(matched, candidate)

    def unmatch(self, matched, candidate):
        self.candidates.add(candidate, matched)
        super().unmatch(matched, candidate)

    def has_candidates(self):
        return self.candidates.is_empty()

    def candidates_copy(self):
        return self.candidates.copy()
