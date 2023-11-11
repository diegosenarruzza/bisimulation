from itertools import chain, combinations
from z3 import BoolVal, is_var, is_app_of, is_app, Z3_OP_UNINTERPRETED

TrueFormula = BoolVal(True)


def powerset(s):
    # s = {1, 2, 3}
    # powerset(s) = [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]

    return list(map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s)+1))))


# def collect_variables(assertion):
#     variables = set()
#
#     if len(assertion.children()) > 0:
#         for child in assertion.children():
#             variables = variables.union(collect_variables(child))
#     else:
#         variables.add(assertion)
#
#     return variables

def collect_variables(expression):
    if is_var(expression):
        return {expression}
    elif is_app_of(expression, Z3_OP_UNINTERPRETED):
        return {expression}
    elif is_app(expression):
        variables = set()
        for arg in expression.children():
            variables |= collect_variables(arg)
        return variables
    else:
        return set()


# Devuelve un conjunto con las assertions cuyas variables no son las del "label".
def clean_knowledge_for(knowledge, label):
    return set([assertion for assertion in knowledge if not label.contains_any(assertion.variables)])


def merge_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
