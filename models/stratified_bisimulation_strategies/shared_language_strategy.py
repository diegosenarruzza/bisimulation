from z3 import Solver, unsat, Or, Not
from libs.tools import powerset
from models.assertable_finite_state_machines.assertion import Assertion
from .knowledge import Knowledge
from .initial_relation_calculation import InitialRelationCalculation


class SharedLanguageBisimulationStrategy:

    def __init__(self, afsm_left, afsm_right):
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right
        self.symmetric_mode = False
        self.current_relation = None

    def execute(self, minimize):
        self._set_initial_relation_as_current()
        self._calculate_bisimulation_from_current_relation()

        # La relacion no es una bisimulacion si: no tiene elementos o, no esta el elemento inicial
        # Se invalida en tal caso
        if not self.result_is_a_bisimulation():
            self._invalidate_current_relation()

        if minimize:
            self._minimize_current_relation()

    def result(self):
        return set(self.current_relation)

    def result_is_a_bisimulation(self):
        if self.current_relation is None:
            return False

        initial_element = ((self.afsm_left.initial_state, frozenset()), (self.afsm_right.initial_state, frozenset()))
        return len(self.current_relation) > 0 and initial_element in self.current_relation

    def _set_initial_relation_as_current(self):
        self.current_relation = InitialRelationCalculation(self.afsm_left, self.afsm_right).calculate()

    def _minimize_current_relation(self):
        # Saco todos los elementos tq la relacion sigue siendo una bisimulacion
        for i in range(0, len(self.current_relation)):
            removed_element = self.current_relation.pop(0)
            smallest_relation = self.current_relation

            self._calculate_bisimulation_from_current_relation()

            # Si la nueva relacion no es una bisimulacion, entonces el elemento que saque era necesario
            if not self.result_is_a_bisimulation():
                smallest_relation.append(removed_element)

            self.current_relation = smallest_relation

    def _invalidate_current_relation(self):
        self.current_relation = []

    def _calculate_bisimulation_from_current_relation(self):
        # Detalle por el hecho de que tiene que ser un do-while
        next_relation = self.current_relation
        self.current_relation = []

        while self.current_relation != next_relation:
            self.current_relation = next_relation
            next_relation = []

            for related_element in self.current_relation:
                self._calculate_bisimulation_for(related_element, next_relation)

    def _enable_symmetric_mode(self):
        self.symmetric_mode = True

    def _disable_symmetric_mode(self):
        self.symmetric_mode = False

    def _calculate_bisimulation_for(self, candidate_element, next_relation):
        (simulated_state, simulated_assertions_set), (simulator_state, simulator_assertions_set) = candidate_element

        # Se tienen que poder simular mutuamente
        self._disable_symmetric_mode()
        if self._is_able_to_simulate_falling_into_current_relation(simulated_state, Knowledge(simulated_assertions_set), simulator_state, Knowledge(simulator_assertions_set)):
            self._enable_symmetric_mode()
            if self._is_able_to_simulate_falling_into_current_relation(simulator_state, Knowledge(simulator_assertions_set), simulated_state, Knowledge(simulated_assertions_set)):
                next_relation.append(candidate_element)

    def _set_current_knowledge(self, knowledge):
        self.current_knowledge = set(knowledge)

    def _is_able_to_simulate_falling_into_current_relation(self, simulated_state, simulated_knowledge, simulator_state, simulator_knowledge):
        is_able = True
        simulated_transitions = simulated_state.get_transitions()
        i = 0

        # Si corta porque no cumple is_able, entonces es porque existe una accion que "simulator_state" no puede simular, o que puede pero no cae en la relacion
        # Si corta porque i < len(transitions) entonces recorrio todas las acciones y "simulator_state" siempre pudo simular a "simulated_state" y caer dentro de la relacion
        while is_able and i < len(simulated_transitions):
            simulated_transition = simulated_transitions[i]

            # Saco las assertions cuyas variables van a ser sobreescritas por la transicion actual
            cleaned_simulated_knowledge = simulated_knowledge.clean_by(simulated_transition.label)
            cleaned_simulator_knowledge = simulator_knowledge.clean_by(simulated_transition.label)
            # self._clean_knowledge()

            simulator_transitions = self._get_transitions_with_simulated_label_from(simulator_state, simulated_transition)

            # Necesito verificar si existe algun subconjunto de transiciones desde "simulator_state", que me sirva para simular la transicion de el "simulated_state"
            # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "simulated_state"
            # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

            is_able = self._exists_a_valid_transition_subset_that_simulates(simulated_transition, simulator_transitions, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

            i += 1

        return is_able

    def _get_transitions_with_simulated_label_from(self, simulating_state, simulated_transition):
        return simulating_state.get_transitions_with(simulated_transition.label)

    def _exists_a_valid_transition_subset_that_simulates(self, simulated_transition, simulating_transitions, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        # No tomo el subconjunto vacio porque no seria valido. Si no hay mas conjuntos que el vacio, entonces nunca entra al loop y devuelve False
        simulating_transitions_subsets = list(powerset(simulating_transitions))
        simulating_transitions_subsets.remove(frozenset())

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulating_transitions_subsets):
            simulating_transitions_subset = list(simulating_transitions_subsets[j])

            # si encontre un sub-conjunto de transiciones, cuya implicacion es satisfacible y ademas cae dentro de la current_relation, entonces es valido
            valid_transitions_set_exists = self._transitions_subset_fall_into_relation(simulated_transition, simulating_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge) and \
                                           self._is_able_to_simulate_knowledge(simulated_transition, simulating_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

            j += 1

        return valid_transitions_set_exists

    # Usamos z3-prover.
    def _is_able_to_simulate_knowledge(self, simulated_transition, simulation_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        simulated_knowledge = cleaned_simulated_knowledge.union(cleaned_simulator_knowledge).add(simulated_transition.assertion)
        simulator_knowledge = cleaned_simulator_knowledge.add(
            Assertion(Or({transition.assertion.expression for transition in simulation_transitions_subset}))
        )

        implication = simulated_knowledge.build_implication_with(simulator_knowledge)
        solver = Solver()

        return solver.check(Not(implication)) == unsat

    def _transitions_subset_fall_into_relation(self, simulated_transition, simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        fall_into_current_relation = False
        k = 0

        # me fijo si todas las transiciones del sub-conjunto caen dentro de la aproximacion que me pasaron por parametro
        while not fall_into_current_relation and k < len(simulator_transitions_subset):
            simulator_transition = simulator_transitions_subset[k]

            simulated_element = (simulated_transition.target, cleaned_simulated_knowledge.add(simulated_transition.assertion).assertions_set)
            simulator_element = (simulator_transition.target, cleaned_simulator_knowledge.add(simulator_transition.assertion).assertions_set)

            if self.symmetric_mode:
                related_element = (simulator_element, simulated_element)
            else:
                related_element = (simulated_element, simulator_element)

            fall_into_current_relation = related_element in self.current_relation

            k += 1

        return fall_into_current_relation
