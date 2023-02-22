from .decision import Decision


class MessageMatcher:

    def __init__(self, decider, candidates, interactions, participant_matcher):
        self.decider = decider
        self.candidates = list(candidates)
        self.interactions = interactions
        self.matches = {}
        self.participant_matcher = participant_matcher

    def match(self, interaction):
        valid_candidates = self.get_valid_candidates_set_for(interaction)
        if len(valid_candidates) == 0:
            raise Exception('no more candidates')

        message_hash = str(interaction.message)
        if message_hash not in self.matches:
            # De los canidatos validos, filtra por aquellos que esten dentro del conjunto de candidatos del matcher
            candidates = [valid_candidate for valid_candidate in valid_candidates if valid_candidate in self.candidates]
            self.decider.take(
                Decision(self, message_hash, candidates)
            )

        return self.matches[message_hash]

    # Filtra las interacciones segun las que coinciden con el emisor y receptor de la interaccion recivida.
    # Devuelve el conjunto de los mensajes, esos son los mensajes validos que pueden matchear con la interaccion recivida.
    def get_valid_candidates_set_for(self, interaction):
        return [
            candidate_interaction.message for candidate_interaction in self.interactions
            if self.interactions_are_compatibles(interaction, candidate_interaction)

        ]

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
