import unittest
from specs.resources.afsm.afsm_example_1 import afsm_example_1
from specs.resources.afsm.afsm_example_2_1 import afsm_example_2_1
from specs.resources.afsm.afsm_example_2_2 import afsm_example_2_2
from specs.resources.afsm.afsm_example_3_1 import afsm_example_3_1
from specs.resources.afsm.afsm_example_3_2 import afsm_example_3_2
from models.assertable_finite_state_machines.assertion import Assertion
from models.stratified_bisimulation_strategies.knowledge import Knowledge
from z3 import Int, BoolVal

true = BoolVal(True)
x = Int('x')
y = Int('y')

x_grater_than_zero = Assertion(Int('x') > 0)
x_lower_than_zero = Assertion(Int('x') < 0)
x_neq_zero = Assertion(Int('x') != 0)
y_grater_than_x = Assertion(Int('y') > Int('x'))


def _(state, *expressions):
    assertions = list(map(Assertion, expressions))
    return state, Knowledge(frozenset(assertions))


class AFSMCase(unittest.TestCase):

    def assertIsSubset(self, expected_relation, relation):
        self.assertTrue(expected_relation.issubset(relation))

    def test_must_be_bisimilar_with_itself(self):
        p0 = afsm_example_1.states['p0']
        p1 = afsm_example_1.states['p1']

        expected_relation = {
            (_(p0), _(p0)),
            (_(p1, x > 0), _(p1, x > 0)),
            (_(p0, x > 0, y > x), _(p0, x > 0, y > x))
        }
        relation = afsm_example_1.calculate_bisimulation_with(afsm_example_1)
        self.assertIsSubset(expected_relation, relation)

    def test_must_be_bisimilars_example_2(self):
        p0 = afsm_example_2_1.states['p0']
        p1 = afsm_example_2_1.states['p1']
        q0 = afsm_example_2_2.states['q0']
        q1 = afsm_example_2_2.states['q1']

        expected_relation = {
            (_(p0), _(q0)),
            (_(p1, x != 0), _(q1, x > 0)),
            (_(p1, x != 0), _(q1, x < 0))
        }
        relation = afsm_example_2_1.calculate_bisimulation_with(afsm_example_2_2)
        self.assertIsSubset(expected_relation, relation)

    def test_must_be_bisimilars_example_3(self):
        p0 = afsm_example_3_1.states['p0']
        p1 = afsm_example_3_1.states['p1']
        p2 = afsm_example_3_1.states['p2']
        p3 = afsm_example_3_1.states['p3']
        q0 = afsm_example_3_2.states['q0']
        q1 = afsm_example_3_2.states['q1']
        q2 = afsm_example_3_2.states['q2']
        q3 = afsm_example_3_2.states['q3']
        q4 = afsm_example_3_2.states['q4']

        expected_relation = {
            (_(p0), _(q0)),
            (_(p1, x != 0), _(q1, x != 0)),
            (_(p2, x != 0, true), _(q2, x != 0, x > 0)),
            (_(p3, x != 0, true), _(q4, x != 0, x > 0, true)),
            (_(p2, x != 0, true), _(q3, x != 0, x < 0)),
            (_(p3, x != 0, true), _(q4, x != 0, x < 0, true))
        }

        relation = afsm_example_3_1.calculate_bisimulation_with(afsm_example_3_2)
        self.assertIsSubset(expected_relation, relation)

    def test_relation_must_be_empty_when_are_not_bisimilars(self):
        relation = afsm_example_1.calculate_bisimulation_with(afsm_example_2_1)
        self.assertEqual(set(), relation)


if __name__ == '__main__':
    unittest.main()
