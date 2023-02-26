class Symmetrical:

    def __init__(self, collection, symmetric_collection):
        self.collection = collection
        self.symmetric_collection = symmetric_collection
        self.symmetric_mode = False

    def enable_symmetric_mode(self):
        self.symmetric_mode = True

    def disable_symmetric_mode(self):
        self.symmetric_mode = False

    def _collections(self):
        if self.symmetric_mode:
            return self.symmetric_collection, self.collection
        else:
            return self.collection, self.symmetric_collection

    def _current_collection(self):
        if self.symmetric_mode:
            return self.symmetric_collection
        else:
            return self.collection

    def copy(self):
        return list(self._current_collection())
