from .simulation import SharedLanguageSimulationStrategy
from ..initial_relation_builder import InitialRelationBuilder


class SharedLanguageBisimulationStrategy:

    def __init__(self, afsm_left, afsm_right):
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right
        self.symmetric_mode = False
        self.current_relation = None
        self.current_simulation = None

    def execute(self, minimize):
        self._set_initial_relation_as_current()
        self._calculate_bisimulation_from_current_relation()

        # La relacion no es una bisimulacion si: no tiene elementos o, no esta el elemento inicial
        # Se invalida en tal caso
        if not self.result_is_a_bisimulation():
            self._invalidate_current_relation()

        if minimize:
            self._minimize_current_relation()

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

    def result(self):
        return set(self.current_relation)

    def result_is_a_bisimulation(self):
        if self.current_relation is None:
            return False

        initial_element = ((self.afsm_left.initial_state, frozenset()), (self.afsm_right.initial_state, frozenset()))
        return len(self.current_relation) > 0 and initial_element in self.current_relation

    def _set_initial_relation_as_current(self):
        self.current_relation = self._initial_relation()

    def _initial_relation(self):
        return InitialRelationBuilder(self.afsm_left, self.afsm_right).build()

    def _invalidate_current_relation(self):
        self.current_relation = []

    def _calculate_bisimulation_from_current_relation(self):
        # Detalle por el hecho de que tiene que ser un do-while
        next_relation = self.current_relation
        self.current_relation = []

        while self.current_relation != next_relation:
            self.current_relation = next_relation
            next_relation = []

            for candidate_element in self.current_relation:
                if self._is_a_bisimulation(candidate_element):
                    next_relation.append(candidate_element)

    def _is_a_bisimulation(self, candidate_element):
        self._disable_symmetric_mode_with(candidate_element)

        if self.current_simulation.is_able_to_simulate():
            self._enable_symmetric_mode_with(candidate_element)

            if self.current_simulation.is_able_to_simulate():
                return True

        return False

    def _enable_symmetric_mode_with(self, candidate_element):
        self.symmetric_mode = True
        self.current_simulation = SharedLanguageSimulationStrategy(self, tuple(reversed(candidate_element)))

    def _disable_symmetric_mode_with(self, candidate_element):
        self.symmetric_mode = False
        self.current_simulation = SharedLanguageSimulationStrategy(self, candidate_element)

    def includes(self, element):
        if self.symmetric_mode:
            return tuple(reversed(element)) in self.current_relation
        else:
            return element in self.current_relation
