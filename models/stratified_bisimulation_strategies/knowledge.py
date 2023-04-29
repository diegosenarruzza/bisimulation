from z3 import And, Implies, Solver, sat
from libs.tools import TrueFormula
from models.assertable_finite_state_machines.assertion import Assertion
TrueAssertion = Assertion(TrueFormula)


class Knowledge:

    def __init__(self, assertions_set):
        self.assertions_set = assertions_set - {TrueAssertion}

    def __repr__(self):
        return str(self.assertions_set)

    def __eq__(self, other):
        return self.assertions_set == other.assertions_set

    def __hash__(self):
        return self.assertions_set.__hash__()

    def clean_by(self, label):
        new_assertions_set = frozenset([assertion for assertion in self.assertions_set if not label.contains_any(assertion.get_variables())])
        return Knowledge(new_assertions_set)

    def union(self, other_knowledge):
        return Knowledge(self.assertions_set.union(other_knowledge.assertions_set))

    def add(self, assertion):
        return Knowledge(self.assertions_set.union({assertion}))

    def build_implication_with(self, other_knowledge):
        return Implies(self.build_conjunction(), other_knowledge.build_conjunction())

    def build_conjunction(self):
        return And(set(assertion.expression for assertion in self.assertions_set))

    def is_satisfiable(self):
        solver = Solver()
        return solver.check(self.build_conjunction()) == sat
