class Transition:

    def __init__(self, source, target, label, assertion):
        self.source = source
        self.target = target
        self.label = label
        self.assertion = assertion

    def __repr__(self):
        return f"{self.source} -({self.label}, {self.assertion})-> {self.target}"
