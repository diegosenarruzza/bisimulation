from libs.tools import powerset
from itertools import product
from models.stratified_bisimulation_strategies.knowledge import Knowledge


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
                for state in self._reachable_states_from(transition.target):
                    assertions_by_state[state].add(transition.assertion)

            return assertions_by_state

        def _reachable_states_from(self, start_state):
            # An end_state is reachable from start_state if there is a path between start_state and it.
            return {end_state for end_state in self.afsm.get_states() if dfs(start_state, end_state, set(), []) is not None}

        def knowledge_set_for(self, assertions_set):
            assertions_sets = powerset(assertions_set)
            knowledge_set = {Knowledge(assertions_set) for assertions_set in assertions_sets}

            return {knowledge for knowledge in knowledge_set if knowledge.is_satisfiable()}
