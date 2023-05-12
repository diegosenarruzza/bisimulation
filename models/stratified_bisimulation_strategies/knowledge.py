from z3 import And, Implies, Solver, sat, is_and
from libs.tools import TrueFormula
from models.assertable_finite_state_machines.assertion import Assertion
TrueAssertion = Assertion(TrueFormula)


class Knowledge:

    def __init__(self, assertions_set):
        self.assertions_set = self._flatten(assertions_set - {TrueAssertion})

    def __repr__(self):
        return str(self.assertions_set)

    def __eq__(self, other):
        return self.assertions_set == other.assertions_set

    def __hash__(self):
        return self.assertions_set.__hash__()

    def clean_by(self, label):
        new_assertions_set = set()
        for assertion in self.assertions_set:

            if is_and(assertion.expression):
                non_redefined_sub_expressions = []
                # Me quedo con las sub expresiones de esta assertion, que no sean redefinidas en esta transicion
                for sub_expression in assertion.expression.children():
                    sub_assertion = Assertion(sub_expression)
                    if not label.contains_any(sub_assertion.get_variables()):
                        non_redefined_sub_expressions.append(sub_expression)

                # Si quedan expresiones a usar como parte del conocimiento, las agrego
                if len(non_redefined_sub_expressions) > 0:
                    for non_redefined_sub_expression in non_redefined_sub_expressions:
                        new_assertions_set.add(Assertion(non_redefined_sub_expression))
            else:
                if not label.contains_any(assertion.get_variables()):
                    new_assertions_set.add(assertion)

        # new_assertions_set = frozenset([assertion for assertion in self.assertions_set if not label.contains_any(assertion.get_variables())])
        return Knowledge(frozenset(new_assertions_set))

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

    def _flatten(self, assertions):
        flatted_assertions = set()
        for assertion in assertions:
            if is_and(assertion.expression):
                for expression in assertion.expression.children():
                    flatted_assertions.add(Assertion(expression))
            else:
                flatted_assertions.add(assertion)
        return frozenset(flatted_assertions)