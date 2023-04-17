from libs.z3_renamer import rename_variables
from models.assertable_finite_state_machines.assertion import Assertion
from .matcher import Matcher


# VariableMatcher no toma decisiones, solo guarda las variables decididas por el message matcher
class VariableMatcher(Matcher):

    def match_assertion(self, assertion):
        renamed_expression = rename_variables(assertion.expression, self._string_matches())
        return Assertion(renamed_expression)

    def decide(self, decision):
        matched_message = decision.matched
        candidate_message = decision.current_candidate
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            if not self.match_manager.has_matched(matched_variable):
                self.match_manager.match(matched_variable, candidate_variable)

    # Si "desmatcheo" un mensaje, las variables que habia en ese mensaje tienen que ser desmatcheadas tambien.
    def rollback(self, decision):
        matched_message = decision.matched
        candidate_message = decision.current_candidate
        for matched_variable, candidate_variable in zip(matched_message.payload, candidate_message.payload):
            self.match_manager.unmatch(matched_variable, candidate_variable)

    def serialize(self):
        return {
            'variables': self.match_manager.serialize()
        }

    def _string_matches(self):
        string_matches = {}
        for matched, matching in self.match_manager.copy().items():
            string_matches[matched] = str(matching)

        return string_matches
