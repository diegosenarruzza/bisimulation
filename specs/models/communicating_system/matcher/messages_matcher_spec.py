import unittest
from models.communicating_system.matchers.messages_matcher import match_messages
from models.communicating_system.interaction import Interaction
from z3 import Int, Bool
Message = Interaction.Message


class MessageMatcher(unittest.TestCase):

    def test_1_must_match_one_to_one(self):
        mf = Message('f')
        mg = Message('g')

        expected_matches = [
            [(mf, mg)]
        ]
        matches = match_messages([mf], [mg])

        self.assertEqual(expected_matches, matches)

    def test_2_must_match_with_two_combinations(self):
        mf1 = Message('f1')
        mf2 = Message('f2')
        mg1 = Message('g1')
        mg2 = Message('g2')
        messages_collection_1 = [mf1, mf2]
        messages_collection_2 = [mg1, mg2]

        expected_matches = [
            [(mf1, mg1), (mf2, mg2)],
            [(mf1, mg2), (mf2, mg1)]
        ]
        matches = match_messages(messages_collection_1, messages_collection_2)

        self.assertEqual(expected_matches, matches)

    def test_3_must_match_with_three_combinations(self):
        mf1 = Message('f1')
        mf2 = Message('f2')
        mf3 = Message('f3')
        mg1 = Message('g1')
        mg2 = Message('g2')
        mg3 = Message('g3')
        messages_collection_1 = [mf1, mf2, mf3]
        messages_collection_2 = [mg1, mg2, mg3]

        expected_matches = [
            [(mf1, mg1), (mf2, mg2), (mf3, mg3)],
            [(mf1, mg1), (mf2, mg3), (mf3, mg2)],
            [(mf1, mg2), (mf2, mg1), (mf3, mg3)],
            [(mf1, mg2), (mf2, mg3), (mf3, mg1)],
            [(mf1, mg3), (mf2, mg1), (mf3, mg2)],
            [(mf1, mg3), (mf2, mg2), (mf3, mg1)]
        ]
        matches = match_messages(messages_collection_1, messages_collection_2)

        self.assertEqual(expected_matches, matches)

    def test_4_must_not_match_when_there_is_not_common_arity(self):
        mf1 = Message('f1', [Int('a')])
        mf2 = Message('f2', [Int('a'), Bool('b')])
        mg1 = Message('f2', [Int('x')])
        mg2 = Message('f2', [Bool('a'), Int('b')])
        messages_collection_1 = [mf1, mf2]
        messages_collection_2 = [mg1, mg2]

        matches = match_messages(messages_collection_1, messages_collection_2)

        self.assertEqual([], matches)

    def test_5_must_match_by_arity(self):
        mf1 = Message('f1', [Int('a')])
        mf2 = Message('f2', [Bool('b'), Int('c')])
        mg1 = Message('g1', [Bool('x'), Int('y')])
        mg2 = Message('g2', [Int('z')])
        messages_collection_1 = [mf1, mf2]
        messages_collection_2 = [mg1, mg2]

        expected_matches = [
            [(mf1, mg2), (mf2, mg1)]
        ]
        matches = match_messages(messages_collection_1, messages_collection_2)

        self.assertEqual(expected_matches, matches)


if __name__ == '__main__':
    unittest.main()
