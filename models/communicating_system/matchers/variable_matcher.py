from .matcher import Matcher


# VariableMatcher no toma decisiones, solo guarda las variables decididas por el message matcher
class VariableMatcher(Matcher):

    # def __init__(self, decider, match_manager):
    #     self.decidier = decider
    #     self.match_manager = match_manager

    # Se asume que una variable no puede aparecer en dos mensajes iguales.
    # ej: no puede haber [f(int x, int y), f(int x, int z)]
    # Tampoco puede pasar que dos mensajes distintos usen una misma variable.
    # ej: no puede haber [f(int x), g(int x)]
    def decide_match(self, matched_message, candidate_message):
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            if not self.match_manager.has_matched(matched_variable):
                self.match_manager.match(matched_variable, candidate_variable)

    # Si "desmatcheo" un mensaje, las variables que habia en ese mensaje tiene que ser desmatcheadas tambien.
    def rollback_match(self, matched_message, candidate_message):
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            self.match_manager.unmatch(matched_variable, candidate_variable)
    #
    # def enable_symmetric_mode(self):
    #     self.match_manager.enable_symmetric_mode()
    #
    # def disable_symmetric_mode(self):
    #     self.match_manager.disable_symmetric_mode()

    def serialize(self):
        return {
            'variables': self.match_manager.serialize()
        }
