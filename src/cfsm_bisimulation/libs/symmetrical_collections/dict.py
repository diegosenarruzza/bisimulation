from .symmetical import Symmetrical


class SymmetricalDict(Symmetrical):

    def safe_add(self, key, symmetric_key):
        self.collection[str(key)] = symmetric_key
        self.symmetric_collection[str(symmetric_key)] = key

    def safe_remove(self, key, symmetric_key):
        del self.collection[str(key)]
        del self.symmetric_collection[str(symmetric_key)]

    def get(self, key):
        return self.current_collection()[str(key)]

    def includes(self, element):
        return str(element) in self.current_collection()

    def copy(self):
        return self.current_collection().copy()
