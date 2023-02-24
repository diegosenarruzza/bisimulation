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
