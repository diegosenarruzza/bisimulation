from ...libs.tools import powerset
from itertools import product
from ...models.stratified_bisimulation_strategies.knowledge import Knowledge


def dfs(start, end, visited=None, path=[]):
    if visited is None:
        visited = set()

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
        # First approach could be: states x PowerSet(assertions) as candidates for each automaton
        # This approach filter the reachable states from the state which makes available an assertion
        # (the target of the corresponding transition)
        left_candidates = self.left_candidates_builder.build()
        right_candidates = self.right_candidates_builder.build()

        candidates = set(product(left_candidates, right_candidates))
        return candidates

    class CandidatesBuilder:

        def __init__(self, afsm):
            self.afsm = afsm
            self.reachable_states_cache = {}

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

            # There is a problem with And assertions, at moment to check if and cleaned And assertion
            # exists in current relation,
            # this will be false, cause cleaned assertion was never calculated and was never incorporated
            # in initial relation.
            # ej:   label: f(int x), knowledge: And(x > 0, y > 0), cleaned_assertion: y > 0, state: q
            #       initial_relation = (q, And(x > 0, y > 0)), and it wil check if (q, y > 0) \in initial_relation.
            # This method extends knowledge when an And assertion is reachable for a transition that redefine a variable
            # (and so clean it).
            # to all reachable states from the one that redefine the assertion.
            self._fill_reachable_states_with_cleaned_assertions(assertions_by_state)

            return assertions_by_state

        def _fill_reachable_states_with_cleaned_assertions(self, assertions_by_state):
            for transition in self.afsm.all_transitions():
                available_assertions_until_source = assertions_by_state[transition.source] - {transition.assertion}

                for assertion in available_assertions_until_source:
                    cleaned_assertion = assertion.clean_by(transition.label)
                    if cleaned_assertion is not None and assertion != cleaned_assertion:
                        for state in self._reachable_states_from(transition.target):
                            assertions_by_state[state].add(cleaned_assertion)

        # An end_state is reachable from start_state if there is a path between start_state and it.
        def _reachable_states_from(self, start_state):
            if start_state not in self.reachable_states_cache:
                self.reachable_states_cache[start_state] = {
                    end_state for end_state in self.afsm.get_states() if dfs(start_state, end_state) is not None
                }

            return self.reachable_states_cache[start_state]

        def knowledge_set_for(self, assertions_set):
            assertions_sets = powerset(assertions_set)
            knowledge_set = {Knowledge(assertions) for assertions in assertions_sets}

            return {knowledge for knowledge in knowledge_set if knowledge.is_satisfiable()}
