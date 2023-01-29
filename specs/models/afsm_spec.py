import unittest
from specs.resources.afsm_example_1_1 import afsm_example_1_1
from specs.resources.afsm_example_1_2 import afsm_example_1_2
from specs.resources.afsm_example_2_1 import afsm_example_2_1
from z3 import Int

class AFSMCase(unittest.TestCase):

    def test_must_be_bisimilar_with_itself(self):
        p0 = afsm_example_2_1.states['p0']
        p1 = afsm_example_2_1.states['p1']

        expected_relation = {
            (p0, (), p0),
            (p1, (Int('x') > 0,), p1),
            (p0, (Int('x') > 0, Int('y') > Int('x')), p0)
        }
        relation = afsm_example_2_1.build_bisimulation_with(afsm_example_2_1)
        self.assertEqual(expected_relation, relation)


    # TODO: Esta dando errror. Hacer test unitarios de los demas componentes y ver donde falla
    def test_must_return_bisimulation_relation_when_are_bisimilars(self):
        bisimulation = afsm_example_1_1.build_bisimulation_with(afsm_example_1_2)
        self.assertEqual(len(bisimulation), 6)


if __name__ == '__main__':
    unittest.main()
