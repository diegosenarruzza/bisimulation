import unittest
from specs.resources.afsm_example_1_1 import afsm_example_1_1
from specs.resources.afsm_example_1_2 import afsm_example_1_2


class AFSMCase(unittest.TestCase):

    # TODO: Esta dando errror. Hacer test unitarios de los demas componentes y ver donde falla
    def test_must_return_bisimulation_relation_when_are_bisimilars(self):
        bisimulation = afsm_example_1_1.try_bisimulation_with(afsm_example_1_2)
        self.assertTrue(len(bisimulation) > 0)


if __name__ == '__main__':
    unittest.main()
