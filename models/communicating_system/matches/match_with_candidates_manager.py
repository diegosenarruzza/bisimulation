from libs.symmetrical_collections.list import SymmetricalList
from .match_manager import MatchManager


class MatchWithCandidatesManager(MatchManager):

    def __init__(self, candidates, symmetric_candidates):
        self.candidates = SymmetricalList(candidates, symmetric_candidates)
        super().__init__()

    def match(self, matched, matching):
        self.candidates.remove(matched, matching)
        super().match(matched, matching)

    def unmatch(self, matched, matching):
        self.candidates.add(matched, matching)
        super().unmatch(matched, matching)

    def enable_symmetric_mode(self):
        self.candidates.enable_symmetric_mode()
        super().enable_symmetric_mode()

    def disable_symmetric_mode(self):
        self.candidates.disable_symmetric_mode()
        super().disable_symmetric_mode()

    def has_candidates(self):
        return self.candidates.is_empty()

    def candidates(self):
        return self.candidates.copy()
