from models.afsm import AFSM
from libs.tools import TrueAssertion
from .interaction_parser import InteractionParser
from models.stratified_bisimulation_strategies.non_shared_language_strategy import NonSharedLanguageBisimulationStrategy


class CommunicatingFiniteStateMachine(AFSM):

    def __init__(self, participants):
        # TODO: Verify are not repeated
        self.participants = participants
        super().__init__()

    def add_transition_between(self, source_id, target_id, interaction_string, assertion=TrueAssertion):
        interaction = self._parse_interaction(interaction_string)
        # validate interaction participants are in participant_ids

        super().add_transition_between(source_id, target_id, interaction, assertion)

    @staticmethod
    def _parse_interaction(interaction_string):
        return InteractionParser().parse(interaction_string)

    def interactions(self):
        return set(
            transition for transitions in list(self.transitions_by_source_id.values()) for transition in transitions
        )

    def _bisimulation_strategy_with(self, cfsm):
        return NonSharedLanguageBisimulationStrategy(self, cfsm)
