import unittest
from libs.z3_renamer import rename_variables
from z3 import Int, String, Bool, And, Or, Not


class Z3RenamerTestCase(unittest.TestCase):

    def test_01_must_rename_simple_variables(self):
        int_var = Int('x')
        string_var = String('y')
        bool_var = Bool('z')

        renames = {'x': 'number', 'y': 'text', 'z': 'is_true'}

        self.assertEqual(Int('number'), rename_variables(int_var, renames))
        self.assertEqual(String('text'), rename_variables(string_var, renames))
        self.assertEqual(Bool('is_true'), rename_variables(bool_var, renames))

    def test_02_rename_comparisons(self):
        gt_formula = Int('x') > 0
        ge_formula = Int('x') >= 0
        lt_formula = Int('x') < 0
        le_formula = Int('x') <= 0
        eq_formula = Int('x') == 0
        renames = {'x': 'number'}

        self.assertEqual(Int('number') > 0, rename_variables(gt_formula, renames))
        self.assertEqual(Int('number') >= 0, rename_variables(ge_formula, renames))
        self.assertEqual(Int('number') < 0, rename_variables(lt_formula, renames))
        self.assertEqual(Int('number') <= 0, rename_variables(le_formula, renames))
        self.assertEqual(Int('number') == 0, rename_variables(eq_formula, renames))

    def test_03_rename_operations_with_one_level(self):
        and_formula = And(Int('x') >= 0, String('p') == '1234')
        or_formula = Or(Int('x') < 0, String('p') == '1234')
        not_formula = Not(Int('x') == 1)
        renames = {'x': 'number', 'p': 'password'}

        self.assertEqual(
            And(Int('number') >= 0, String('password') == '1234'),
            rename_variables(and_formula, renames)
        )
        self.assertEqual(
            Or(Int('number') < 0, String('password') == '1234'),
            rename_variables(or_formula, renames)
        )
        self.assertEqual(
            Not(Int('number') == 1),
            rename_variables(not_formula, renames)
        )

    def test_04_must_not_rename_constants(self):
        formula = String('password') == 'password'
        renames = {'password': 'new_password'}

        self.assertEqual(String('new_password') == 'password', rename_variables(formula, renames))


if __name__ == '__main__':
    unittest.main()
