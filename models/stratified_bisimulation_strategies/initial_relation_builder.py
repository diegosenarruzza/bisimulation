from libs.tools import powerset, TrueFormula
from itertools import product
from models.assertable_finite_state_machines.assertion import Assertion
from models.stratified_bisimulation_strategies.knowledge import Knowledge
TrueAssertion = Assertion(TrueFormula)


def knowledge_sets(s):
    assertions = powerset(s)
    sets = {Knowledge(assertions_set) for assertions_set in assertions}

    return {knowledge for knowledge in sets if knowledge.is_satisfiable()}


class InitialRelationBuilder:

    def __init__(self, afsm_left, afsm_right):
        self.afsm_left = afsm_left
        self.afsm_right = afsm_right

    # En la bisimulacion clasica, haria: afsm_left.states x afsm_right.states como relacion inicial, e iria descartando a partir de ahi
    # Ahora necesito agregar el hecho de que los estados pueden tener conocimiento, pero en principio no se que conocimiento puede tener cada estado
    # Entonces necesito que aparezca cada estado de cada automata, con cada posible conocimiento:
    #  [afsm_left.states x afsm_left.all_assertions] x [afsm_right.states x afsm_right.all_assertions]
    # De todos estos puedo descartar directamente los que tengan assertions que no se contradigan (que si hago un AND, son directamente falsas)

    def build(self):
        left_candidates = list(product(self.afsm_left.get_states(), knowledge_sets(self.afsm_left.all_assertions())))
        right_candidates = list(product(self.afsm_right.get_states(), knowledge_sets(self.afsm_right.all_assertions())))

        candidates = set(product(left_candidates, right_candidates))
        return candidates
