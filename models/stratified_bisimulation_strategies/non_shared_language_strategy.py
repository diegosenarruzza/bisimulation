from .match_exception import MatchException
from .shared_language_strategy import SharedLanguageBisimulationStrategy
from z3 import Solver, sat, And, Or, Implies


class NonSharedLanguageBisimulationStrategy(SharedLanguageBisimulationStrategy):

    def __init__(self, afsm_left, afsm_right, matcher):
        super().__init__(afsm_left, afsm_right)
        self.matcher = matcher
        self.initial_relation = None

    def execute(self):
        self._try_calculate_bisimulation_relation()
        self._minimize_current_relation()

    def result(self):
        return self.match_current_relation(), self.matcher.serialize()

    def match_current_relation(self):
        matched_relation = set()
        for simulated_state, knowledge, simulating_state in self.current_relation:
            matched_knowledge = self._match_expressions_set_from(knowledge)
            matched_relation.add((simulated_state, frozenset(matched_knowledge), simulating_state))

        return matched_relation

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

    def _set_current_knowledge(self, knowledge):
        self._define_variables_on(knowledge)
        super()._set_current_knowledge(knowledge)

    def _set_current_simulated_transition(self, simulated_transition):
        self._define_variables_on({simulated_transition.assertion})
        super()._set_current_simulated_transition(simulated_transition)

    # Necesito definir las variables del conocimiento actual. Para eso
    # tengo que matchear los mensajes a los que pertenecen (en sus respectivos automatas)
    def _define_variables_on(self, knowledge):
        for assertion in knowledge:
            interactions = assertion.interactions_that_define_variables()
            current_symmetric_mode = self.symmetric_mode
            if assertion.graph == self.afsm_left:
                self._disable_symmetric_mode()
            else:
                self._enable_symmetric_mode()
            for interaction in interactions:
                self.matcher.match(interaction)
            self.symmetric_mode = current_symmetric_mode

    def _is_able_to_simulate_knowledge(self, simulation_transitions_subset):
        simulation_assertions = {transition.assertion for transition in simulation_transitions_subset}
        self._define_variables_on(simulation_assertions)

        # Necesito obtener los matches de las assertions. En este punto se supone que todas ya fueron matcheadas.
        matched_current_knowledge = self._match_expressions_set_from(self.current_knowledge)
        matched_current_simulated_assertions = self._match_expressions_set_from({self.current_simulated_transition.assertion})
        matched_simulation_assertions = self._match_expressions_set_from(simulation_assertions)

        transition_knowledge = And(matched_current_knowledge.union(matched_current_simulated_assertions))
        simulation_transition_knowledge = And(matched_current_knowledge.union({Or(matched_simulation_assertions)}))

        solver = Solver()

        return solver.check(Implies(transition_knowledge, simulation_transition_knowledge)) == sat

    def _match_expressions_set_from(self, assertions):
        matched_expressions = set()
        for assertion in assertions:
            current_symmetric_mode = self.symmetric_mode
            if assertion.graph == self.afsm_left:
                self._disable_symmetric_mode()
                matched_assertion = self.matcher.match_assertion(assertion)
            else:
                matched_assertion = assertion
                # self._enable_symmetric_mode()
            matched_expressions = matched_expressions.union({matched_assertion.expression})
            self.symmetric_mode = current_symmetric_mode

        return matched_expressions
