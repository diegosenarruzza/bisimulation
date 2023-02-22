class Decision:

    def __init__(self, matcher, matched, candidates):
        self.matcher = matcher
        self.matched = matched
        self.candidates = list(candidates)
        self.current_candidate = None

    def has_more_candidates(self):
        return len(self.candidates) > 0

    def decide(self):
        self.current_candidate = self.candidates.pop()
        self.matcher.decide_match(self.matched, self.current_candidate)

    def rollback(self):
        self.matcher.rollback_match(self.matched, self.current_candidate)
        self.current_candidate = None


class NoDecision:

    def decide(self):
        return None

    def rollback(self):
        return None

    def has_more_candidates(self):
        return False
