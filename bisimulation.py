M1 = FSM.new(P, p0, L, T1)
M2 = FSM.new(Q, q0, L, T2)

# esta instanciacion es solo por el orden de ejecucion
current_approximation = []
next_approximation = M1.states.product(M2.states) + M2.states.product(M1.states)


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

        second_implication &= current_approximation.includes((_f, _e))

      else:
        second_implication &= False

    # Si se cumplen las implicaciones para ambos lados, entonces (e, f) esta en la relacion.
    # (f, e) tambien va a estar, pero se va a calcular cuando llegue a esa tupla en la iteracion
    # calcular dos veces eso es innecesario, porque solo invierte el orden el el que se hacen los ciclos,
    # el resultado es el mismo. 
    if first_implication and second_implication
      next_approximation.append((e, f))


# si current_approximation y next_approximation son iguales, se llego al punto fijo.

return current_approximation