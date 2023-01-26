from models.state import State
from models.transition import Transition
from models.tools import powerset

from itertools import product

class AFSM:

  def __init__(self):
    self.states = {}
    self.transitions_by_source_id = {}

  def add_state(self, id):
    # validate not p resent
    self.states[id] = State(self, id)
    self.transitions_by_source_id[id] = []

  # assertion must to be a z3 assertion
  def add_transition_between(self, source_id, target_id, label, assertion):
    # validate present
    # validate transition not exist

    source = self.states[source_id]
    target = self.states[target_id]

    transition = Transition(source, target, label, assertion) 

    self.transitions_by_source_id[source_id].append(transition)
  
  def transitions_of(self, id):
    #  validate present
    return self.transitions_by_source_id[id]

  def transitions_with_label_of(self, id, label):
    return filter(lambda transition: transition.label == label, self.transitions_of(id))

  def all_assertions(self):
    return map(lambda transition: transition.assertion, self.transitions_by_source_id.values())

  def get_states(self):
    return self.states.values()

  # Hay que tener cuidado con el hecho de que los automatas tienen que tener distintos ids
  # Depende de como definamos la igualdad de State.
  # Se esta asumiendo que tanto "self", como "afsm" son validos, i.e. que cumplen con lo que cumple un cfsm que son los que estamos usando de base.
  def try_bisimulation_with(self, afsm):
    assertions = list(set(self.all_assertions + afsm.all_assertions))

    all_posible_knowledge = powerset(assertions)

    current_approximation = []
    symmetric_current_approximation = []
    # TODO: Hacer notar que nunca va a haber un problema con el orden en el que se genera el conocimiento.
    next_approximation = product([self.get_states(), all_posible_knowledge, afsm.get_states()])

    while current_approximation != next_approximation:
      current_approximation = next_approximation
      symmetric_current_approximation = [tuple(reversed(t)) for t in current_approximation]
      next_approximation = []

      for (e, K, f) in current_approximation:
        knowledge = set(K)
        # si e puede imitar a f y f puede imitar a e (cayendo siempre dentro de la current_approximation) entonces tienen que estar en la siguiente aprox.
        # simetric en True porque va a ir a comprobar que exista (_e, _f) en la relacion en lugar de (_f, _e)
        if e.is_able_to_simulate_falling_into(f, knowledge, current_approximation) and f.is_able_to_simulate_falling_into(e, knowledge, symmetric_current_approximation):
          next_approximation.append((e, K, f))

    return current_approximation + symmetric_current_approximation