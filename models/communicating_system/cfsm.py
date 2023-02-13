from models.afsm import AFSM
from libs.tools import TrueAssertion
from models.communicating_system.interaction_parser import InteractionParser


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

    def transitions_with_label_of(self, id, label):
        return set(filter(lambda transition: transition.label == label, self.transitions_of(id)))

    # TODO: Cambiar este metodo para que sea el que no espera que los labels sean iguales.
    def build_bisimulation_with(self, cfsm):
        # TODO: Me parece que aca, voy a tener que hacer una re-construccion de cfsm.
        #  Una primera idea es generar todos los matches posibles.
        #   es decir, genero una tabla de equivalencias
        #   Primero valido si existe algun matchin posible:
        #       - que la cantidad de participantes sea igual,       (match de participantes)
        #       - que la cantidad de tags sea igual                 (match de tags)
        #       - que las aridades entre tags iguales, sea igual    (match de variables)
        #   El paso sencillo a partir de validar que existe un match,
        #   Segundo, tendria que generar todos los matches posibles,
        #   porque me parece que si pruebo matches que no tienen sentido me puede llegar a armar una bisimulacion
        #   que no tiene ningun sentido.
        #   Tercero, generar un nuevo cfsm a partir de los matches, probar e ir haciendo backtracking.

        # puede haber mas de un matching valido? (creo que si). ej:
        # q0 -> g1 -> q1 -> g2 -> q1
        # p0 -> f1 -> p1 -> f2 -> p1
        return super().build_bisimulation_with(cfsm)
