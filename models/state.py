from libs.tools import clean_knowledge_for


class State:

    def __init__(self, graph, id):
        self.graph = graph
        self.id = id

    def __repr__(self):
        return self.id

    def get_transitions(self):
        return self.graph.transitions_of(self.id)

    def get_transitions_with(self, label):
        return self.graph.transitions_with_label_of(self.id, label)

    def is_able_to_simulate_falling_into(self, simulation_state, knowledge, relation):
        is_able = True
        transitions = self.get_transitions()
        i = 0

        # Si corta porque no cumple is_able, entonces es porque existe una accion que "simulation_state" no puede simular, o que puede pero no cae en la relacion
        # Si corta porque i < len(transitions) entonces recorrio todas las acciones y "simulation_state" siempre pudo simular a e y caer dentro de la relacion
        while is_able and i < len(transitions):
            transition = transitions[i]
            label = transition.label

            # Saco las assertions cuyas variables van a ser sobreescritas por la transicion actual
            cleaned_knowledge = clean_knowledge_for(knowledge, label) if label.has_variable() else knowledge
            simulation_transitions = simulation_state.get_transitions_with(label)

            # Necesito verificar si existe algun subconjunto de transiciones desde "simulation_state", que me sirva para simular la transicion de "self"
            # Si existe, va a ser unico, ya que si existe mas de un subconjunto que hace esto, quiere decir que existen al menos dos transiciones desde "self"
            # tq. ambos caminos son validos para una traza valida. Esto nos daria un automata no-determinista, y estamos trabajando siempre con deterministas.

            is_able = transition.exists_a_valid_transition_subset_that_simulates(simulation_transitions, cleaned_knowledge, relation)

            i += 1

        return is_able
