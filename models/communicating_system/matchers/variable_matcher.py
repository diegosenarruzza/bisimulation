# VariableMatcher no toma decisiones, solo guarda las variables decididas por el message matcher
class VariableMatcher:

    def __init__(self):
        self.matches = {}

    # Se asume que una variable no puede aparecer en dos mensajes iguales.
    # ej: no puede haber [f(int x, int y), f(int x, int z)]
    # Tampoco puede pasar que dos mensajes distintos usen una misma variable.
    # ej: no puede haber [f(int x), g(int x)]
    def decide_match(self, matched_message, candidate_message):
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            if matched_variable not in self.matches:
                self.matches[matched_variable] = candidate_variable

    # Si "desmatcheo" un mensaje, las variables que habia en ese mensaje tiene que ser desmatcheadas tambien.
    def rollback_match(self, matched_message, candidate_message):
        for matched_variable in matched_message.payload:
            del self.matches[matched_variable]

    def serialize(self):
        return {
            'variable_matches': self.matches
        }
