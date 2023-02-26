from .matcher import Matcher


# VariableMatcher no toma decisiones, solo guarda las variables decididas por el message matcher
class VariableMatcher(Matcher):

    def decide_match(self, matched_message, candidate_message):
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            if not self.match_manager.has_matched(matched_variable):
                self.match_manager.match(matched_variable, candidate_variable)

    # Si "desmatcheo" un mensaje, las variables que habia en ese mensaje tiene que ser desmatcheadas tambien.
    def rollback_match(self, matched_message, candidate_message):
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            self.match_manager.unmatch(matched_variable, candidate_variable)

    def serialize(self):
        return {
            'variables': self.match_manager.serialize()
        }
