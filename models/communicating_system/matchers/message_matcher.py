from .decision import Decision
from .no_candidate_match_exception import NoCandidateMatchException


class MessageMatcher:

    def __init__(self, decider, candidates, interactions, participant_matcher):
        self.decider = decider
        self.candidates = list(candidates)
        self.interactions = interactions
        self.matches = {}
        self.participant_matcher = participant_matcher

    def match(self, interaction):
        valid_candidates = self.valid_candidates_for(interaction)
        if len(valid_candidates) == 0:
            raise NoCandidateMatchException(f'There is no valid candidates for interaction: {interaction}')

        message_hash = str(interaction.message)
        if message_hash not in self.matches:
            # De los canidatos validos, filtra por aquellos que esten dentro del conjunto de candidatos del matcher
            candidates = self.message_candidates_from(valid_candidates)

            if len(candidates) == 0:
                raise NoCandidateMatchException(f'There is no candidates for interaction: {interaction}')

            self.decider.take(
                Decision(self, message_hash, candidates)
            )

        return self.matches[message_hash]

    # Los mensajes candidatos validos son aquellos cuyas interacciones son compatibles con la interaccion a matchear
    def valid_candidates_for(self, interaction):
        return [
            candidate_interaction.message for candidate_interaction in self.interactions
            if self.interactions_are_compatibles(interaction, candidate_interaction)

        ]

    # Son candidatos, para esta interaccion, los mensajes que estne en el conjunto de candidatos validos
    def message_candidates_from(self, valid_candidates):
        return [candidate for candidate in self.candidates if candidate in valid_candidates]

    def interactions_are_compatibles(self, matchable_interaction, candidate_interaction):
        sender, receiver = self.participant_matcher.match(matchable_interaction)
        return sender == candidate_interaction.sender and \
            receiver == candidate_interaction.receiver and \
            matchable_interaction.message.is_compatible_with(candidate_interaction.message)

    def decide_match(self, matched, candidate):
        self.candidates.remove(candidate)
        self.matches[matched] = candidate

    def rollback_match(self, matched, candidate):
        self.candidates.append(candidate)
        del self.matches[matched]
