from .decision import Decision


class Matcher:

    def __init__(self, decider, match_manager):
        self.decider = decider
        self.match_manager = match_manager
        self.symmetric_mode = False

    def decide_match(self, matched, candidate):
        self.match_manager.match(matched, candidate)

    def rollback_match(self, matched, candidate, symmetric_mode_when_match):
        self.match_manager.unmatch(matched, candidate, symmetric_mode_when_match)

    def enable_symmetric_mode(self):
        self.symmetric_mode = True
        self.match_manager.enable_symmetric_mode()

    def disable_symmetric_mode(self):
        self.symmetric_mode = False
        self.match_manager.disable_symmetric_mode()

    def decide(self, matched, candidates):
        self.decider.take(
            Decision(self, matched, candidates, self.symmetric_mode)
        )
