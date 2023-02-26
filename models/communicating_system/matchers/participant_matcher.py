from libs.tools import merge_dicts
from .matcher import Matcher
from .decision import Decision
from .no_candidate_match_exception import NoCandidateMatchException


class ParticipantMatcher(Matcher):

    def match(self, interaction):
        matched_sender = self.match_for(interaction.sender)
        matched_receiver = self.match_for(interaction.receiver)

        return matched_sender, matched_receiver

    def match_for(self, participant_id):
        if not self.match_manager.has_matched(participant_id):
            if not self.match_manager.has_candidates():
                raise NoCandidateMatchException(f'There is no candidates for participant: {participant_id}')
            self.decider.take(
                Decision(self, participant_id, self.match_manager.candidates_copy())
            )

        return self.match_manager.get_match(participant_id)

    def serialize(self):
        return {
            'participants': self.match_manager.serialize()
        }
