import unittest
from z3 import Int
from ...resources.cfsm.example_1 import cfsm as cfsm_example_1
from ...resources.cfsm.example_2 import cfsm_1 as cfsm_example_2_1, cfsm_2 as cfsm_example_2_2
from ...resources.cfsm.example_3 import cfsm_1 as cfsm_example_3_1, cfsm_2 as cfsm_example_3_2
from models.communicating_system.interaction import Interaction
from models.assertable_finite_state_machines.assertion import Assertion
Message = Interaction.Message
x = Int('x')
number = Int('number')

def _(state, *expressions):
    assertions = list(map(Assertion, expressions))
    return state, frozenset(assertions)


class CFSMTestCase(unittest.TestCase):

    def assertIsSubset(self, expected_relation, relation):
        self.assertTrue(expected_relation.issubset(relation))

    def test_01_must_match_and_be_bisimilar_and_match_with_itself(self):
        q0 = cfsm_example_1.states['q0']
        q1 = cfsm_example_1.states['q1']
        f_x = Message('f', payload=[x])

        expected_relation = {
            (_(q0), _(q0)),
            (_(q1, x > 0), _(q1, x > 0)),
        }
        expected_matches = {
            'participants': {'customer': 'customer', 'service': 'service'},
            'messages': {str(f_x): f_x},
            'variables': {'x': x}
        }

        relation, matches = cfsm_example_1.calculate_bisimulation_with(cfsm_example_1, minimize=True)

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_02_must_match_and_be_bisimilar_when_is_exactly_same_machine_with_diff_names(self):
        p0 = cfsm_example_2_1.states['p0']
        p1 = cfsm_example_2_1.states['p1']
        q0 = cfsm_example_2_2.states['q0']
        q1 = cfsm_example_2_2.states['q1']

        add_message = Message('add', payload=[x])
        add_to_cart_message = Message('add_to_cart', payload=[number])

        expected_relation = {
            (_(p0), _(q0)),
            (_(p1, x > 0), _(q1, number > 0))
        }
        expected_matches = {
            'participants': {'consumer': 'client', 'producer': 'shop'},
            'messages': {str(add_message): add_to_cart_message},
            'variables': {'x': number}
        }

        relation, matches = cfsm_example_2_1.calculate_bisimulation_with(cfsm_example_2_2, minimize=True)

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_03_must_return_empty_relation_and_match_when_is_not_be_bisimilar_but_match(self):
        relation, matches = cfsm_example_3_1.calculate_bisimulation_with(cfsm_example_3_2)

        self.assertEqual(set(), relation)
        self.assertEqual({}, matches)


if __name__ == '__main__':
    unittest.main()
