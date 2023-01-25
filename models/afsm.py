from state import State
from transition import Transition
from itertools import product
from tools import powerset

class AFSM:

  def __init__(self):
    self.states = {}
    self.transitions_by_source_id = {}

  def add_state(self, id):
    # validate not p resent
    self.states[id] = State.new(self, id)
    self.transitions_by_source_id[id] = []

  # TODO: Voy a necesitar que las assertions sean algo mas, cosa de poder acceder a ellas como "logica" y como string.
  def add_transition_between(self, source_id, target_id, label, assertion):
    # validate present
    # validate transition not exist

    source = self.states[source_id]
    target = self.states[target_id]

    transition = Transition.new(source, target, label, assertion) 

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
  def try_bisimulation_with(self, afsm):
    assertions = list(set(self.all_assertions + afsm.all_assertions))

    all_posible_knowledge = powerset(assertions)

    current_approximation = []
    symmetric_current_approximation = []
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