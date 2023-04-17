from .symmetical import Symmetrical


class SymmetricalList(Symmetrical):

    def safe_add(self, element, symmetric_element):
        self.collection.append(element)
        self.symmetric_collection.append(symmetric_element)

    def safe_remove(self, element, symmetric_element):
        self.collection.remove(element)
        self.symmetric_collection.remove(symmetric_element)

    def includes(self, element):
        return element in self.current_collection()

    def is_empty(self):
        return len(self.current_collection()) > 0

    def filter(self, condition):
        return [element for element in self.current_collection() if condition(condition)]

    def copy(self):
        return list(self.current_collection())
