from ..matches.match_manager import MatchManager
from ..matches.match_with_candidates_manager import MatchWithCandidatesManager
from ..matches.message_match_manager import MessageMatchManager


class MatchManagerFactory:

    def __init__(self, cfsm_left, cfsm_right):
        self.cfsm_left = cfsm_left
        self.cfsm_right = cfsm_right
        self.participant_match_manager = None
        self.message_match_manager = None
        self.variable_match_manager = None

    # Participant candidates to match with cfsm_left are cfsm_right participants.
    def participant_match(self):
        if self.participant_match_manager is None:
            self.participant_match_manager = MatchWithCandidatesManager(
                self.cfsm_right.get_participants(),
                self.cfsm_left.get_participants()
            )
        return self.participant_match_manager

    def message_match(self):
        if self.message_match_manager is None:
            self.message_match_manager = MessageMatchManager(
                self.cfsm_right.messages(),
                self.cfsm_left.messages(),
                self.cfsm_right.interactions(),
                self.cfsm_left.interactions(),
                self.participant_match()
            )
        return self.message_match_manager

    def variable_match(self):
        if self.variable_match_manager is None:
            self.variable_match_manager = MatchManager()
        return self.variable_match_manager
