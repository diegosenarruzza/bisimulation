from ..factories.match_manager_factory import MatchManagerFactory
from ..matchers.decider import Decider
from ..matchers.action_matcher import ActionMatcher
from ..matchers.participant_matcher import ParticipantMatcher
from ..matchers.message_matcher import MessageMatcher
from ..matchers.variable_matcher import VariableMatcher
from libs.symmetrical_collections.symmetry_mode import SymmetryMode


class MatcherFactory:

    def __init__(self, cfsm_left, cfsm_right):
        self.cfsm_left = cfsm_left
        self.cfsm_right = cfsm_right
        self.symmetry_mode = SymmetryMode(False)
        self.decider = Decider(self.symmetry_mode)
        self.match_manager_factory = MatchManagerFactory(cfsm_left, cfsm_right, self.symmetry_mode)

    def action_matcher(self):
        return ActionMatcher(
            self.decider,
            self.participant_matcher(),
            self.message_matcher(),
            self.symmetry_mode
        )

    def participant_matcher(self):
        return ParticipantMatcher(
            self.decider,
            self.match_manager_factory.participant_match(),
            self.symmetry_mode
        )

    def message_matcher(self):
        return MessageMatcher(
            self.decider,
            self.match_manager_factory.message_match(),
            self.variable_matcher(),
            self.symmetry_mode
        )

    def variable_matcher(self):
        return VariableMatcher(
            self.decider,
            self.match_manager_factory.variable_match(),
            self.symmetry_mode
        )
