import unittest
from models.communicating_system.matchers.participant_matcher import ParticipantMatcher
from models.communicating_system.matchers.decider import Decider
from models.communicating_system.interaction import Interaction
Message = Interaction.Message


class ParticipantMatcherTestCase(unittest.TestCase):

    def test_01_must_match_participants(self):
        candidates = ['p1', 'p2', 'p3']
        matcher = ParticipantMatcher(Decider(), candidates)

        matched_sender, matched_receiver = matcher.match(Interaction('c1', 'c2', Message('m1')))

        self.assertNotEqual(matched_sender, matched_receiver)
        self.assertIn(matched_sender, candidates)
        self.assertIn(matched_receiver, candidates)
        self.assertTrue(matcher.has_more_candidates())

    def test_02_must_respect_matches(self):
        candidates = ['p1', 'p2', 'p3']
        matcher = ParticipantMatcher(Decider(), candidates)

        sender_1, receiver_1 = matcher.match(Interaction('c1', 'c2', Message('m1')))
        sender_2, receiver_2 = matcher.match(Interaction('c1', 'c3', Message('m1')))
        sender_3, receiver_3 = matcher.match(Interaction('c3', 'c1', Message('m1')))

        self.assertEqual(sender_1, sender_2)
        self.assertEqual(sender_1, receiver_3)
        self.assertEqual(receiver_2, sender_3)
        self.assertFalse(matcher.has_more_candidates())

    def test_03_rollback_last_decision_must_take_new_candidate(self):
        candidates = ['p1', 'p2', 'p3']
        decider = Decider()
        matcher = ParticipantMatcher(decider, candidates)
        interaction = Interaction('c1', 'c2', Message('m1'))

        old_sender, old_receiver = matcher.match(interaction)
        self.assertEqual(['p3'], matcher.candidates)

        decider.next()
        new_sender, new_receiver = matcher.match(interaction)

        self.assertEqual('p1', old_sender)
        self.assertEqual('p1', new_sender)
        self.assertEqual('p2', old_receiver)
        self.assertEqual('p3', new_receiver)
        self.assertEqual(['p2'], matcher.candidates)


if __name__ == '__main__':
    unittest.main()
