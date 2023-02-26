from .symmetical import Symmetrical


class SymmetricalList(Symmetrical):

    def add(self, element, symmetric_element):
        current_collection, current_symmetric_collection = self._collections()
        current_collection.append(element)
        current_symmetric_collection.append(symmetric_element)

    def remove(self, element, symmetric_element):
        current_collection, current_symmetric_collection = self._collections()
        current_collection.remove(element)
        current_symmetric_collection.remove(symmetric_element)

    def includes(self, element):
        return element in self._current_collection()

    def is_empty(self):
        return len(self._current_collection()) > 0

    def filter(self, condition):
        return [element for element in self._current_collection() if condition(condition)]
