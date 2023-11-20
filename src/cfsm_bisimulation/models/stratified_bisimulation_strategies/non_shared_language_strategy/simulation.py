from z3 import Solver, Not, unsat
from ....libs.tools import powerset
from ..shared_language_strategy.simulation import SharedLanguageSimulationStrategy

# To see if knowledge simulation condition is satisfied, I need to match every component that simulate:
#   - The simulated transition label
#   - The simulated transition assertion
#   - The simulated knowledge


class NonSharedLanguageSimulationStrategy(SharedLanguageSimulationStrategy):

    def _exists_a_valid_transition_subset_that_simulates(self):
        cleaned_simulated_knowledge = self.simulated_knowledge.clean_by(self.simulated_transition.label)

        matched_simulated_action, self.matched_cleaned_simulated_knowledge = self.bisimulation.match()

        cleaned_simulator_knowledge = self.simulator_knowledge.clean_by(matched_simulated_action)
        simulator_transitions = self.simulator_state.get_transitions_with(matched_simulated_action)

        simulator_transitions_subsets = list(powerset(simulator_transitions))

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulator_transitions_subsets):
            simulator_transitions_subset = list(simulator_transitions_subsets[j])
            valid_transitions_set_exists = self._is_a_valid_transition_subset_to_simulate(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

            j += 1

        return valid_transitions_set_exists

    def _is_able_to_simulate_knowledge(self, simulator_assertion, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        simulated_knowledge = self.matched_cleaned_simulated_knowledge.union(cleaned_simulator_knowledge)
        simulator_knowledge = cleaned_simulator_knowledge.add(simulator_assertion)

        implication = simulated_knowledge.build_implication_with(simulator_knowledge)
        solver = Solver()

        return solver.check(Not(implication)) == unsat
