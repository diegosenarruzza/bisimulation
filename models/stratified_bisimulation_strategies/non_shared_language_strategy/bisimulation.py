from .match_exception import MatchException
from .simulation import NonSharedLanguageSimulationStrategy
from ..shared_language_strategy.bisimulation import SharedLanguageBisimulationStrategy


class NonSharedLanguageBisimulationStrategy(SharedLanguageBisimulationStrategy):

    def __init__(self, afsm_left, afsm_right, matcher):
        super().__init__(afsm_left, afsm_right)
        self.matcher = matcher
        self.initial_relation = None

    def execute(self, minimize):
        self._try_calculate_bisimulation_relation()

        if minimize:
            self._minimize_current_relation()

    def result(self):
        return super().result(), self.matcher.serialize()

    def _try_calculate_bisimulation_relation(self):
        self._set_initial_relation_as_current()
        try:
            self._calculate_bisimulation_from_current_relation()
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

    def _initial_relation(self):
        if self.initial_relation is None:
            self.initial_relation = super()._initial_relation()

        return self.initial_relation

    def _enable_symmetric_mode_with(self, candidate_element):
        self.symmetric_mode = True
        self.current_simulation = NonSharedLanguageSimulationStrategy(self, tuple(reversed(candidate_element)))
        self.matcher.enable_symmetric_mode()

    def _disable_symmetric_mode_with(self, candidate_element):
        self.symmetric_mode = False
        self.current_simulation = NonSharedLanguageSimulationStrategy(self, candidate_element)
        self.matcher.disable_symmetric_mode()