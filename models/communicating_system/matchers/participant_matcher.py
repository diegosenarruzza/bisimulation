from .decision import Decision


class ParticipantMatcher:

    def __init__(self, decider, candidates):
        self.decider = decider
        self.candidates = set(candidates)
        self.matches = {}

    def match(self, interaction):
        matched_sender = self.match_for(interaction.sender)
        matched_receiver = self.match_for(interaction.receiver)

        return matched_sender, matched_receiver

    def match_for(self, participant_id):
        if participant_id not in self.matches:
            self.decider.take(
                Decision(self, participant_id, self.candidates)
            )

        return self.matches[participant_id]

    def decide_match(self, matched, candidate):
        self.candidates.remove(candidate)
        self.matches[matched] = candidate

    def rollback_match(self, matched, candidate):
        self.candidates.add(candidate)
        del self.matches[matched]

    def has_more_candidates(self):
        return len(self.candidates) > 0
