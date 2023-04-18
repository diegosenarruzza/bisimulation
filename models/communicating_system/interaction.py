class Interaction:

    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def __repr__(self):
        return f'{self.sender} -> {self.receiver} : {self.message})'

    def __eq__(self, other):
        return self.sender == other.sender and self.receiver == other.receiver and self.message == other.message

    def has_variable(self):
        return self.message.is_carrying_something()

    def contains_any(self, variables):
        return self.message.includes(variables)

    class Message:

        def __init__(self, tag, payload=[]):
            self.tag = tag
            self.payload = payload  # Array of z3 variables: [ Int('x'), Boolean('y') ]

        def __repr__(self):
            return f'{self.tag}({self._str_payload()})'

        def __eq__(self, other):
            return self.tag == other.tag and self.payload == other.payload

        def __hash__(self):
            return hash((self.tag, tuple(hash(var) for var in self.payload)))

        def is_carrying_something(self):
            return len(self.payload) > 0

        def includes(self, variables):
            return any(var in set(self.payload) for var in variables)

        def is_compatible_with(self, message):
            return self.payload_sort() == message.payload_sort()

        def payload_sort(self):
            return list(map(lambda var: var.sort(), self.payload))

        def _str_payload(self):
            return ', '.join(map(lambda var: f'{str(var.sort()).lower()} {str(var)}', self.payload))
