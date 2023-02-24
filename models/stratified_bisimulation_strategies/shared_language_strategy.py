from libs.tools import powerset, clean_knowledge_for
from itertools import product
from z3 import Solver, sat, And, Or, Implies


class SharedLanguagesBisimulationStrategy:

    def __init__(self, afsm_left, afsm_right, initial_relation=None):
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right
        self.symmetric_mode = False
        self.current_relation = initial_relation
        self.current_knowledge = set({})

    def execute(self):
        self._set_initial_relation()
        self._calculate_bisimulation_relation()

        # Si no obtuve una relacion de bisimulacion desde la relacion inicial, entonces no la voy a obtener sacando elementos.
        # En lugar de devolver una relacion no valida, devuelvo un conjunto vacio.
        if not self.result_is_a_bisimulation():
            self.invalidate_current_relation()

        # Saco todos los elementos tq la relacion sigue siendo una bisimulacion
        for i in range(0, len(self.current_relation)):
            removed_element = self.current_relation.pop(0)
            strategy = self.__class__(self.afsm_left, self.afsm_right, self.current_relation)
            strategy.execute()

            # Si la nueva relacion es vacia, entonces el elemento que saque era necesario
            if not strategy.result_is_a_bisimulation():
                self.current_relation.append(removed_element)

    def result(self):
        return set(self.current_relation)

    def _initial_relation(self):
        assertions = self.afsm_left.all_assertions().union(self.afsm_right.all_assertions())
        all_possible_knowledge = list(map(lambda knowledge: frozenset(knowledge), powerset(assertions)))
        return list(product(self.afsm_left.get_states(), all_possible_knowledge, self.afsm_right.get_states()))

    def _set_initial_relation(self):
        if self.current_relation is None:
            self.current_relation = self._initial_relation()

    def result_is_a_bisimulation(self):
        initial_element = (self.afsm_left.initial_state, frozenset(), self.afsm_right.initial_state)
        return len(self.current_relation) > 0 and initial_element in self.current_relation

    def invalidate_current_relation(self):
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
                if self.is_able_to_simulate_falling_into(simulated_state, simulating_state):
                    self.symmetric_mode = True
                    if self.is_able_to_simulate_falling_into(simulating_state, simulated_state):
                        next_relation.append(relation_element)
                    self.symmetric_mode = False

    def is_able_to_simulate_falling_into(self, simulated_state, simulating_state):
        is_able = True
        transitions = simulated_state.get_transitions()
        i = 0

        # Si corta porque no cumple is_able, entonces es porque existe una accion que "simulating_state" no puede simular, o que puede pero no cae en la relacion
        # Si corta porque i < len(transitions) entonces recorrio todas las acciones y "simulating_state" siempre pudo simular a e y caer dentro de la relacion
        while is_able and i < len(transitions):
            transition = transitions[i]
            label = transition.label

            # Saco las assertions cuyas variables van a ser sobreescritas por la transicion actual
            if label.has_variable():
                self.clean_knowledge_with(label)

            simulating_transitions = self.get_transitions_with_label_from(simulating_state, label)

            # Necesito verificar si existe algun subconjunto de transiciones desde "simulation_state", que me sirva para simular la transicion de "self"
            # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "self"
            # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

            is_able = self.exists_a_valid_transition_subset_that_simulates(transition, simulating_transitions)

            i += 1

        return is_able

    def clean_knowledge_with(self, label):
        self.current_knowledge = clean_knowledge_for(self.current_knowledge, label)

    # TODO: en estrategia con lenguage no compartido sobreescrivir esto, matchear el label y hacer super()... con el match.
    def get_transitions_with_label_from(self, state, label):
        return state.get_transitions_with(label)

    def exists_a_valid_transition_subset_that_simulates(self, simulated_transition, simulating_transitions):
        # No tomo el subconjunto vacio porque no seria valido. Si no hay mas conjuntos que el vacio, entonces nunca entra al loop y devuelve False
        simulating_transitions_subsets = list(powerset(simulating_transitions))
        simulating_transitions_subsets.remove(())

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulating_transitions_subsets):
            simulating_transitions_subset = list(simulating_transitions_subsets[j])

            # si encontre un sub-conjunto de transiciones, cuya implicacion es satisfacible y ademas cae dentro de la aproximacion, entonces es valido
            valid_transitions_set_exists = self._is_able_to_simulate_knowledge(simulated_transition, simulating_transitions_subset) and \
                                           self.transitions_subset_fall_into_relation(simulated_transition, simulating_transitions_subset)

            j += 1

        return valid_transitions_set_exists

    # Usamos z3-prover. Las assertions tienen que estar escritas con este framework.
    def _is_able_to_simulate_knowledge(self, simulated_transition, simulation_transitions_subset):
        simulation_assertions = {transition.assertion for transition in simulation_transitions_subset}

        transition_knowledge = And(self.current_knowledge.union({simulated_transition.assertion}))
        simulation_transition_knowledge = And(self.current_knowledge.union({Or(simulation_assertions)}))

        solver = Solver()

        return solver.check(Implies(transition_knowledge, simulation_transition_knowledge)) == sat

    def transitions_subset_fall_into_relation(self, simulated_transition, simulating_transitions_subset):
        fall_into_current_relation = False
        k = 0

        # me fijo si todas las transiciones del sub-conjunto caen dentro de la aproximacion que me pasaron por parametro
        while not fall_into_current_relation and k < len(simulating_transitions_subset):
            simulating_transition = simulating_transitions_subset[k]

            if self.symmetric_mode:
                related_element = (
                    simulating_transition.target,
                    self.current_knowledge.union({simulated_transition.assertion, simulating_transition.assertion}),
                    simulated_transition.target
                )
            else:
                related_element = (
                    simulated_transition.target,
                    self.current_knowledge.union({simulated_transition.assertion, simulating_transition.assertion}),
                    simulating_transition.target
                )

            fall_into_current_relation = related_element in self.current_relation

            k += 1

        return fall_into_current_relation
