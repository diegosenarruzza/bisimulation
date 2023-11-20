class Symmetrical:

    def __init__(self, collection, symmetric_collection, initial_symmetry_mode):
        self.collection = collection
        self.symmetric_collection = symmetric_collection
        self.symmetric_mode = False
        self.symmetry_mode = initial_symmetry_mode

    def add(self, element, symmetric_element):
        self.symmetry_mode.add_in(self, element, symmetric_element)

    def remove(self, element, symmetric_element):
        self.symmetry_mode.remove_in(self, element, symmetric_element)

    def current_collection(self):
        return self.symmetry_mode.current_collection_of(self)
