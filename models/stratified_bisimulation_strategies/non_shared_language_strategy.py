from .match_exception import MatchException
from .shared_language_strategy import SharedLanguageBisimulationStrategy


class NonSharedLanguageBisimulationStrategy(SharedLanguageBisimulationStrategy):

    def __init__(self, afsm_left, afsm_right, matcher):
        super().__init__(afsm_left, afsm_right)
        self.matcher = matcher

    def execute(self):
        while not self.result_is_a_bisimulation() and self.matcher.has_more_possible_matches:
            self._set_initial_relation()
            try:
                self._calculate_bisimulation_relation()
            except MatchException:
                pass
            self.matcher.match_next()

        if not self.result_is_a_bisimulation():
            self._invalidate_current_relation()

        self._minimize_current_relation()

    def result(self):
        return super().result(), self.matcher.serialize()

    def _get_transitions_with_label_from(self, state, label):
        matched_label = self.matcher.match(label)
        return super()._get_transitions_with_label_from(state, matched_label)

    def _clean_knowledge_with(self, label):
        super()._clean_knowledge_with(label)
        # TODO: ver si tengo que matchear
        # self.current_knowledge = clean_knowledge_for(self.current_knowledge, label)

    # _is_able_to_simulate_knowledge
