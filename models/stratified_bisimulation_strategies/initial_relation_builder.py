from libs.tools import powerset
from itertools import product
from models.stratified_bisimulation_strategies.knowledge import Knowledge


def knowledge_sets(s):
    assertions = powerset(s)
    sets = {Knowledge(assertions_set) for assertions_set in assertions}

    return {knowledge for knowledge in sets if knowledge.is_satisfiable()}


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
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right

    def build(self):
        # First approach could be do: states x PowerSet(assertions) as candidates for each automata
        # This approach filters the states of each assertion, leaving those that are reachable from the states that define the variables of that assertion.
        left_candidates = self._calculate_candidates_for(self.afsm_left)
        right_candidates = self._calculate_candidates_for(self.afsm_right)

        candidates = set(product(left_candidates, right_candidates))
        return candidates

    def _calculate_candidates_for(self, afsm):
        assertions = afsm.all_assertions()
        owner_variable_states_by_assertion = {}
        for assertion in assertions:
            if len(assertion.get_variables()) > 0:
                owner_variable_states_by_assertion[assertion] = {transition.target for transition in afsm.transitions_that_define(assertion.get_variables())}

        assertions_by_state = {}
        for end_state in afsm.get_states():
            assertions_by_state[end_state.id] = set()
            for assertion, start_states in owner_variable_states_by_assertion.items():
                # If there is a path between any state p and a state owner of a variable, any assertion with that variable could finalize in a knowledge of p.
                if any(dfs(start_state, end_state, set(), []) is not None for start_state in start_states):
                    assertions_by_state[end_state.id].add(assertion)

        candidates = []
        for state_id, assertions_set in assertions_by_state.items():
            state = afsm.states[state_id]
            candidates += [(state, knowledge) for knowledge in knowledge_sets(assertions_set)]
        #
        return candidates
