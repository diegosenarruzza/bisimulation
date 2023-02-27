from libs.tools import merge_dicts
from .matcher import Matcher
from .decision import Decision
from .no_candidate_match_exception import NoCandidateMatchException


class MessageMatcher(Matcher):

    def __init__(self, decider, match_manager, variable_matcher):
        super().__init__(decider, match_manager)
        self.variable_matcher = variable_matcher

    def match(self, interaction):
        compatible_messages, message_candidates = self.match_manager.candidates_collections_for(interaction)
        if len(compatible_messages) == 0:
            raise NoCandidateMatchException(f'There is no compatible candidates for message: {interaction.message}')

        if not self.match_manager.has_matched(interaction.message):
            if len(message_candidates) == 0:
                raise NoCandidateMatchException(f'There is no candidates for message: {interaction.message}')

            self.decider.take(
                Decision(self, interaction.message, message_candidates)
            )

        return self.match_manager.get_match(interaction.message)

    def decide_match(self, matched, candidate):
        super().decide_match(matched, candidate)
        self.variable_matcher.decide_match(matched, candidate)

    def rollback_match(self, matched, candidate):
        super().rollback_match(matched, candidate)
        self.variable_matcher.rollback_match(matched, candidate)

    def serialize(self):
        return merge_dicts(
            {'messages': self.match_manager.serialize()},
            self.variable_matcher.serialize()
        )

    def enable_symmetric_mode(self):
        super().enable_symmetric_mode()
        self.variable_matcher.enable_symmetric_mode()

    def disable_symmetric_mode(self):
        super().disable_symmetric_mode()
        self.variable_matcher.disable_symmetric_mode()
