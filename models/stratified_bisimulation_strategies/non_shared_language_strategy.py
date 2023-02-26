from .match_exception import MatchException
from .shared_language_strategy import SharedLanguageBisimulationStrategy


class NonSharedLanguageBisimulationStrategy(SharedLanguageBisimulationStrategy):

    def __init__(self, afsm_left, afsm_right, matcher):
        super().__init__(afsm_left, afsm_right)
        self.matcher = matcher
        self.initial_relation = None

    def execute(self):
        self._try_calculate_bisimulation_relation()
        self._minimize_current_relation()

    def result(self):
        return super().result(), self.matcher.serialize()

    def _try_calculate_bisimulation_relation(self):
        self._set_initial_relation_as_current()
        try:
            self._calculate_bisimulation_relation()
            if not self.result_is_a_bisimulation():
                self._retry_if_is_possible()
        except MatchException:
            self._retry_if_is_possible()

    def _retry_if_is_possible(self):
        self.matcher.match_next()
        if self.matcher.has_more_possible_matches():
            self._try_calculate_bisimulation_relation()
        else:
            self._invalidate_current_relation()

    def _set_initial_relation_as_current(self):
        self.current_relation = self._initial_relation()

    def _initial_relation(self):
        if self.initial_relation is None:
            self.initial_relation = super()._initial_relation()

        return self.initial_relation

    def _get_transitions_with_simulated_label_from(self, simulating_state):
        matched_label = self.matcher.match(self.current_simulated_transition.label)
        return simulating_state.get_transitions_with(matched_label)

    def _enable_symmetric_mode(self):
        super()._enable_symmetric_mode()
        self.matcher.disable_symmetric_mode()

    def _disable_symmetric_mode(self):
        super()._disable_symmetric_mode()
        self.matcher.enable_symmetric_mode()

    #
    # def _clean_knowledge(self):
    #     super()._clean_knowledge()
        # TODO: ver si tengo que matchear
        # self.current_knowledge = clean_knowledge_for(self.current_knowledge, label)

    # _is_able_to_simulate_knowledge
