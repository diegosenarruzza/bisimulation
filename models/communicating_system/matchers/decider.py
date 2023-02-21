class Decider:

    def __init__(self):
        self.decisions = []

    def take(self, decision):
        decision.decide()
        self.decisions.append(decision)

    def next(self):
        if len(self.decisions) > 0:
            last_decision = self.decisions.pop()

            # Si todavia tiene candidatos:
            #   - Hago un rollback, lo que me deja el matcher como si no hubiese tomado esa decision,
            #   - Le digo que vuelva a decidir, porque su lista de candidatos no es vacia, y tiene un elemento menos de la que uso para empezar (porque cuando decide, popea)
            #   - Vuelvo a pushear la decision, con la lista de candidatos mas corta
            if last_decision.has_more_candidates(self):
                last_decision.rollback(self)
                self.take(last_decision)
            else:
                # Si no tiene mas candidatos, la ultima decision ya no me sirve. Entonces sigo con la decision anterior.
                self.next()
