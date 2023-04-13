from libs.tools import powerset
from itertools import product, chain, combinations
from z3 import BoolVal, Solver, sat
from .knowledge import Knowledge
from ..assertion import Assertion
TrueAssertion = Assertion(BoolVal(True))


class InitialRelationCalculation:

    def __init__(self, afsm_left, afsm_right):
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right

    # En la bisimulacion clasica, haria: afsm_left.states x afsm_right.states como relacion inicial, e iria descartando a partir de ahi
    # Ahora necesito agregar el hecho de que los estados pueden tener conocimiento, pero en principio no se que conocimiento puede tener cada estado
    # Entonces necesito que aparezca cada estado de cada automata, con cada posible conocimiento:
    #  [afsm_left.states x afsm_left.all_assertions] x [afsm_right.states x afsm_right.all_assertions]
    # De todos estos puedo descartar directamente los que tengan assertions que no se contradigan (que si hago un AND, son directamente falsas)

    def calculate(self):
        left_candidates = list(product(self.afsm_left.get_states(), powerset(self.afsm_left.all_assertions())))
        right_candidates = list(product(self.afsm_right.get_states(), powerset(self.afsm_right.all_assertions())))

        return list(product(left_candidates, right_candidates))

    # def calculate(self):
    #     # TODO: podria filtrar los candidatos en donde el conocimiento no se contradiga
    #
    #     left_knowledges = self.knowledges_for(self.afsm_left)
    #     right_knowledges = self.knowledges_for(self.afsm_right)
    #
    #     left_candidates = list(product(self.afsm_left.get_states(), left_knowledges))
    #     right_candidates = list(product(self.afsm_right.get_states(), right_knowledges))
    #
    #     return list(product(left_candidates, right_candidates))
    #
    # def knowledges_for(self, afsm):
    #     assertions = afsm.all_assertions()
    #     if TrueAssertion in assertions:
    #         assertions.remove(TrueAssertion)
    #
    #     assertions_powerset = list(map(lambda t: Knowledge(frozenset(t)), chain.from_iterable(combinations(assertions, r) for r in range(len(assertions)+1))))
    #
    #     solver = Solver()
    #
    #     return list(map(lambda k: k.assertions_set, filter(lambda knowledge: solver.check(knowledge.build_conjunction()) == sat, assertions_powerset)))
