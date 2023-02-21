from .decision import Decision


class MessageMatcher:

    def __init__(self, decider, candidates, participant_matcher):
        self.decider = decider
        self.candidates = list(candidates)
        self.matches = {}
        self.participant_matcher = participant_matcher

    def match(self, interaction):
        message_hash = str(interaction.message)
        if message_hash not in self.matches:
            self.decider.take(
                Decision(self, message_hash, self.get_candidates_for(interaction))
            )

        return self.matches[message_hash]

    def get_candidates_for(self, interaction):
        return [candidate for candidate in self.candidates if
                self.candidate_is_available_for(candidate, interaction)]

    def candidate_is_available_for(self, message_candidate, interaction):
        sender, receiver = self.participant_matcher.match(interaction)
        return message_candidate.sender == sender and \
            message_candidate.receiver == receiver and \
            message_candidate.payload_sort() == interaction.message.payload_sort()

    def decide_match(self, matched, candidate):
        self.candidates.remove(candidate)
        self.matches[matched] = candidate

    def rollback_match(self, matched, candidate):
        self.candidates.append(candidate)
        del self.matches[matched]

    def has_more_candidates(self):
        return len(self.candidates) > 0
