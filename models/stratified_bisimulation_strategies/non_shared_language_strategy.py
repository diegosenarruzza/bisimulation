from .match_exception import MatchException
from .shared_language_strategy import SharedLanguagesBisimulationStrategy


class NonSharedLanguageBisimulationStrategy(SharedLanguagesBisimulationStrategy):

    def __init__(self, afsm_left, afsm_right, initial_relation=None, matcher=None):
        super().__init__(afsm_left, afsm_right, initial_relation)
        self.matcher = matcher

    def execute(self):
        # is a do-while
        self.try_execute()

        while not self.result_is_a_bisimulation() and self.matcher.has_more_possible_matches():
            self.matcher.match_next()
            self.try_execute()

    def try_execute(self):
        try:
            super().execute()
        except MatchException:
            # do nothing
            pass

    def get_transitions_with_label_from(self, state, label):
        matched_label = self.matcher.match(label)
        return super().get_transitions_with_label_from(state, matched_label)
