from ...libs.tools import collect_variables
from z3 import is_and, And


class Assertion:

    def __init__(self, expression):
        self.expression = expression
        self.variables = None

    def __repr__(self):
        return str(self.expression)

    def __eq__(self, other):
        return self.expression == other.expression

    def __hash__(self):
        return self.expression.__hash__()

    def get_variables(self):
        if self.variables is None:
            self.variables = collect_variables(self.expression)

        return self.variables

    def _is_and(self):
        return is_and(self.expression)

    def clean_by(self, label):
        cleaned_assertion = self
        if label.contains_any(self.get_variables()):
            if self._is_and():
                cleaned_assertion = self.clean_and_by(label)
            else:
                cleaned_assertion = None

        return cleaned_assertion

    def clean_and_by(self, label):
        cleaned_sub_expressions = [sub_expression for sub_expression in self.expression.children() if not label.contains_any(collect_variables(sub_expression))]

        if len(cleaned_sub_expressions) == 0:
            return None

        return Assertion(And(cleaned_sub_expressions))
