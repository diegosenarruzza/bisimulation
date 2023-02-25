from ..matches.match_manager import MatchManager
from ..matches.match_with_candidates_manager import MatchWithCandidatesManager
from ..matches.message_match_manager import MessageMatchManager


class MatchManagerFactory:

    def __init__(self, cfsm_left, cfsm_right):
        self.cfsm_left = cfsm_left
        self.cfsm_right = cfsm_right

    def participant_match(self):
        return MatchWithCandidatesManager(
            self.cfsm_left.participants,
            self.cfsm_right.participants
        )

    def message_match(self):
        return MessageMatchManager(
            self.cfsm_left.messages(),
            self.cfsm_right.messages(),
            self.cfsm_left.interactions(),
            self.cfsm_right.interactions(),
            self.participant_match()
        )

    def variable_match(self):
        return MatchManager()
