import unittest
from z3 import Int
from specs.resources.afsm_example_1_1 import afsm_example_1_1
from specs.resources.afsm_example_1_2 import afsm_example_1_2
from specs.resources.afsm_example_2_1 import afsm_example_2_1
from specs.resources.afsm_example_3_1 import afsm_example_3_1
from specs.resources.afsm_example_3_2 import afsm_example_3_2


class AFSMCase(unittest.TestCase):

    def test_must_be_bisimilar_with_itself(self):
        p0 = afsm_example_2_1.states['p0']
        p1 = afsm_example_2_1.states['p1']

        expected_relation = {
            (p0, frozenset(), p0),
            (p1, frozenset({Int('x') > 0}), p1),
            (p0, frozenset({Int('x') > 0, Int('y') > Int('x')}), p0)
        }
        relation = afsm_example_2_1.build_bisimulation_with(afsm_example_2_1)
        self.assertEqual(expected_relation, relation)

    def test_must_be_bisimilars_example_3(self):
        p0 = afsm_example_3_1.states['p0']
        p1 = afsm_example_3_1.states['p1']
        q0 = afsm_example_3_2.states['q0']
        q1 = afsm_example_3_2.states['q1']

        x = Int('x')

        expected_relation = {
            (p0, frozenset(), q0),
            (p1, frozenset({x != 0, x > 0}), q1),
            (p1, frozenset({x != 0, x < 0}), q1)
        }
        relation = afsm_example_3_1.build_bisimulation_with(afsm_example_3_2)
        self.assertEqual(expected_relation, relation)


if __name__ == '__main__':
    unittest.main()
