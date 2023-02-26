from libs.tools import powerset, clean_knowledge_for
from itertools import product
from z3 import Solver, sat, And, Or, Implies


class SharedLanguageBisimulationStrategy:

    def __init__(self, afsm_left, afsm_right):
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right
        self.symmetric_mode = False
        self.current_relation = None
        self.current_knowledge = None
        self.current_simulated_transition = None

    def execute(self):
        self._set_initial_relation_as_current()
        self._calculate_bisimulation_relation()

        # La relacion puede no ser una bisimulacion porque: no tiene elementos o, no esta el elemento inicial
        # Invalido la relacion (seteo []) para contemplar el segundo caso
        if not self.result_is_a_bisimulation():
            self._invalidate_current_relation()

        self._minimize_current_relation()

    def result(self):
        return set(self.current_relation)

    def result_is_a_bisimulation(self):
        if self.current_relation is None:
            return False

        initial_element = (self.afsm_left.initial_state, frozenset(), self.afsm_right.initial_state)
        return len(self.current_relation) > 0 and initial_element in self.current_relation

    def _set_initial_relation_as_current(self):
        self.current_relation = self._initial_relation()

    def _initial_relation(self):
        assertions = self.afsm_left.all_assertions().union(self.afsm_right.all_assertions())
        all_possible_knowledge = [frozenset(knowledge) for knowledge in powerset(assertions)]
        return list(product(self.afsm_left.get_states(), all_possible_knowledge, self.afsm_right.get_states()))

    def _minimize_current_relation(self):
        # Saco todos los elementos tq la relacion sigue siendo una bisimulacion
        for i in range(0, len(self.current_relation)):
            removed_element = self.current_relation.pop(0)
            smallest_relation = self.current_relation

            self._calculate_bisimulation_relation()

            # Si la nueva relacion es vacia, entonces el elemento que saque era necesario
            if not self.result_is_a_bisimulation():
                smallest_relation.append(removed_element)

            self.current_relation = smallest_relation

    def _invalidate_current_relation(self):
        self.current_relation = []

    def _calculate_bisimulation_relation(self):
        next_relation = self.current_relation
        self.current_relation = []

        while self.current_relation != next_relation:
            self.current_relation = next_relation
            next_relation = []

            for relation_element in self.current_relation:
                simulated_state, knowledge, simulating_state = relation_element
                self.current_knowledge = set(knowledge)

                # si simulated_state puede imitar a simulating_state y simulating_state puede imitar a simulated_state
                # (cayendo siempre dentro de la current_relation) entonces tienen que estar en la siguiente aprox.
                self._disable_symmetric_mode()
                if self._is_able_to_simulate_falling_into(simulated_state, simulating_state):
                    self._enable_symmetric_mode()
                    if self._is_able_to_simulate_falling_into(simulating_state, simulated_state):
                        next_relation.append(relation_element)

    def _enable_symmetric_mode(self):
        self.symmetric_mode = True

    def _disable_symmetric_mode(self):
        self.symmetric_mode = False

    def _is_able_to_simulate_falling_into(self, simulated_state, simulating_state):
        is_able = True
        simulated_transitions = simulated_state.get_transitions()
        i = 0

        # Si corta porque no cumple is_able, entonces es porque existe una accion que "simulating_state" no puede simular, o que puede pero no cae en la relacion
        # Si corta porque i < len(transitions) entonces recorrio todas las acciones y "simulating_state" siempre pudo simular a e y caer dentro de la relacion
        while is_able and i < len(simulated_transitions):
            self.current_simulated_transition = simulated_transitions[i]

            # Saco las assertions cuyas variables van a ser sobreescritas por la transicion actual
            self._clean_knowledge()

            # necesito saber cual ese el label que le corresponde al de la derecha, a partir de el de la izquierda
            # (si symmetric es False)
            # Para buscar el label en el de la derecha, tengo que traducir de izquierda a dereceha (si es symmetric)
            # y de derecha a izquierda (si es no symmetric)

            simulating_transitions = self._get_transitions_with_simulated_label_from(simulating_state)

            # Necesito verificar si existe algun subconjunto de transiciones desde "simulating_state", que me sirva para simular la transicion de el "simulated_state"
            # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "simulated_state"
            # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

            is_able = self._exists_a_valid_transition_subset_that_simulates(simulating_transitions)

            i += 1

        return is_able

    def _clean_knowledge(self):
        if self.current_simulated_transition.label.has_variable():
            self.current_knowledge = clean_knowledge_for(self.current_knowledge, self.current_simulated_transition.label)

    def _get_transitions_with_simulated_label_from(self, simulating_state):
        return simulating_state.get_transitions_with(self.current_simulated_transition.label)

    def _exists_a_valid_transition_subset_that_simulates(self, simulating_transitions):
        # No tomo el subconjunto vacio porque no seria valido. Si no hay mas conjuntos que el vacio, entonces nunca entra al loop y devuelve False
        simulating_transitions_subsets = list(powerset(simulating_transitions))
        simulating_transitions_subsets.remove(())

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulating_transitions_subsets):
            simulating_transitions_subset = list(simulating_transitions_subsets[j])

            # si encontre un sub-conjunto de transiciones, cuya implicacion es satisfacible y ademas cae dentro de la aproximacion, entonces es valido
            valid_transitions_set_exists = self._is_able_to_simulate_knowledge(simulating_transitions_subset) and \
                                           self._transitions_subset_fall_into_relation(simulating_transitions_subset)

            j += 1

        return valid_transitions_set_exists

    # Usamos z3-prover. Las assertions tienen que estar escritas con este framework.
    def _is_able_to_simulate_knowledge(self, simulation_transitions_subset):
        simulation_assertions = {transition.assertion for transition in simulation_transitions_subset}

        transition_knowledge = And(self.current_knowledge.union({self.current_simulated_transition.assertion}))
        simulation_transition_knowledge = And(self.current_knowledge.union({Or(simulation_assertions)}))

        solver = Solver()

        return solver.check(Implies(transition_knowledge, simulation_transition_knowledge)) == sat

    def _transitions_subset_fall_into_relation(self, simulating_transitions_subset):
        fall_into_current_relation = False
        k = 0

        # me fijo si todas las transiciones del sub-conjunto caen dentro de la aproximacion que me pasaron por parametro
        while not fall_into_current_relation and k < len(simulating_transitions_subset):
            simulating_transition = simulating_transitions_subset[k]

            if self.symmetric_mode:
                related_element = (
                    simulating_transition.target,
                    self.current_knowledge.union({self.current_simulated_transition.assertion, simulating_transition.assertion}),
                    self.current_simulated_transition.target
                )
            else:
                related_element = (
                    self.current_simulated_transition.target,
                    self.current_knowledge.union({self.current_simulated_transition.assertion, simulating_transition.assertion}),
                    simulating_transition.target
                )

            fall_into_current_relation = related_element in self.current_relation

            k += 1

        return fall_into_current_relation
