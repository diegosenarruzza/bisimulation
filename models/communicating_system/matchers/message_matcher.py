from libs.tools import merge_dicts
from .matcher import Matcher
from .decision import Decision
from .no_candidate_match_exception import NoCandidateMatchException


class MessageMatcher(Matcher):

    def __init__(self, decider, match_manager, variable_matcher):
        super().__init__(decider, match_manager)
        # self.decider = decider
        # self.match_manager = match_manager
        self.variable_matcher = variable_matcher
        # self.candidates = list(candidates)
        # self.interactions = interactions
        # self.matches = {}
        # self.variable_matcher = VariableMatcher()
        # self.symmetric_matches = False

    def match(self, interaction):
        compatible_messages, message_candidates = self.match_manager.candidates_collections_for(interaction)
        # valid_candidates = self.valid_candidates_for(interaction)
        if len(compatible_messages) == 0:
            raise NoCandidateMatchException(f'There is no compatible candidates for message: {interaction.message}')

        if not self.match_manager.has_matched(interaction.message):
            if len(message_candidates) == 0:
                raise NoCandidateMatchException(f'There is no candidates for message: {interaction.message}')

            self.decider.take(
                Decision(self, interaction.message, message_candidates)
            )

        return self.match_manager.get_match(interaction.message)

    # Los mensajes candidatos validos son aquellos cuyas interacciones son compatibles con la interaccion a matchear
    # def valid_candidates_for(self, interaction):
    #     return [
    #         candidate_interaction.message for candidate_interaction in self.interactions
    #         if self.interactions_are_compatibles(interaction, candidate_interaction)
    #
    #     ]
    #
    # # Son candidatos, para esta interaccion, los mensajes que estne en el conjunto de candidatos validos
    # def message_candidates_from(self, valid_candidates):
    #     return [candidate for candidate in self.candidates if candidate in valid_candidates]
    #
    # def interactions_are_compatibles(self, matchable_interaction, candidate_interaction):
    #     sender, receiver = self.participant_matcher.match(matchable_interaction)
    #     return sender == candidate_interaction.sender and \
    #         receiver == candidate_interaction.receiver and \
    #         matchable_interaction.message.is_compatible_with(candidate_interaction.message)
    #
    # def decide_match(self, matched, candidate):
    #     self.match_manager.match(matched, candidate)
    #     # self.candidates.remove(candidate)
    #     # self.matches[str(matched)] = candidate
    #
    # def rollback_match(self, matched, candidate):
    #     self.match_manager.unmatch(matched, candidate)
    #     # self.candidates.append(candidate)
    #     # del self.matches[str(matched)]
    #
    # # def serialize(self):
    # #     return merge_dicts(
    # #         {'message_matches': self.matches},
    # #         self.variable_matcher.serialize()
    # #     )
    #
    # def enable_symmetric_mode(self):
    #     self.match_manager.enable_symmetric_mode()
    #
    # def disable_symmetric_mode(self):
    #     self.match_manager.disable_symmetric_mode()

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
