from libs.tools import collect_variables


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
