from .messages_matcher import match_messages
from .participants_matcher import match_participants

# fijo cfsm1
def match(cfsm1, cfsm2):
    matches = []
    participants_1 = cfsm1.participants
    participants_2 = cfsm2.participants

    interactions_1 = cfsm1.interactions()
    interactions_2 = cfsm2.interactions()

    messages_1 = list(map(lambda interaction: interaction.message, interactions_1))
    messages_2 = list(map(lambda interaction: interaction.message, interactions_2))

    # Si no hay la misma cantidad de participantes, interacciones o mensajes, entonces no puede haber matching
    if len(participants_1) != len(participants_2) or \
            len(interactions_1) != len(interactions_2) or \
            len(messages_1) != len(messages_2):
        return matches

    message_matches = match_messages(messages_1, messages_2)

    # Si no se consigue un matching de mensajes, entonces no puede haber match entre los automatas
    if len(message_matches) == 0:
        return matches

    participant_matches = match_participants(participants_1, participants_2)

    # TODO: iterar uno, iterar el otro, intentar matchear las interacciones a partir de convinar ambos.


