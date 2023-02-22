import unittest
from models.communicating_system.matchers.participant_matcher import ParticipantMatcher
from models.communicating_system.matchers.message_matcher import MessageMatcher
from models.communicating_system.matchers.decider import Decider
from models.communicating_system.interaction import Interaction
Message = Interaction.Message


class MessagesMatcherTestCase(unittest.TestCase):

    def test_01_must_match_messages(self):
        decider = Decider()
        interaction_candidates = [Interaction('p1', 'p2', Message('m1')), Interaction('p1', 'p3', Message('m2'))]
        message_candidates = [interaction.message for interaction in interaction_candidates]
        participant_candidates = ['p1', 'p2', 'p3']

        participant_matcher = ParticipantMatcher(decider, participant_candidates)
        matcher = MessageMatcher(decider, message_candidates, interaction_candidates, participant_matcher)

        matchable_interaction_1 = Interaction('c1', 'c2', Message('n1'))
        matchable_interaction_2 = Interaction('c1', 'c3', Message('n2'))

        participant_matcher.match(matchable_interaction_1)
        participant_matcher.match(matchable_interaction_2)

        matched_message_n1 = matcher.match(matchable_interaction_1)
        matched_message_n2 = matcher.match(matchable_interaction_2)

        self.assertNotEqual(matched_message_n1, matched_message_n2)
        self.assertIn(matched_message_n1, message_candidates)
        self.assertIn(matched_message_n2, message_candidates)

    def test_02_must_respect_matches(self):
        decider = Decider()
        interaction_candidates = [
            Interaction('p1', 'p2', Message('m2')),
            Interaction('p1', 'p3', Message('m2')),
            Interaction('p1', 'p2', Message('m1'))
        ]
        message_candidates = [Message('m2'), Message('m1')]
        participant_candidates = ['p1', 'p2', 'p3']

        participant_matcher = ParticipantMatcher(decider, participant_candidates)
        matcher = MessageMatcher(decider, message_candidates, interaction_candidates, participant_matcher)

        matchable_interaction_1 = Interaction('c1', 'c2', Message('n2'))
        matchable_interaction_2 = Interaction('c1', 'c3', Message('n2'))
        matchable_interaction_3 = Interaction('c1', 'c2', Message('n1'))

        participant_matcher.match(matchable_interaction_1)
        participant_matcher.match(matchable_interaction_2)

        old_matched_message_n2 = matcher.match(matchable_interaction_1)
        new_matched_message_n2 = matcher.match(matchable_interaction_2)
        matched_message_n1 = matcher.match(matchable_interaction_3)

        self.assertEqual(old_matched_message_n2, new_matched_message_n2)
        self.assertNotEqual(matched_message_n1, new_matched_message_n2)

    def test_03_rollback_last_decision_must_take_new_candidate(self):
        decider = Decider()
        interaction_candidates = [
            Interaction('p1', 'p2', Message('m1')),
            Interaction('p1', 'p2', Message('m2'))
        ]
        message_candidates = [Message('m1'), Message('m2')]
        participant_candidates = ['p1', 'p2']

        participant_matcher = ParticipantMatcher(decider, participant_candidates)
        matcher = MessageMatcher(decider, message_candidates, interaction_candidates, participant_matcher)

        matchable_interaction = Interaction('c1', 'c2', Message('n1'))

        participant_matcher.match(matchable_interaction)

        old_message = matcher.match(matchable_interaction)
        self.assertEqual([Message('m2')], matcher.candidates)

        decider.next()
        new_message = matcher.match(matchable_interaction)

        self.assertNotEqual(new_message, old_message)
        self.assertEqual([Message('m1')], matcher.candidates)


if __name__ == '__main__':
    unittest.main()
