from ..factories.match_manager_factory import MatchManagerFactory
from ..matchers.decider import Decider
from ..matchers.interaction_matcher import InteractionMatcher
from ..matchers.participant_matcher import ParticipantMatcher
from ..matchers.message_matcher import MessageMatcher
from ..matchers.variable_matcher import VariableMatcher


class MatcherFactory:

    def __init__(self, cfsm_left, cfsm_right):
        self.cfsm_left = cfsm_left
        self.cfsm_right = cfsm_right
        self.match_manager_factory = MatchManagerFactory(cfsm_left, cfsm_right)
        self.decider = Decider()

    def interaction_matcher(self):
        return InteractionMatcher(
            self.decider,
            self.participant_matcher(),
            self.message_matcher()
        )

    def participant_matcher(self):
        return ParticipantMatcher(
            self.decider,
            self.match_manager_factory.participant_match()
        )

    def message_matcher(self):
        return MessageMatcher(
            self.decider,
            self.match_manager_factory.message_match(),
            self.variable_matcher()
        )

    def variable_matcher(self):
        return VariableMatcher(
            self.decider,
            self.match_manager_factory.variable_match()
        )
