M1 = FSM.new(P, p0, L, T1)
M2 = FSM.new(Q, q0, L, T2)

# propuesta 2, un poco mas chica

# esta instanciacion es solo por el orden de ejecucion
current_approximation = []
next_approximation = M1.states.product(M2.states) # guardo solo un lado de la relacion


while current_approximation != next_approximation
  current_approximation = next_approximation
  next_approximation = []

  for (e, f) in current_approximation:

    first_implication = False

    for a in e.get_actions():
      if f.has_transition_with(a):
        _e = e.get_state_through(a)
        _f = f.get_state_through(a)

        first_implication &= current_approximation.includes((_e, _f))
        # cada par de estados al que llego tiene que estar en la relacion

      else:
        first_implication &= False

    second_implication = False

    for a in f.get_actions():
      if e.has_transition_with(a):
        _e = e.get_state_through(a)
        _f = f.get_state_through(a)

        second_implication &= current_approximation.includes((_e, _f))

      else:
        second_implication &= False

    # verifico solo hacia un lado, porque asumo simetria
    # Me fijo que todas las acciones que e puede hacer, f tambien, y al revez. Solo que me fijo que los estados a los que llegan este, pero de un lado
    if first_implication and second_implication
      next_approximation.append((e, f))


# si current_approximation y next_approximation son iguales, se llego al punto fijo.

return current_approximation + simetric(current_approximation)