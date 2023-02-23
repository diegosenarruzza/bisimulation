from ..interaction import Interaction
from .decider import Decider
from .participant_matcher import ParticipantMatcher
from .message_matcher import MessageMatcher


class InteractionMatcher:

    def __init__(self, interactions, participant_candidates, message_candidates):
        self.decider = Decider()
        self.participant_matcher = ParticipantMatcher(self.decider,  participant_candidates)
        self.message_matcher = MessageMatcher(self.decider, message_candidates, interactions, self.participant_matcher)

    def match(self, interaction):
        sender, receiver = self.participant_matcher.match(interaction)
        message = self.message_matcher.match(interaction)

        return Interaction(sender, receiver, message)

    def match_next(self):
        self.decider.take_next_decision()

    def has_more_possible_matches(self):
        return self.decider.there_are_decisions_to_take()

    def serialize(self):
        return {
            'participant_matches': self.participant_matcher.matches,
            'message_matches': self.message_matcher.matches
        }
