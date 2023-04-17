from .decision import Decision


class Matcher:

    def __init__(self, decider, match_manager, symmetry_mode):
        self.decider = decider
        self.match_manager = match_manager
        self.symmetry_mode = symmetry_mode

    def take_decision(self, matched, candidates):
        self.decider.take(
            Decision(self, matched, candidates, self.symmetry_mode.copy())
        )

    def decide(self, decision):
        self.match_manager.match(decision.matched, decision.current_candidate)

    def rollback(self, decision):
        self.match_manager.unmatch(decision.matched, decision.current_candidate)
