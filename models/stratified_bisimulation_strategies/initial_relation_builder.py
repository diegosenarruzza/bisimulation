from libs.tools import powerset
from itertools import product
from models.stratified_bisimulation_strategies.knowledge import Knowledge
from models.assertable_finite_state_machines.assertion import Assertion
from z3 import is_and, And


def dfs(start, end, visited, path):
    visited.add(start)
    path.append(start)
    if start == end:
        return path
    for transition in start.get_transitions():
        if transition.target not in visited:
            new_path = dfs(transition.target, end, visited, path)
            if new_path:
                return new_path
    path.pop()
    return None


class InitialRelationBuilder:

    def __init__(self, afsm_left, afsm_right):
        self.left_candidates_builder = self.CandidatesBuilder(afsm_left)
        self.right_candidates_builder = self.CandidatesBuilder(afsm_right)

    def build(self):
        # First approach could be do: states x PowerSet(assertions) as candidates for each automaton
        # This approach filter the reachable states from the state which makes available an assertion (the target of the corresponding transition)
        left_candidates = self.left_candidates_builder.build()
        right_candidates = self.right_candidates_builder.build()

        candidates = set(product(left_candidates, right_candidates))
        return candidates

    class CandidatesBuilder:

        def __init__(self, afsm):
            self.afsm = afsm

        def build(self):
            assertions_by_state = self._build_reachable_assertions_by_state()

            candidates = []
            for state, assertions_set in assertions_by_state.items():
                candidates += [(state, knowledge) for knowledge in self.knowledge_set_for(assertions_set)]

            return candidates

        def _build_reachable_assertions_by_state(self):
            assertions_by_state = {}
            for state in self.afsm.get_states():
                assertions_by_state[state] = set()

            for transition in self.afsm.all_transitions():
                reachable_states = self._reachable_states_from(transition.target)
                for state in reachable_states:
                    assertions_by_state[state].add(transition.assertion)

            for transition in self.afsm.all_transitions():
                available_assertions_until_source = assertions_by_state[transition.source] - {transition.assertion}
                available_and_assertions_until_source = {assertion for assertion in available_assertions_until_source if is_and(assertion.expression)}

                for assertion in available_and_assertions_until_source:
                    if transition.label.contains_any(assertion.get_variables()):
                        non_redefined_assertion = self.cleaned_and_assertion(assertion, transition)

                        for state in self._reachable_states_from(transition.target):
                            if non_redefined_assertion is not None and non_redefined_assertion != assertion:
                                assertions_by_state[state].add(non_redefined_assertion)

            return assertions_by_state

        def cleaned_and_assertion(self, assertion, transition):
            non_redefined_sub_expressions = []
            # Me quedo con las sub expresiones de esta assertion, que no sean redefinidas en esta transicion
            for sub_expression in assertion.expression.children():
                sub_assertion = Assertion(sub_expression)
                if not transition.label.contains_any(sub_assertion.get_variables()):
                    non_redefined_sub_expressions.append(sub_expression)

            # Si quedan expresiones a usar como parte del conocimiento, las agrego
            non_redefined_assertion = None
            if len(non_redefined_sub_expressions) > 0:
                if len(non_redefined_sub_expressions) == 1:
                    non_redefined_assertion = Assertion(non_redefined_sub_expressions[0])
                else:
                    non_redefined_assertion = Assertion(And(non_redefined_sub_expressions))

            return non_redefined_assertion

        def _reachable_states_from(self, start_state):
            # An end_state is reachable from start_state if there is a path between start_state and it.
            return {end_state for end_state in self.afsm.get_states() if dfs(start_state, end_state, set(), []) is not None}

        def knowledge_set_for(self, assertions_set):
            assertions_sets = powerset(assertions_set)
            knowledge_set = {Knowledge(assertions) for assertions in assertions_sets}

            return {knowledge for knowledge in knowledge_set if knowledge.is_satisfiable()}
