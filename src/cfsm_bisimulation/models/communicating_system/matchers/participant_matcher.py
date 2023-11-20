from .matcher import Matcher
from .no_candidate_match_exception import NoCandidateMatchException


class ParticipantMatcher(Matcher):

    def match(self, action):
        left_participant = self.match_participant_with(action.left_participant)
        right_participant = self.match_participant_with(action.right_participant)

        return left_participant, right_participant

    def match_participant_with(self, participant_id):
        if not self.match_manager.has_matched(participant_id):
            if not self.match_manager.has_candidates():
                raise NoCandidateMatchException(f'There is no candidates for participant: {participant_id}')

            self.take_decision(participant_id, self.match_manager.candidates_copy())

        return self.match_manager.get_match(participant_id)

    def serialize(self):
        return {
            'participants': self.match_manager.serialize()
        }
