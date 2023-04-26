from models.assertable_finite_state_machines.afsm import AFSM
from libs.tools import TrueFormula
from .action_parser import ActionParser
from models.stratified_bisimulation_strategies.non_shared_language_strategy.bisimulation import NonSharedLanguageBisimulationStrategy
from .factories.matcher_factory import MatcherFactory


class CommunicatingFiniteStateMachine(AFSM):

    def __init__(self, participants):
        # TODO: Verify are not repeated
        self.participants = participants
        super().__init__()

    def add_transition_between(self, source_id, target_id, action_string, formula=TrueFormula):
        action = self._parse_action(action_string)
        # validate action participants are in participant_ids

        super().add_transition_between(source_id, target_id, action, formula)

    @staticmethod
    def _parse_action(action_string):
        return ActionParser().parse(action_string)

    def _bisimulation_strategy_with(self, cfsm):
        return NonSharedLanguageBisimulationStrategy(
            self,
            cfsm,
            self._matcher_factory_with(cfsm).action_matcher()
        )

    def actions(self):
        return [transition.label for transition in self._all_transitions()]

    def messages(self):
        return {transition.label.message for transition in self._all_transitions()}

    def get_participants(self):
        return [participant for participant in self.participants]

    def _matcher_factory_with(self, cfsm):
        return MatcherFactory(self, cfsm)

    def actions_that_define(self, variables):
        actions = []
        for action in self.actions():
            if action.contains_any(variables):
                actions.append(action)
        return actions

    def transitions_that_define(self, variables):
        transitions = [transition for transition in self._all_transitions() if transition.label.contains_any(variables)]

        return transitions
