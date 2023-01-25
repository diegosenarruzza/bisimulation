class State:

  def __init__(self, graph, id):
    self.graph = graph
    self.id = id

  def get_transitions(self):
    self.graph.transitions_of(self.id)

  def get_transitions_with(self, label):
    self.graph.transitions_with_label_of(self.id, self.label)


  def is_able_to_simulate_falling_into(self, simulation_state, knowledge, approximation):
      is_able = True
      transitions = self.get_transitions()
      i = 0

      # Si corta porque no cumple is_able, entonces es porque existe una accion que "simulation_state" no puede simular, o que puede pero no cae en la relacion
       # Si corta porque i < len(transitions) entonces recorrio todas las acciones y "simulation_state" siempre pudo simular a e y caer dentro de la relacion
      while is_able and i < len(transitions):
        transition = transitions[i]
        label = transition.label()

        cleaned_knowledge = self.clean_knowledge_for(knowledge, label)
        simulation_transitions = simulation_state.get_transitions_with(label)

        # Necesito verificar si existe algun subconjunto de transiciones desde "simulation_state", que me sirva para simular la transicion de "state"
        # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "state"
        # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

        is_able = transition.exists_a_valid_transition_subset_wich_simulate(simulation_transitions, cleaned_knowledge, approximation)
        # is_able es False si  el "simulation_state" no puede imitar la transicion "transition"

        i += 1

      return is_able


  # TODO: Necesito parsear el label y quedarme con la variable
  # Quizas, el label tiene que ser algo mas que un string
  #   es decir, que su version serializada sea un string, pero que cuando se parsee se convierta en un label acorde al lenguaje de los automatas.
  #   Por lo menos, tiene que saber contestar al mensaje "variable"
  def clean_knowledge_for(self, label):
    pass

  # TODO: este metodo no deberia estar aca. De ultima armar una collection custom para almacenar el conocimiento, y que tenga un metodo "clean" o algo asi.