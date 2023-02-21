from ..interaction import Interaction
from .decider import Decider
from .participant_matcher import ParticipantMatcher
from .message_matcher import MessageMatcher


class InteractionMatcher:

    def __init__(self, participant_candidates, message_candidates):
        self.decider = Decider()
        self.participant_matcher = ParticipantMatcher(self.decider,  participant_candidates)
        self.message_matcher = MessageMatcher(self.decider, message_candidates, self.participant_matcher)

    def match(self, interaction):
        sender, receiver = self.participant_matcher.match(interaction)
        message = self.message_matcher.match(interaction)

        return Interaction(sender, receiver, message)

    def next_match(self):
        self.decider.next()

    def has_more_candidates(self):
        return self.participant_matcher.has_more_candidates() or self.message_matcher.has_more_candidates()
