from .matcher import Matcher
from .no_candidate_match_exception import NoCandidateMatchException


class ParticipantMatcher(Matcher):

    def match(self, interaction, simulator_state):
        candidate_participant_ids = self.candidates_collection_from(simulator_state, lambda transition: transition.label.sender)
        matched_sender = self.match_participant_with(interaction.sender, candidate_participant_ids)

        candidate_participant_ids = self.candidates_collection_from(simulator_state, lambda transition: transition.label.receiver)
        matched_receiver = self.match_participant_with(interaction.receiver, candidate_participant_ids)

        return matched_sender, matched_receiver

    def match_participant_with(self, participant_id, candidate_participant_ids):
        if not self.match_manager.has_matched(participant_id):
            if len(candidate_participant_ids) == 0:
                raise NoCandidateMatchException(f'There is no candidates for participant: {participant_id}')

            self.take_decision(participant_id, candidate_participant_ids)

        return self.match_manager.get_match(participant_id)

    def candidates_collection_from(self, simulator_state, participant_in):
        compatible_participant_ids = set(participant_in(transition) for transition in simulator_state.get_transitions())
        candidate_participant_ids = [
            participant_id for participant_id in self.match_manager.candidates.current_collection() if participant_id in compatible_participant_ids
        ]
        return candidate_participant_ids

    def serialize(self):
        return {
            'participants': self.match_manager.serialize()
        }
