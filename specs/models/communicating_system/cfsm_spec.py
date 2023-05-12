import unittest
from z3 import Int, BoolVal, String
from ...resources.cfsm.example_1 import cfsm as cfsm_example_1
from ...resources.cfsm.example_2 import cfsm_1 as cfsm_example_2_1, cfsm_2 as cfsm_example_2_2
from ...resources.cfsm.example_3 import cfsm_1 as cfsm_example_3_1, cfsm_2 as cfsm_example_3_2
from ...resources.cfsm.example_4 import cfsm_1 as cfsm_example_4_1, cfsm_2 as cfsm_example_4_2
from ...resources.cfsm.example_5 import cfsm_1 as cfsm_example_5_1, cfsm_2 as cfsm_example_5_2
from ...resources.cfsm.example_6 import cfsm_1 as cfsm_example_6_1, cfsm_2 as cfsm_example_6_2
from ...resources.cfsm.example_7 import cfsm_1 as cfsm_example_7_1, cfsm_2 as cfsm_example_7_2
from ...resources.cfsm.example_8 import cfsm as cfsm_example_8
from models.communicating_system.action import Action
from models.assertable_finite_state_machines.assertion import Assertion
from models.stratified_bisimulation_strategies.knowledge import Knowledge
Message = Action.Message
x = Int('x')
number = Int('number')
true = BoolVal(True)


def _(state, *expressions):
    assertions = list(map(Assertion, expressions))
    return state, Knowledge(frozenset(assertions))


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
            'participants': {'Customer': 'Customer', 'Service': 'Service'},
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
            'participants': {'Consumer': 'Client', 'Producer': 'Shop'},
            'messages': {str(add_message): add_to_cart_message},
            'variables': {'x': number}
        }

        relation, matches = cfsm_example_2_1.calculate_bisimulation_with(cfsm_example_2_2, minimize=True)

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_03_must_return_empty_relation_and_match_when_is_not_bisimilar_but_match(self):
        relation, matches = cfsm_example_3_2.calculate_bisimulation_with(cfsm_example_3_1)

        expected_relation = set()
        expected_matches = {
            'participants': {'Client': 'Consumer'},
            'messages': {},
            'variables': {}
        }

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_04_must_match_and_be_bisimilar_when_split_a_transition_in_two(self):
        p0 = cfsm_example_4_1.states['p0']
        p1 = cfsm_example_4_1.states['p1']
        p2 = cfsm_example_4_1.states['p2']
        q0 = cfsm_example_4_2.states['q0']
        q1 = cfsm_example_4_2.states['q1']
        q2 = cfsm_example_4_2.states['q2']
        q3 = cfsm_example_4_2.states['q3']

        y = Int('y')
        amount = Int('amount')
        another_amount = Int('another_amount')

        add_message = Message('add', payload=[x])
        remove_message = Message('remove', payload=[y])
        deposit_message = Message('deposit', payload=[amount])
        withdraw_message = Message('withdraw', payload=[another_amount])

        expected_relation = {
            (_(p0), _(q0)),

            (_(p1, x != 0), _(q1, amount > 0)),
            (_(p2, x != 0, true), _(q3, amount > 0, true)),

            (_(p1, x != 0), _(q2, amount < 0)),
            (_(p2, x != 0, true), _(q3, amount < 0, true)),
        }
        expected_matches = {
            'participants': {'Consumer': 'Client', 'Adder': 'Wallet', 'Remover': 'Bank'},
            'messages': {
                str(add_message): deposit_message,
                str(remove_message): withdraw_message
            },
            'variables': {'x': amount, 'y': another_amount}
        }

        relation, matches = cfsm_example_4_1.calculate_bisimulation_with(cfsm_example_4_2, minimize=False)

        self.assertIsSubset(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_05_must_return_empty_relation_and_match_when_is_not_bisimilar_cause_not_match(self):
        relation, matches = cfsm_example_5_2.calculate_bisimulation_with(cfsm_example_5_1)

        expected_relation = set()
        expected_matches = {
            'participants': {'Client': 'Consumer'},
            'messages': {},
            'variables': {}
        }

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_06_must_not_be_bisimilar(self):
        relation, matches = cfsm_example_6_1.calculate_bisimulation_with(cfsm_example_6_2)

        expected_relation = set()
        expected_matches = {
            'participants': {'Consumer': 'Consumer'},
            'messages': {},
            'variables': {}
        }

        self.assertEqual(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_07_must_match_and_be_bisimilar(self):
        p0 = cfsm_example_7_1.states['p0']
        p1 = cfsm_example_7_1.states['p1']
        p2 = cfsm_example_7_1.states['p2']
        q0 = cfsm_example_7_2.states['q0']
        q1 = cfsm_example_7_2.states['q1']
        q2 = cfsm_example_7_2.states['q2']
        q3 = cfsm_example_7_2.states['q3']

        user = String('user')
        username = String('username')

        login_msg_user = Message('login', payload=[user])
        login_msg_username = Message('login', payload=[username])
        success_msg = Message('success')
        signup_msg = Message('signUp')
        ok_msg = Message('ok')
        signoff_msg = Message('signOff')

        expected_relation = {
            (_(p0), _(q0)),
            (_(p1), _(q1)),

            (_(p2, user == 'root'), _(q2, username == 'root')),
            (_(p0, user == 'root'), _(q0, username == 'root')),

            (_(p2, user == 'user'), _(q3, username == 'user')),
            (_(p0, user == 'user'), _(q0, username == 'user'))
        }
        expected_matches = {
            'participants': {'Client': 'Client', 'Service': 'Db'},
            'messages': {
                str(login_msg_user): login_msg_username,
                str(success_msg): ok_msg,
                str(signup_msg): signoff_msg
            },
            'variables': {'user': username}
        }

        relation, matches = cfsm_example_7_1.calculate_bisimulation_with(cfsm_example_7_2, minimize=False)

        self.assertIsSubset(expected_relation, relation)
        self.assertEqual(expected_matches, matches)

    def test_08(self):
        q0 = cfsm_example_8.states['q0']
        q1 = cfsm_example_8.states['q1']
        q2 = cfsm_example_8.states['q2']
        q3 = cfsm_example_8.states['q3']
        q4 = cfsm_example_8.states['q4']
        y = Int('y')
        f_x = Message('f', [x])
        g_y = Message('g', [y])
        m1 = Message('m1')
        m2 = Message('m2')

        expected_relation = {
            (_(q0), _(q0)),
            (_(q1), _(q1)),
            (_(q1, y > 0, x > 0), _(q1, y > 0, x > 0)),
            (_(q2, y > 0, x > 0), _(q2, y > 0, x > 0)),
            (_(q3, y <= 0), _(q3, y <= 0)),
            (_(q3, y <= 0, x > 0), _(q3, y <= 0, x > 0)),
            (_(q4, y <= 0), _(q4, y <= 0)),
            (_(q4, y <= 0, x > 0), _(q4, y <= 0, x > 0)),
        }

        expected_matches = {
            'participants': {'A1': 'A1', 'A2': 'A2'},
            'messages': {
                str(f_x): f_x,
                str(g_y): g_y,
                str(m1): m1,
                str(m2): m2
            },
            'variables': {'x': x, 'y': y}
        }

        relation, matches = cfsm_example_8.calculate_bisimulation_with(cfsm_example_8)
        self.assertIsSubset(expected_relation, relation)
        self.assertEqual(expected_matches, matches)


if __name__ == '__main__':
    unittest.main()
