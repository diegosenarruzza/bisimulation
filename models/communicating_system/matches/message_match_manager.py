from .match_with_candidates_manager import MatchWithCandidatesManager


class MessageMatchManager(MatchWithCandidatesManager):

    def __init__(self, matches, candidates, interactions, participant_match_manager):
        super().__init__(matches, candidates)
        self.interactions = interactions
        self.participant_match_manager = participant_match_manager

    def candidates_collections_for(self, interaction):
        compatible_messages = [interaction.message for interaction in self._compatible_interactions_with(interaction)]
        message_candidates = self._message_candidates_from(compatible_messages)
        return compatible_messages, message_candidates

    def _compatible_interactions_with(self, interaction):
        # return self.interactions.filter(lambda candidate_interaction: self._interactions_are_compatibles(interaction, candidate_interaction))
        return [
            candidate_interaction for candidate_interaction in self.interactions.current_collection()
            if self._interactions_are_compatibles(interaction, candidate_interaction)

        ]

    # Son candidatos, para esta interaccion, los mensajes que estne en el conjunto de candidatos validos
    def _message_candidates_from(self, compatible_messages):
        return [candidate for candidate in self.candidates.current_collection() if candidate in compatible_messages]

    def _interactions_are_compatibles(self, matchable_interaction, candidate_interaction):
        sender = self.participant_match_manager.get_match(matchable_interaction.sender)
        receiver = self.participant_match_manager.get_match(matchable_interaction.receiver)
        return sender == candidate_interaction.sender and \
            receiver == candidate_interaction.receiver and \
            matchable_interaction.message.is_compatible_with(candidate_interaction.message)
