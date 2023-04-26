from .match_with_candidates_manager import MatchWithCandidatesManager


class MessageMatchManager(MatchWithCandidatesManager):

    def __init__(self, matches, candidates, actions, participant_match_manager):
        super().__init__(matches, candidates)
        self.actions = actions
        self.participant_match_manager = participant_match_manager

    def candidates_collections_for(self, action):
        compatible_messages = [action.message for action in self._compatible_actions_with(action)]
        message_candidates = self._message_candidates_from(compatible_messages)
        return compatible_messages, message_candidates

    def _compatible_actions_with(self, action):
        return [
            candidate_action for candidate_action in self.actions.current_collection()
            if self._actions_are_compatibles(action, candidate_action)

        ]

    # Son candidatos, para esta accion, los mensajes compatibles que esten en el conjunto de candidatos validos
    def _message_candidates_from(self, compatible_messages):
        return [candidate for candidate in self.candidates.current_collection() if candidate in compatible_messages]

    def _actions_are_compatibles(self, matchable_action, candidate_action):
        sender = self.participant_match_manager.get_match(matchable_action.sender)
        receiver = self.participant_match_manager.get_match(matchable_action.receiver)
        return sender == candidate_action.sender and \
            receiver == candidate_action.receiver and \
            matchable_action.message.is_compatible_with(candidate_action.message)
