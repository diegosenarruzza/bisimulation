from z3 import is_int_value, is_string_value, is_true, is_false, is_and, is_or, is_not, is_distinct, is_eq, is_gt, is_ge, is_lt, is_le, is_int, is_bool, is_string, And, Or, Not, Int, Bool, String


def rename_variables(expression, renames):

    if is_int_value(expression):
        return expression.as_long()

    if is_string_value(expression):
        return expression.as_string()

    if is_true(expression) or is_false(expression):
        return expression

    if is_and(expression):
        children = [rename_variables(child, renames) for child in expression.children()]
        return And(children)
    elif is_or(expression):
        children = [rename_variables(child, renames) for child in expression.children()]
        return Or(children)
    elif is_not(expression):
        sub_exp = expression.children()[0]
        return Not(rename_variables(sub_exp, renames))

    elif is_distinct(expression):
        left, right = rename_comparison(expression, renames)
        return left != right

    elif is_eq(expression):
        left, right = rename_comparison(expression, renames)
        return left == right

    elif is_gt(expression):
        left, right = rename_comparison(expression, renames)
        return left > right
    elif is_ge(expression):
        left, right = rename_comparison(expression, renames)
        return left >= right

    elif is_lt(expression):
        left, right = rename_comparison(expression, renames)
        return left < right
    elif is_le(expression):
        left, right = rename_comparison(expression, renames)
        return left <= right

    elif is_int(expression):
        return Int(rename_variable(expression, renames))

    elif is_bool(expression):
        return Bool(rename_variable(expression, renames))

    elif is_string(expression):
        return String(rename_variable(expression, renames))

    # Cualquier otra, no esta contemplada. Hay que agregarla
    return expression


def rename_comparison(comparison, renames):
    left, right = [rename_variables(child, renames) for child in comparison.children()]
    return left, right


def rename_variable(variable, renames):
    return renames[str(variable)]
