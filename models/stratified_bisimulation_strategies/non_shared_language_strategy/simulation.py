from z3 import Solver, Not, unsat
from libs.tools import powerset
from ..shared_language_strategy.simulation import SharedLanguageSimulationStrategy
from ..knowledge import Knowledge

# Para ver si se cumple la condicion de simulacion del conocimiento, necesito matchear todos los componentes que simulan.
#   - El label de la simulated transition
#   - La assertion de la simulated transition
#   - El simulated knowledge


class NonSharedLanguageSimulationStrategy(SharedLanguageSimulationStrategy):

    def _exists_a_valid_transition_subset_that_simulates(self):
        cleaned_simulated_knowledge = self.simulated_knowledge.clean_by(self.simulated_transition.label)

        # Matcheo el label a simular y lo uso para:
        #   - Limpiar el knowledge simulador
        #   - Buscar las transiciones desde el estado simulador con el mismo label
        matched_simulated_transition_label = self.bisimulation.matcher.match(self.simulated_transition.label)

        cleaned_simulator_knowledge = self.simulator_knowledge.clean_by(matched_simulated_transition_label)
        simulator_transitions = self.simulator_state.get_transitions_with(matched_simulated_transition_label)

        simulator_transitions_subsets = list(powerset(simulator_transitions))
        simulator_transitions_subsets.remove(frozenset())

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulator_transitions_subsets):
            simulator_transitions_subset = list(simulator_transitions_subsets[j])
            valid_transitions_set_exists = self._is_a_valid_transition_subset_to_simulate(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

            j += 1

        return valid_transitions_set_exists

    def _is_able_to_simulate_knowledge(self, simulator_assertion, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        matched_cleaned_simulated_knowledge = self._match_knowledge(cleaned_simulator_knowledge.add(self.simulated_transition.assertion))

        simulated_knowledge = matched_cleaned_simulated_knowledge.add(self.simulated_transition.assertion)
        simulator_knowledge = cleaned_simulator_knowledge.add(simulator_assertion)

        implication = simulated_knowledge.build_implication_with(simulator_knowledge)
        solver = Solver()

        return solver.check(Not(implication)) == unsat

    def _match_knowledge(self, knowledge):
        matched_knowledge = Knowledge(frozenset())

        for assertion in knowledge.assertions_set:
            matched_knowledge.add(
                self.bisimulation.matcher.match_assertion(assertion)
            )
        return matched_knowledge
