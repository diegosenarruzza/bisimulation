class Decision:

    def __init__(self, matcher, matched, candidates, symmetry_mode_when_match):
        self.matcher = matcher
        self.matched = matched
        self.candidates = list(candidates)
        self.current_candidate = None
        self.symmetry_mode_when_match = symmetry_mode_when_match

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.matched}: {self.current_candidate} or {str(self.candidates)}'

    def has_more_candidates(self):
        return len(self.candidates) > 0

    def decide(self):
        self.current_candidate = self.candidates.pop(0)
        self.matcher.decide(self)

    def rollback(self):
        self.matcher.rollback(self)
        self.current_candidate = None


class NoDecision:

    def __init__(self, initial_symmetry_mode):
        self.symmetry_mode_when_match = initial_symmetry_mode

    def decide(self):
        return None

    def rollback(self):
        return None

    def has_more_candidates(self):
        return False

    def __str__(self):
        return 'NoDecision'

    def __repr__(self):
        return 'NoDecision'
