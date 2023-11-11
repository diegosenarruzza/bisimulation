from z3 import Or, Not, Solver, unsat
from ....libs.tools import powerset
from src.cfsm_bisimulation.models.assertable_finite_state_machines.assertion import Assertion


class SharedLanguageSimulationStrategy:

    def __init__(self, bisimulation, candidate_element_tuple):
        self.bisimulation = bisimulation
        (simulated_state, simulated_knowledge), (simulator_state, simulator_knowledge) = candidate_element_tuple
        self.simulated_state = simulated_state
        self.simulated_knowledge = simulated_knowledge
        self.simulator_state = simulator_state
        self.simulator_knowledge = simulator_knowledge

        self.simulated_transition = None

    def is_able_to_simulate(self):
        is_able = True
        simulated_transitions = self.simulated_state.get_transitions()
        i = 0

        # Si corta porque no cumple is_able, entonces es porque existe una accion que "simulator_state" no puede simular, o que puede pero no cae en la relacion
        # Si corta porque i < len(transitions) entonces recorrio todas las acciones y "simulator_state" siempre pudo simular a "simulated_state" y caer dentro de la relacion
        while is_able and i < len(simulated_transitions):
            self.simulated_transition = simulated_transitions[i]

            # Necesito verificar si existe algun subconjunto de transiciones desde "simulator_state", que me sirva para simular la transicion de el "simulated_state"
            # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "simulated_state"
            # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

            is_able = self._exists_a_valid_transition_subset_that_simulates()

            i += 1

        return is_able

    def _exists_a_valid_transition_subset_that_simulates(self):
        cleaned_simulated_knowledge = self.simulated_knowledge.clean_by(self.simulated_transition.label)
        cleaned_simulator_knowledge = self.simulator_knowledge.clean_by(self.simulated_transition.label)
        simulator_transitions = self.simulator_state.get_transitions_with(self.simulated_transition.label)

        # No tomo el subconjunto vacio porque no seria valido. Si no hay mas conjuntos que el vacio, entonces nunca entra al loop y devuelve False
        simulator_transitions_subsets = list(powerset(simulator_transitions))
        simulator_transitions_subsets.remove(frozenset())

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulator_transitions_subsets):
            simulator_transitions_subset = list(simulator_transitions_subsets[j])
            valid_transitions_set_exists = self._is_a_valid_transition_subset_to_simulate(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

            j += 1

        return valid_transitions_set_exists

    def _is_a_valid_transition_subset_to_simulate(self, simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        simulator_assertion = Assertion(Or({transition.assertion.expression for transition in simulator_transitions_subset}))

        # si encontre un sub-conjunto de transiciones, cuya implicacion es satisfacible y ademas cae dentro de la current_relation, entonces es valido
        return self._transitions_subset_fall_into_relation(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge) and \
               self._is_able_to_simulate_knowledge(simulator_assertion, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

    def _transitions_subset_fall_into_relation(self, simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        fall_into_current_relation = False
        k = 0

        # me fijo si todas las transiciones del sub-conjunto caen dentro de la aproximacion que me pasaron por parametro
        while not fall_into_current_relation and k < len(simulator_transitions_subset):
            simulator_transition = simulator_transitions_subset[k]

            simulated_element = (self.simulated_transition.target, cleaned_simulated_knowledge.add(self.simulated_transition.assertion))
            simulator_element = (simulator_transition.target, cleaned_simulator_knowledge.add(simulator_transition.assertion))

            fall_into_current_relation = self.bisimulation.includes((simulated_element, simulator_element))

            k += 1

        return fall_into_current_relation

    def _is_able_to_simulate_knowledge(self, simulator_assertion, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        simulated_knowledge = cleaned_simulated_knowledge.union(cleaned_simulator_knowledge).add(self.simulated_transition.assertion)
        simulator_knowledge = cleaned_simulator_knowledge.add(simulator_assertion)

        implication = simulated_knowledge.build_implication_with(simulator_knowledge)
        solver = Solver()

        return solver.check(Not(implication)) == unsat
