from libs.tools import merge_dicts
from .matcher import Matcher
from .decision import Decision
from .no_candidate_match_exception import NoCandidateMatchException


class ParticipantMatcher(Matcher):

    # def __init__(self, decider, match_manager):
    #     self.decider = decider
    #     self.match_manager = match_manager

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

        # return self.matches[participant_id]
        return self.match_manager.get_match(participant_id)

    # def decide_match(self, matched, candidate):
    #     self.match_manager.match(matched, candidate)
    #     # self.candidates.remove(candidate)
    #     # self.matches[matched] = candidate
    #
    # def rollback_match(self, matched, candidate):
    #     self.match_manager.unmatch(matched, candidate)
    #     # self.candidates.append(candidate)
    #     # del self.matches[matched]

    def serialize(self):
        return {
            'participants': self.match_manager.serialize()
        }
