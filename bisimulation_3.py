M1 = FSM.new(E, p0, L, T1)
M2 = FSM.new(F, q0, L, T2)


# esta instanciacion es solo por el orden de ejecucion
current_approximation = []
next_approximation = E.product(F) # guardo solo un lado de la relacion


def is_able_to_simulate_falling_into(e, f, approximation, simetric=False):
  is_able = True
  actions = e.get_actions()
  i = 0

  # Si corta porque no cumple is_able, entonces es porque existe una accion que f no puede simular, o que puede pero no cae en la relacion
  # Si corta porque i < len(actions) entonces recorrio todas las acciones y f siempre pudo simular a e y caer dentro de la relacion
  while is_able and i < len(actions):
    a = actions[i]

    # si puede simular la accion
    if f.has_transition_with(a):
      _e = e.get_state_through(a)
      _f = f.get_state_through(a)

      related_element = (_f, _e) if simetric else (_e, _f)

      # si el elemento relacionado esta en la aproximacion, entonces f puede simular a e mediante la accion "a".
      is_able = related_element in approximation

    else:
      # si existe una accion en f que e no puede simular, entonces e no puede imitar a f directamente.
      is_able = False

    i++

  return is_able

while current_approximation != next_approximation
  current_approximation = next_approximation
  next_approximation = []

  for (e, f) in current_approximation:

    # si e puede imitar a f y f puede imitar a e (cayendo siempre dentro de la current_approximation) entonces tienen que estar en la siguiente aprox.
      # simetric en True porque va a ir a comprobar que exista (_e, _f) en la relacion en lugar de (_f, _e)
    if is_able_to_simulate_falling_into(e, f, current_approximation) and is_able_to_simulate_falling_into(f, e, current_approximation, simetric=True):
      next_approximation.append((e, f))


# si current_approximation y next_approximation son iguales, se llego al punto fijo.

return current_approximation + simetric(current_approximation)