from libs.tools import merge_dicts
from ..interaction import Interaction
from .participant_matcher import ParticipantMatcher
from .message_matcher import MessageMatcher
from .decider import Decider


class InteractionMatcher:

    def __init__(self, decider, participant_matcher, message_matcher):
        self.decider = decider
        self.participant_matcher = participant_matcher
        self.message_matcher = message_matcher
        # self.match_manager = MatchManager()
        # self.participant_matcher = ParticipantMatcher(self.decider, self.match_manager,  participant_candidates)
        # self.message_matcher = MessageMatcher(self.decider, message_candidates, interactions, self.participant_matcher)
        # self.symmetric_matches = False

    def match(self, interaction):
        sender, receiver = self.participant_matcher.match(interaction)
        message = self.message_matcher.match(interaction)

        return Interaction(sender, receiver, message)

    def match_next(self):
        self.decider.take_next_decision()

    def has_more_possible_matches(self):
        return self.decider.there_are_decisions_to_take()

    def enable_symmetric_mode(self):
        self.participant_matcher.enable_symmetric_mode()
        self.message_matcher.enable_symmetric_mode()

    def disable_symmetric_mode(self):
        self.participant_matcher.disable_symmetric_mode()
        self.message_matcher.disable_symmetric_mode()

    def serialize(self):
        return merge_dicts(
            self.participant_matcher.serialize(),
            self.message_matcher.serialize()
        )
