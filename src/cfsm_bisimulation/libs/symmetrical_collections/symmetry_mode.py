class SymmetryMode:

    def __init__(self, initial_mode):
        self.mode = initial_mode

    def add_in(self, symmetrical_collection, element, symmetric_element):
        if self.mode:
            symmetrical_collection.safe_add(symmetric_element, element)
        else:
            symmetrical_collection.safe_add(element, symmetric_element)

    def remove_in(self, symmetrical_collection, element, symmetric_element):
        if self.mode:
            symmetrical_collection.safe_remove(symmetric_element, element)
        else:
            symmetrical_collection.safe_remove(element, symmetric_element)

    def current_collection_of(self, symmetrical_collection):
        if self.mode:
            return symmetrical_collection.symmetric_collection
        else:
            return symmetrical_collection.collection

    def enable(self):
        self.mode = True

    def disable(self):
        self.mode = False

    def copy(self):
        return SymmetryMode(bool(self.mode))

    def work_as(self, another_symmetry_mode):
        self.mode = bool(another_symmetry_mode.mode)
