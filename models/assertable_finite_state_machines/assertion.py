from libs.tools import collect_variables


class Assertion:

    def __init__(self, expression):
        self.expression = expression
        self.variables = None
        # self.graph = graph

    def __repr__(self):
        return str(self.expression)

    def __eq__(self, other):
        return self.expression == other.expression

    # def interactions_that_define_variables(self):
    #     return self.graph.interactions_that_define(self.variables)
    #     # return [self.graph.interaction_that_define(variable) for variable in self.variables]

    def __hash__(self):
        return self.expression.__hash__()

    def get_variables(self):
        if self.variables is None:
            self.variables = collect_variables(self.expression)

        return self.variables
