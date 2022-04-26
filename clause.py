class Clause:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority

    def __eq__(self, other):
        if type(other) == Clause and other.value == self.value:
            return True
        return False
