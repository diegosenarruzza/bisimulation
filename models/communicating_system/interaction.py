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
        return self.message.incldues(variables)

    class Message:

        def __init__(self, tag, payload=[]):
            self.tag = tag
            self.payload = payload  # Array of z3 variables: [ Int('x'), Boolean('y') ]

        def __repr__(self):
            payload = ', '.join(map(lambda var: f'{str(var.sort()).lower()} {str(var)}', self.payload))
            return f'{self.tag}({payload})'

        def __eq__(self, other):
            return self.tag == other.tag and self.payload == other.payload

        def is_carrying_something(self):
            return len(self.payload) > 0

        def includes(self, variables):
            return any(var in self.payload for var in variables)

        def payload_sort(self):
            return list(map(lambda var: var.sort(), self.payload))
