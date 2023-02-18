from .interaction import Interaction


class Matcher:

    def __init__(self, participant_candidates, message_candidates):
        self.decisions = []
        self.participant_candidates = participant_candidates
        self.message_candidates = message_candidates
        # listas sin repetidos. porque un mensaje se puede haber mandado n veces de la misma manera (con las mismas variables, si son distintos caminos vale)

        self.participants_match = {}
        self.messages_match = {}

    def is_able_to_take_more_decisions(self):
        return len(self.participant_candidates) > 0 or len(self.message_candidates) > 0

    # TODO: no tengo que asumir nada, y si no encuentro match posible esto tiene que tirar una excepcion.
    # Despues lo voy a necesitar para traducir al momento de usar el z3solver igualmente.
    def match_interaction(self, interaction):
        matched_sender = self.match_participant(interaction.sender)
        matched_receiver = self.match_participant(interaction.receiver)
        matched_message = self.match_message(interaction)

        return Interaction(matched_sender, matched_receiver, matched_message)

    def match_participant(self, participant_id):
        if participant_id not in self.participants_match:
            participant_decision = self.ParticipantDecision(participant_id, self.participant_candidates)    # TODO: Ver si esto le guarda una copia, o exactamente el mismo
            self.take_decision(participant_decision)

        return self.participants_match[participant_id]

    def match_message(self, interaction):
        message_hash = str(interaction.message)
        if message_hash not in self.messages_match:
            message_decision = self.MessageDecision(interaction.message, self.get_message_candidates_for(interaction))
            self.take_decision(message_decision)

        return self.messages_match[message_hash]

    def get_message_candidates_for(self, interaction):
        return [message_candidate for message_candidate in self.message_candidates if self.message_candidate_is_available_for(message_candidate, interaction)]

    def message_candidate_is_available_for(self, message_candidate, interaction):
        matched_sender = self.match_participant(interaction.sender)
        matched_receiver = self.match_participant(interaction.receiver)
        return message_candidate.sender == matched_sender and \
               message_candidate.receiver == matched_receiver and \
               message_candidate.payload_sort() == interaction.message.payload_sort()

    def rollback(self):
        if len(self.decisions) > 0:
            last_decision = self.decisions.pop()

            # Si todavia tiene candidatos:
            #   - Hago un rollback, lo que me deja el matcher como si no hubiese tomado esa decision,
            #   - Le digo que vuelva a decidir, porque su lista de candidatos no es vacia, y tiene un elemento menos de la que uso para empezar (porque cuando decide, popea)
            #   - Vuelvo a pushear la decision, con la lista de candidatos mas corta
            if last_decision.has_more_candidates(self):
                last_decision.rollback_for(self)
                self.take_decision(last_decision)
            else:
                # Si no tiene mas candidatos, la ultima decision ya no me sirve. Entonces sigo con la decision anterior.
                self.rollback()

    def take_decision(self, decision):
        decision.decide_for(self)
        self.decisions.append(decision)

    def decide_participant_match(self, participant_id_matched, participant_id_match_candidate):
        self.participant_candidates.remove(participant_id_match_candidate)
        self.participants_match[participant_id_matched] = participant_id_match_candidate

    def rollback_participant_match(self, participant_id_matched, participant_id_match_candidate):
        self.participant_candidates.append(participant_id_match_candidate)
        del self.participants_match[participant_id_matched]

    def decide_message_match(self, message_matched, message_match_candidate):
        self.message_candidates.remove(message_match_candidate)
        self.messages_match[str(message_matched)] = message_match_candidate

    def rollback_message_match(self, message_matched, message_match_candidate):
        self.message_candidates.append(message_match_candidate)
        del self.messages_match[str(message_matched)]

    class Decision:

        def __init__(self, matched, match_candidates):
            self.matched = matched
            self.match_candidates = match_candidates
            self.current_match_candidate = None

        def has_more_candidates(self):
            return len(self.match_candidates) > 0

    class ParticipantDecision(Decision):

        def decide_for(self, matcher):
            self.current_match_candidate = self.match_candidates.pop(0)
            matcher.decide_participant_match(self.matched, self.current_match_candidate)

        def rollback_for(self, matcher):
            matcher.rollback_participant_match(self.matched, self.current_match_candidate)
            self.current_match_candidate = None

    class MessageDecision(Decision):

        def decide_for(self, matcher):
            self.current_match_candidate = self.match_candidates.pop(0)
            matcher.decide_message_match(self.matched, self.current_match_candidate)

        def rollback_for(self, matcher):
            matcher.rollback_message_match(self.matched, self.current_match_candidate)
            self.current_match_candidate = None
