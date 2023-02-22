from .decision import Decision


class MessageMatcher:

    def __init__(self, decider, candidates, interactions, participant_matcher):
        self.decider = decider
        self.candidates = set(candidates)
        self.interactions = interactions
        self.matches = {}
        self.participant_matcher = participant_matcher

    def match(self, interaction):
        candidates = self.get_valid_candidates_set_for(interaction)
        if len(candidates) == 0:
            raise Exception('no more candidates')

        message_hash = str(interaction.message)
        if message_hash not in self.matches:
            self.decider.take(
                Decision(self, message_hash, candidates)
            )

        return self.matches[message_hash]

    # Filtra las interacciones segun las que coinciden con el emisor y receptor de la interaccion recivida.
    # Devuelve el conjunto de los mensajes, esos son los mensajes validos que pueden matchear con la interaccion recivida.
    def get_valid_candidates_set_for(self, interaction):
        return {
            candidate_interaction.message for candidate_interaction in self.interactions
            if self.interactions_are_compatibles(candidate_interaction, interaction)
        }

    def interactions_are_compatibles(self, interaction, interaction_candidate):
        sender, receiver = self.participant_matcher.match(interaction)
        return sender == interaction_candidate.sender and \
            receiver == interaction_candidate.receiver and \
            interaction.message.is_compatible_with(interaction_candidate.message)

    def is_valid_message_candidate(self, message_candidate, interaction):
        sender, receiver = self.participant_matcher.match(interaction)
        payload_sort = interaction.message.payload_sort()
        return message_candidate.is_available_for(sender, receiver, payload_sort)

    def decide_match(self, matched, candidate):
        self.candidates.remove(candidate)
        self.matches[matched] = candidate

    def rollback_match(self, matched, candidate):
        self.candidates.add(candidate)
        del self.matches[matched]
