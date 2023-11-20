from .decision import NoDecision


class Decider:

    def __init__(self, symmetry_mode):
        self.decisions = [NoDecision(symmetry_mode)]
        self.symmetry_mode = symmetry_mode

    def take(self, decision):
        decision.decide()
        self.decisions.append(decision)

    def take_next_decision(self):
        if self.there_are_decisions_to_take():
            last_decision = self.decisions.pop()
            # Seteo el modo simetrico al que habia cuando se tomo la decision.
            # Esto es necesario para que se agreguen y eliminen los candidatos en las collecciones correspondientes.
            self.symmetry_mode.work_as(last_decision.symmetry_mode_when_match)

            # Hace rollback para "devolver" el candidato que saco cuando tomo la decision.
            last_decision.rollback()

            # Si todavia tiene candidatos:
            #   - Hago un rollback, lo que me deja el matcher como si no hubiese tomado esa decision,
            #   - Le digo que vuelva a decidir, porque su lista de candidatos no es vacia, y tiene un elemento menos de la que uso para empezar (porque cuando decide, popea)
            #   - Vuelvo a pushear la decision, con la lista de candidatos mas corta
            if last_decision.has_more_candidates():
                self.take(last_decision)
            else:
                # Si no tiene mas candidatos, la ultima decision ya no me sirve. Entonces sigo con la decision anterior.
                self.take_next_decision()

    def there_are_decisions_to_take(self):
        return len(self.decisions) > 0

    def __str__(self):
        return str(self.decisions)

    def __repr__(self):
        string = '[ \n'
        for decision in self.decisions:
            string += f'  {decision}\n'
        string += ']'
        return string
