from ..assertable_finite_state_machines.afsm import AFSM
from ...libs.tools import TrueFormula
from .action_parser import ActionParser
from ..stratified_bisimulation_strategies.non_shared_language_strategy.bisimulation import NonSharedLanguageBisimulationStrategy
from .factories.matcher_factory import MatcherFactory


class CommunicatingFiniteStateMachine(AFSM):

    def __init__(self, participants):
        # TODO: Verify are not repeated
        self.main_participant, *self.participants = participants
        super().__init__()

    def __repr__(self):
        return str(self)

    def __str__(self):
        string = ''
        for source_id, transitions in self.transitions_by_source_id.items():
            if self.initial_state is not  None and self.initial_state.id == source_id:
                string += f'-> {source_id}: [\n'
            else:
                string += f'{source_id}: [\n'

            for transition in transitions:
                string += f'  {transition},\n'
            string += ']\n'
        return string

    def set_as_initial(self, state_id):
        if state_id not in self.states:
            self.add_state(state_id)
        self.initial_state = self.states[state_id]

    def add_transition_between(self, source_id, target_id, action_string, formula=TrueFormula):
        if source_id not in self.states:
            self.add_state(source_id)
        if target_id not in self.states:
            self.add_state(target_id)

        action = self._parse_action(action_string)
        # validate action participants are ine participant_ids

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
        return [transition.label for transition in self.all_transitions()]

    def messages(self):
        return {transition.label.message for transition in self.all_transitions()}

    def get_participants(self):
        return [participant for participant in self.participants]

    def _matcher_factory_with(self, cfsm):
        return MatcherFactory(self, cfsm)
