import unittest
from models.communicating_system.matchers.interaction_matcher import InteractionMatcher
from models.communicating_system.interaction import Interaction
Message = Interaction.Message


class InteractionMatcherTestCase(unittest.TestCase):

    def test_01_must_match_interaction(self):
        interaction_candidates = [Interaction('p1', 'p2', Message('m1')), Interaction('p1', 'p3', Message('m2'))]
        participant_candidates = ['p1', 'p2', 'p3']
        message_candidates = [Message('m1'), Message('m2')]

        matchable_interaction_1 = Interaction('c1', 'c2', Message('n1'))
        matchable_interaction_2 = Interaction('c1', 'c3', Message('n2'))

        matcher = InteractionMatcher(interaction_candidates, participant_candidates, message_candidates)

        matched_interaction_1 = matcher.match(matchable_interaction_1)
        matched_interaction_2 = matcher.match(matchable_interaction_2)

        self.assertNotEqual(matched_interaction_2, matched_interaction_1)
        self.assertIn(matched_interaction_1, interaction_candidates)
        self.assertIn(matched_interaction_2, interaction_candidates)

    def test_02_must_respect_matches(self):
        interaction_candidates = [
            Interaction('p1', 'p2', Message('m1')),
            Interaction('p2', 'p1', Message('m1'))
        ]
        participant_candidates = ['p1', 'p2']
        message_candidates = [Message('m1'), Message('m2')]

        matchable_interaction_1 = Interaction('c1', 'c2', Message('n1'))
        matchable_interaction_2 = Interaction('c2', 'c1', Message('n1'))

        matcher = InteractionMatcher(interaction_candidates, participant_candidates, message_candidates)

        matched_interaction_1 = matcher.match(matchable_interaction_1)
        matched_interaction_2 = matcher.match(matchable_interaction_2)

        self.assertEqual(matched_interaction_2.message, matched_interaction_1.message)
        self.assertEqual(matched_interaction_2.sender, matched_interaction_1.receiver)
        self.assertEqual(matched_interaction_2.receiver, matched_interaction_1.sender)

    def test_03_must_has_more_possibilities_when_match_next_if_it_has(self):
        interaction_candidates = [
            Interaction('p1', 'p2', Message('m1')),
            Interaction('p2', 'p1', Message('m1'))
        ]
        participant_candidates = ['p1', 'p2']
        message_candidates = [Message('m1'), Message('m2')]

        matchable_interaction = Interaction('c1', 'c2', Message('n1'))

        matcher = InteractionMatcher(interaction_candidates, participant_candidates, message_candidates)

        matcher.match(matchable_interaction)
        self.assertTrue(matcher.has_more_possible_matches())

        matcher.match_next()
        self.assertTrue(matcher.has_more_possible_matches())


if __name__ == '__main__':
    unittest.main()
