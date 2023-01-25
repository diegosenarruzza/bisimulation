from models.tools import powerset
from z3 import Solver, sat, And, Or, Implies

class Transition:

  def __init__(self, source, target, label, assertion):
    self.source = source
    self.target = target
    self.label = label
    self.assertion = assertion

  def exists_a_valid_transition_subset_wich_simulate(self, simulation_transitions, knowledge, approximation):
    # No tomo el subconjunto vacio porque no seria valido. Si no hay mas conjuntos que el vacio, entonces nunca entra al loop y devuelve False
    simulation_transitions_subsets = list(powerset(simulation_transitions))
    simulation_transitions_subsets.remove(())

    valid_transitions_set_exists = False
    j = 0

    while (not valid_transitions_set_exists) and j < len(simulation_transitions_subsets):
      simulation_transitions_subset = list(simulation_transitions_subsets[j])

      # si encontre un sub-conjunto de transiciones, cuya implicacion es satisfacible y ademas cae dentro de la aproximacion, entonces es valido 
      valid_transitions_set_exists = self._is_able_to_simule_knowledge(knowledge, simulation_transitions_subset) and \
                                     self.transitions_subset_fall_into_approximation(simulation_transitions_subset, knowledge, approximation)

      j += 1

    return valid_transitions_set_exists


  def transitions_subset_fall_into_approximation(self, simulation_transitions_subset, knowledge, approximation):
    fall_into_approximation = True
    k = 0

    # me fijo si todas las transiciones del sub-conjunto caen dentro de la aproximacion que me pasaron por parametro
    while fall_into_approximation and k < len(simulation_transitions_subset):
      simulation_transition = simulation_transitions_subset[k]

      # calculo el nuevo conocimiento
      new_knowledge  = set([self.assertion, simulation_transition.assertion])

      fall_into_approximation = (self.target, knowledge.union(new_knowledge), simulation_transition.target) in approximation

      k += 1

    return fall_into_approximation


  # Usamos z3-prover. Las assertions tienen que estar escritas con este framework.
  def _is_able_to_simule_knowledge(self, knowledge, simulation_transitions_subset):
    simulation_assertions = map(lambda transition: transition.assertion, simulation_transitions_subset)

    transition_knowledge = And(knowledge + self.assertion)
    simulation_transition_knowledge = And(knowledge + Or(simulation_assertions))

    solver = Solver()

    return solver.check(Implies(transition_knowledge, simulation_transition_knowledge)) == sat