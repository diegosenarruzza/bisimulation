# Para hacer la bisimulacion que estoy buscando tengo que poder incorporar 2 cosas:
  # Buscar en algun subconjunto de las transiciones salientes con el label correspondiente
  # Incorporar la nocion de conocimiento junto con la posibilidad de validar las implicaciones (cosa que por ahora asumimos con z-solver)

# necesito agregarle una dimension mas para poder tener el conocimiento, al armar la aproximacion inicial.
#------------

def are_bisimilars(M1, M2):
  return len(bisimulation(M1, M2)) > 0

def bisimulation(M1, M2):
  assertions = assertions_of([M1, M2])
  all_posible_knwoledge = parts_of(assertions)

  # si puedo prunear "all_posible_knowledge" esto se vuelve mas factible

  current_approximation = []
  next_approximation = M1.states.product(all_posible_knwoledge).product(M2.states)

  while current_approximation != next_approximation:
    current_approximation = next_approximation
    next_approximation = []

    for (e, K, f) in current_approximation:

      # si e puede imitar a f y f puede imitar a e (cayendo siempre dentro de la current_approximation) entonces tienen que estar en la siguiente aprox.
        # simetric en True porque va a ir a comprobar que exista (_e, _f) en la relacion en lugar de (_f, _e)
      if is_able_to_simulate_falling_into(e, f, K, current_approximation) and is_able_to_simulate_falling_into(f, e, K, current_approximation, simetric=True):
        next_approximation.append((e, f))


  return current_approximation + simetric(current_approximation)


def is_able_to_simulate_falling_into(state, simulation_state, knowledge, approximation, simetric=False):
  is_able = True
  transitions = state.get_transitions()
  i = 0

  # Si corta porque no cumple is_able, entonces es porque existe una accion que f no puede simular, o que puede pero no cae en la relacion
  # Si corta porque i < len(transitions) entonces recorrio todas las acciones y f siempre pudo simular a e y caer dentro de la relacion
  while is_able and i < len(transitions):
    transition = transitions[i]
    label = transition_from_e.label()

    cleaned_knowledge = clean_knowledge_for(knowledge, label)
    simulation_transitions = simulation_state.get_transitions_with(label)

    # Necesito verificar si existe algun subconjunto de transiciones desde "simulation_state", que me sirva para simular la transicion de "state"
    # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "state"
    # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

    is_able = exists_a_valid_transition_subset_wich_simulate(transition, simulation_transitions, cleaned_knowledge, approximation, simetric)
    # is_able es False si  el "simulation_state" no puede imitar la transicion "transition"

    i++

  return is_able


def exists_a_valid_transition_subset_wich_simulate(transition, simulation_transitions, knowledge, approximation, simetric):
  label = transition.label()
  assertion = transition.assertion()

  # No tomo el subconjunto vacio porque no seria valido. Si no hay mas conjuntos que el vacio, entonces nunca entra al loop y devuelve False
  simulation_transitions_subsets = parts_of(simulation_transitions, empty_set=False)

  valid_transitions_set_exists = False
  j = 0

  while (not valid_transitions_set_exists) and j < len(simulation_transitions_subsets):
    simulation_transitions_subset = simulation_transitions_subsets[j]

    simulation_assertions = (map lambda transition: transition.assertion, simulation_transitions_subset)

    logic_form_builder = LogicFormsBuilder.new()

    transition_knowledge = logic_form_builder.conjunction_of(knowledge + assertion)
    simulation_transition_knowledge = logic_form_builder.conjunction_of(knowledge).and(logic_form_builder.disjunction_of(simulation_assertions))
    implication = transition_knowledge.implies(simulation_transition_knowledge)

    # si encontre un sub-conjunto de transiciones, cuya implicacion es satisfacible y ademas cae dentro de la aproximacion, entonces es valido
    valid_transition_set_exists = implication.build().is_satisfiable() and transitions_subset_fall_into_approximation(transition, simulation_transitions_subset, knowledge, approximation, simetric)

    j++

  return valid_transitions_set_exists


def transitions_subset_fall_into_approximation(transition, simulation_transitions_subset, knowledge, approximation, simetric):
  target_state = transition.target()

  fall_into_approximation = True
  k = 0

  # me fijo si todas las transiciones del sub-conjunto caen dentro de la aproximacion que me pasaron por parametro
  while fall_into_approximation and k < len(simulation_transition_subset):
    simulation_transition = simulation_transition_subset[k]

    # calculo el nuevo conocimiento
    new_knowledge = knowledge + [transition.assertion, simulation_transition.assertion]
    target_simulation_state = simulation_transition.target()

    related_element = (target_simulation_state, new_knowledge, state) if simetric else (state, new_knowledge, target_simulation_state)

    fall_into_approximation = related_element in approximation

    k++

  return fall_into_approximation
