class Matcher:

    def __init__(self, decider, match_manager):
        self.decider = decider
        self.match_manager = match_manager

    def decide_match(self, matched, candidate):
        self.match_manager.match(matched, candidate)

    def rollback_match(self, matched, candidate):
        self.match_manager.unmatch(matched, candidate)

    def enable_symmetric_mode(self):
        self.match_manager.enable_symmetric_mode()

    def disable_symmetric_mode(self):
        self.match_manager.disable_symmetric_mode()
