import unittest
from z3 import Int, BoolVal
from models.communicating_system.interaction import Interaction
from ...resources.cfsm.example_1 import cfsm as cfsm_example_1
from ...resources.cfsm.example_2 import cfsm_1 as cfsm_example_2_1, cfsm_2 as cfsm_example_2_2
Message = Interaction.Message


class CFSMTestCase(unittest.TestCase):

    def test_01_must_match_and_be_bisimilar_and_match_with_itself(self):
        q0 = cfsm_example_1.states['q0']
        q1 = cfsm_example_1.states['q1']
        f_x = Message('f', payload=[Int('x')])

        expected_relation = {
            (q0, frozenset(), q0),
            (q1, frozenset({Int('x') > 0}), q1),
        }

        expected_matches = {
            'participant': {'p1': 'p1', 'p2': 'p2'},
            'message': {str(f_x): f_x},
            'variable': {Int('x'): Int('x')}
        }

        relation, matches = cfsm_example_1.calculate_bisimulation_with(cfsm_example_1)

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
            (p1, frozenset({Int('x') > 0}), q1)
        }
        expected_matches = {
            'participants_matches': {'client': 'consumer', 'shop': 'producer'},
            'messages_matches': {str(add_to_cart_message): add_message},
            'variable_matches': {Int('number'): Int('x')}
        }

        relation, matches = cfsm_example_2_1.calculate_bisimulation_with(cfsm_example_2_2)

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)


if __name__ == '__main__':
    unittest.main()
