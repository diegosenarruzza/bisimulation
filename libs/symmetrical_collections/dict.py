from .symmetical import Symmetrical


class SymmetricalDict(Symmetrical):

    def add(self, key, symmetric_key):
        current_collection, current_symmetric_collection = self._collections()
        current_collection[str(key)] = symmetric_key
        current_symmetric_collection[str(symmetric_key)] = key

    def remove(self, key, symmetric_key):
        current_collection, current_symmetric_collection = self._collections()
        del current_collection[str(key)]
        del current_symmetric_collection[str(symmetric_key)]

    def get(self, key):
        return self._current_collection()[str(key)]

    def includes(self, element):
        return str(element) in self._current_collection()
