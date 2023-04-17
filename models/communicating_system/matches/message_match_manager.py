from .match_with_candidates_manager import MatchWithCandidatesManager


class MessageMatchManager(MatchWithCandidatesManager):

    def __init__(self, matches, candidates, participant_match_manager):
        super().__init__(matches, candidates)
        self.participant_match_manager = participant_match_manager

    def candidates_collections_from(self, interaction, simulator_state):
        compatible_messages = [interaction.message for interaction in self._compatible_interactions_with(interaction, simulator_state)]
        message_candidates = self._message_candidates_from(compatible_messages)
        return message_candidates

    def _compatible_interactions_with(self, interaction, simulator_state):
        return [
            transition.label for transition in simulator_state.get_transitions()
            if self._interactions_are_compatibles(interaction, transition.label)
        ]

    # Son candidatos, para esta interaccion, los mensajes (candidatos) que esten en el conjunto de candidatos validos
    def _message_candidates_from(self, compatible_messages):
        return [candidate for candidate in self.candidates.current_collection() if candidate in compatible_messages]

    def _interactions_are_compatibles(self, matchable_interaction, candidate_interaction):
        sender = self.participant_match_manager.get_match(matchable_interaction.sender)
        receiver = self.participant_match_manager.get_match(matchable_interaction.receiver)
        return sender == candidate_interaction.sender and \
            receiver == candidate_interaction.receiver and \
            matchable_interaction.message.is_compatible_with(candidate_interaction.message)
