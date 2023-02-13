from models.state import State
from models.transition import Transition
from libs.tools import powerset, symetric_relation_of, TrueAssertion

from itertools import product


class AFSM:

    def __init__(self):
        self.states = {}
        self.transitions_by_source_id = {}
        self.initial_state = None

    def add_state(self, id):
        # validate not present
        self.states[id] = State(self, id)
        self.transitions_by_source_id[id] = []

    def add_states(self, *ids):
        for id in ids:
            self.add_state(id)

    def set_as_initial(self, id):
        # validate exists
        self.initial_state = self.states[id]

    # assertion must to be a z3 assertion
    def add_transition_between(self, source_id, target_id, label, assertion=TrueAssertion):
        # validate present
        # validate transition not exist

        source = self.states[source_id]
        target = self.states[target_id]

        transition = Transition(source, target, label, assertion)

        self.transitions_by_source_id[source_id].append(transition)

    def transitions_of(self, id):
        #  validate present
        return self.transitions_by_source_id[id]

    def transitions_with_label_of(self, id, label):
        return set(filter(lambda transition: transition.label == label, self.transitions_of(id)))

    def all_assertions(self):
        return set(
            map(
                lambda transition: transition.assertion,
                [transition for transitions in list(self.transitions_by_source_id.values()) for transition in transitions]
            )
        )

    def get_states(self):
        return set(self.states.values())

    # Se esta asumiendo que tanto "self", como "afsm" son validos, i.e. que cumplen con lo que cumple un cfsm que son los que estamos usando de base.
    def build_bisimulation_with(self, afsm):
        relation = self._build_stratified_bisimulation_from(self._initial_relation(afsm))

        # Si no obtuve una relacion de bisimulacion desde la relacion inicial, entonces no la voy a obtener sacando elementos.
        # En lugar de devolver una relacion no valida, devuelvo un conjunto vacio.
        if not self._is_a_bisimulation(afsm, relation):
            relation = []

        # Saco todos los elementos tq la relacion sigue siendo una bisimulacion
        for i in range(0, len(relation)):
            removed_element = relation.pop(0)
            smallest_relation = self._build_stratified_bisimulation_from(relation)

            # Si la nueva relacion es vacia, entonces el elemento que saque era necesario
            if not self._is_a_bisimulation(afsm, smallest_relation):
                relation.append(removed_element)

        return set(relation).union(set(symetric_relation_of(relation)))

    def _build_stratified_bisimulation_from(self, initial_relation):
        current_relation = []
        next_relation = initial_relation

        while current_relation != next_relation:
            current_relation = next_relation
            next_relation = []

            for (e, knowledge, f) in current_relation:
                # si e puede imitar a f y f puede imitar a e (cayendo siempre dentro de la current_relation) entonces tienen que estar en la siguiente aprox.
                e_is_able_to_simulate_f = e.is_able_to_simulate_falling_into(f, set(knowledge), current_relation)
                f_is_able_to_simulate_e = f.is_able_to_simulate_falling_into(e, set(knowledge), symetric_relation_of(current_relation))

                if e_is_able_to_simulate_f and f_is_able_to_simulate_e:
                    next_relation.append((e, knowledge, f))

        return current_relation

    def _initial_relation(self, afsm):
        assertions = self.all_assertions().union(afsm.all_assertions())
        all_possible_knowledge = list(map(lambda knowledge: frozenset(knowledge), powerset(assertions)))
        return list(product(self.get_states(), all_possible_knowledge, afsm.get_states()))

    def _is_a_bisimulation(self, afsm, relation):
        initial_element = (self.initial_state, frozenset(), afsm.initial_state)
        return len(relation) > 0 and initial_element in relation
