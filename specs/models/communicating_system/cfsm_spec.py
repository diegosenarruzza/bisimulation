import unittest
from z3 import Int
from ...resources.cfsm.example_1 import cfsm as cfsm_example_1
from ...resources.cfsm.example_2 import cfsm_1 as cfsm_example_2_1, cfsm_2 as cfsm_example_2_2
from ...resources.cfsm.example_3 import cfsm_1 as cfsm_example_3_1, cfsm_2 as cfsm_example_3_2
from models.communicating_system.interaction import Interaction
from models.assertable_finite_state_machines.assertion import Assertion
Message = Interaction.Message
x = Int('x')
x_grater_than_zero = Assertion(x > 0)


def _(state, *assertions):
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
            (_(q1, x_grater_than_zero), _(q1, x_grater_than_zero)),
        }
        expected_matches = {
            'participants': {'p1': 'p1', 'p2': 'p2'},
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

        add_message = Message('add', payload=[Int('x')])
        add_to_cart_message = Message('add_to_cart', payload=[Int('number')])

        expected_relation = {
            (p0, frozenset(), q0),
            (p1, frozenset({Int('number') > 0}), q1)
        }
        expected_matches = {
            'participants': {'client': 'consumer', 'shop': 'producer'},
            'messages': {str(add_to_cart_message): add_message},
            'variables': {'number': Int('x')}
        }

        relation, matches = cfsm_example_2_1.calculate_bisimulation_with(cfsm_example_2_2)

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_03_must_return_empty_relation_and_match_when_is_not_be_bisimilar_but_match(self):
        relation, matches = cfsm_example_3_1.calculate_bisimulation_with(cfsm_example_3_2)

        self.assertEqual(set(), relation)
        self.assertEqual({}, matches)


if __name__ == '__main__':
    unittest.main()
