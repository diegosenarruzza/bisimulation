from libs.symmetrical_collections.list import SymmetricalList
from .match_manager import MatchManager


class MatchWithCandidatesManager(MatchManager):

    def __init__(self, candidates, symmetric_candidates):
        self.candidates = SymmetricalList(candidates, symmetric_candidates)
        super().__init__()

    def match(self, matched, matching):
        self.candidates.remove(matching, matched)
        super().match(matched, matching)

    def unmatch(self, matched, matching, symmetric_mode_when_match):
        if symmetric_mode_when_match == self.candidates.symmetric_mode:
            self.candidates.add(matching, matched)
        else:
            self.candidates.add(matched, matching)

        super().unmatch(matched, matching, symmetric_mode_when_match)

    def enable_symmetric_mode(self):
        super().enable_symmetric_mode()
        self.candidates.enable_symmetric_mode()

    def disable_symmetric_mode(self):
        super().disable_symmetric_mode()
        self.candidates.disable_symmetric_mode()

    def has_candidates(self):
        return self.candidates.is_empty()

    def candidates_copy(self):
        return self.candidates.copy()
